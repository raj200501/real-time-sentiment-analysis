"""SQLite storage for sentiment records."""
from __future__ import annotations

import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, List, Tuple

from .models import SentimentRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS sentiment_records (
    record_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    polarity REAL NOT NULL,
    raw_payload TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sentiment_source ON sentiment_records(source);
CREATE INDEX IF NOT EXISTS idx_sentiment_label ON sentiment_records(sentiment);
"""


class StorageError(RuntimeError):
    """Raised when storage actions fail."""


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path.as_posix())


def initialize(path: Path) -> None:
    with _connect(path) as conn:
        conn.executescript(SCHEMA)


def insert_records(path: Path, records: Iterable[SentimentRecord]) -> int:
    payloads = []
    for record in records:
        row = (
            record.record_id,
            record.source,
            record.text,
            record.created_at.isoformat(),
            record.sentiment,
            record.polarity,
            str(record.raw_payload),
        )
        payloads.append(row)
    if not payloads:
        return 0
    with _connect(path) as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO sentiment_records (
                record_id, source, text, created_at, sentiment, polarity, raw_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            payloads,
        )
    return len(payloads)


def fetch_counts(path: Path) -> List[Tuple[str, int]]:
    with _connect(path) as conn:
        cursor = conn.execute(
            """
            SELECT sentiment, COUNT(*)
            FROM sentiment_records
            GROUP BY sentiment
            ORDER BY sentiment
            """
        )
        return cursor.fetchall()


def fetch_latest(path: Path, limit: int = 5) -> List[dict]:
    with _connect(path) as conn:
        cursor = conn.execute(
            """
            SELECT record_id, source, text, created_at, sentiment, polarity
            FROM sentiment_records
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [
            {
                "record_id": row[0],
                "source": row[1],
                "text": row[2],
                "created_at": row[3],
                "sentiment": row[4],
                "polarity": row[5],
            }
            for row in cursor.fetchall()
        ]


def serialize_counts(counts: Iterable[Tuple[str, int]]) -> List[dict]:
    return [{"sentiment": sentiment, "count": count} for sentiment, count in counts]
