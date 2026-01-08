"""Compatibility wrapper for twitter ingestion.

Reads local sample data and prints a summary of ingested records.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from sentiment_platform.config import load_config  # noqa: E402
from sentiment_platform.ingest import load_records  # noqa: E402


def main() -> int:
    config = load_config()
    records = load_records(
        Path(config.twitter_source_path),
        "twitter",
        "text",
        "created_at",
    )
    print(f"Loaded {len(records)} twitter records from {config.twitter_source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
