"""Data ingestion for local sample sources."""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator, List

from .models import IngestedRecord, SourceType


class IngestionError(RuntimeError):
    """Raised when ingestion cannot proceed."""


def _load_json_lines(path: Path) -> List[dict]:
    if not path.exists():
        raise IngestionError(f"Missing source file: {path}")
    records = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise IngestionError(f"Invalid JSON on line {idx} in {path}: {exc}") from exc
    return records


def _parse_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IngestionError(f"Invalid datetime value: {value}") from exc


def load_records(path: Path, source: SourceType, text_key: str, date_key: str) -> List[IngestedRecord]:
    payloads = _load_json_lines(path)
    records = []
    for payload in payloads:
        text = payload.get(text_key)
        created_at = payload.get(date_key)
        record_id = payload.get("id") or payload.get("record_id")
        if not text or not created_at:
            raise IngestionError(f"Missing required keys in {source} payload: {payload}")
        records.append(
            IngestedRecord(
                record_id=str(record_id or f"{source}-{len(records) + 1}"),
                source=source,
                text=text,
                created_at=_parse_datetime(created_at),
                raw_payload=payload,
            )
        )
    return records


def iter_records(
    twitter_path: Path,
    news_path: Path,
    limit_per_source: int | None = None,
) -> Iterator[IngestedRecord]:
    twitter_records = load_records(twitter_path, "twitter", "text", "created_at")
    news_records = load_records(news_path, "news", "description", "published_at")

    if limit_per_source is not None:
        twitter_records = twitter_records[:limit_per_source]
        news_records = news_records[:limit_per_source]

    for record in twitter_records + news_records:
        yield record


def summarize_records(records: Iterable[IngestedRecord]) -> dict:
    summary = {
        "twitter": 0,
        "news": 0,
        "total": 0,
    }
    for record in records:
        summary[record.source] += 1
        summary["total"] += 1
    return summary


def serialize_records(records: Iterable[IngestedRecord]) -> List[dict]:
    return [asdict(record) for record in records]
