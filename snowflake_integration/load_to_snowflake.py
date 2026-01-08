"""Compatibility wrapper for data loading.

Loads the processed sentiment data into a local SQLite database.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from sentiment_platform.config import load_config  # noqa: E402
from sentiment_platform.pipeline import Pipeline, format_summary  # noqa: E402


def main() -> int:
    config = load_config()
    pipeline = Pipeline(config)
    summary = pipeline.run()
    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
