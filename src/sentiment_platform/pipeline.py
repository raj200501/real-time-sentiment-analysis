"""Pipeline orchestration for ingestion, sentiment analysis, and storage."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List

from .config import Config, ensure_directories
from .ingest import IngestedRecord, iter_records
from .models import SentimentRecord
from .sentiment import SentimentAnalyzer
from .storage import fetch_counts, fetch_latest, initialize, insert_records


class Pipeline:
    """Run the end-to-end pipeline locally."""

    def __init__(self, config: Config):
        self.config = config
        self.analyzer = SentimentAnalyzer()

    def ingest(self) -> List[IngestedRecord]:
        records = list(
            iter_records(
                self.config.twitter_source_path,
                self.config.news_source_path,
                limit_per_source=self.config.max_records_per_source,
            )
        )
        return records

    def analyze(self, records: Iterable[IngestedRecord]) -> List[SentimentRecord]:
        enriched: List[SentimentRecord] = []
        for record in records:
            result = self.analyzer.analyze(record.text)
            enriched.append(
                SentimentRecord(
                    record_id=record.record_id,
                    source=record.source,
                    text=record.text,
                    created_at=record.created_at,
                    sentiment=result.label,
                    polarity=result.polarity,
                    raw_payload=record.raw_payload,
                )
            )
        return enriched

    def store(self, records: Iterable[SentimentRecord]) -> int:
        initialize(self.config.resolved_database_path)
        return insert_records(self.config.resolved_database_path, records)

    def run(self) -> dict:
        ensure_directories([self.config.output_dir, self.config.database_path.parent])
        records = self.ingest()
        enriched = self.analyze(records)
        inserted = self.store(enriched)
        counts = fetch_counts(self.config.resolved_database_path)
        latest = fetch_latest(self.config.resolved_database_path)
        return {
            "inserted": inserted,
            "counts": counts,
            "latest": latest,
        }


def format_summary(result: dict) -> str:
    counts = result.get("counts", [])
    latest = result.get("latest", [])
    lines = ["Pipeline summary:", f"  inserted: {result.get('inserted', 0)}"]
    lines.append("  sentiment counts:")
    for sentiment, count in counts:
        lines.append(f"    - {sentiment}: {count}")
    lines.append("  latest records:")
    for record in latest:
        lines.append(
            "    - "
            + ", ".join(
                [
                    record["record_id"],
                    record["source"],
                    record["sentiment"],
                    record["created_at"],
                ]
            )
        )
    return "\n".join(lines)


def serialize_summary(result: dict) -> dict:
    return {
        "inserted": result.get("inserted", 0),
        "counts": [
            {"sentiment": sentiment, "count": count} for sentiment, count in result.get("counts", [])
        ],
        "latest": [record for record in result.get("latest", [])],
    }
