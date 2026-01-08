"""Smoke test for the sentiment analysis pipeline."""
from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

os.environ.setdefault("DATABASE_PATH", str(ROOT / "var" / "smoke.db"))
os.environ.setdefault("TWITTER_SOURCE_PATH", str(ROOT / "data" / "sample_tweets.jsonl"))
os.environ.setdefault("NEWS_SOURCE_PATH", str(ROOT / "data" / "sample_news.jsonl"))
os.environ.setdefault("OUTPUT_DIR", str(ROOT / "var" / "smoke"))
os.environ.setdefault("MAX_RECORDS_PER_SOURCE", "25")

import sys

sys.path.append(str(ROOT / "src"))

from sentiment_platform.config import load_config  # noqa: E402
from sentiment_platform.pipeline import Pipeline  # noqa: E402


def main() -> int:
    config = load_config()
    pipeline = Pipeline(config)
    summary = pipeline.run()

    if summary["inserted"] <= 0:
        raise SystemExit("No records inserted during smoke test")

    db_path = config.resolved_database_path
    with sqlite3.connect(db_path.as_posix()) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM sentiment_records")
        count = cursor.fetchone()[0]
        if count < 50:
            raise SystemExit(f"Expected at least 50 records, got {count}")

    print(json.dumps({"inserted": summary["inserted"], "count": count}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
