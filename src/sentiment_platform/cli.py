"""Command line interface for running the pipeline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_config
from .pipeline import Pipeline, format_summary, serialize_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Real-time sentiment analysis pipeline (local)")
    parser.add_argument(
        "--config",
        default=".env",
        help="Path to a .env file with configuration overrides",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the full pipeline")
    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Output summary as JSON instead of human-readable text",
    )

    ingest_parser = subparsers.add_parser("ingest", help="Only run ingestion")
    ingest_parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional per-source limit on ingested records",
    )

    analyze_parser = subparsers.add_parser("analyze", help="Analyze one text string")
    analyze_parser.add_argument("text", help="Text to analyze")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(dotenv_path=Path(args.config))
    pipeline = Pipeline(config)

    if args.command == "run":
        summary = pipeline.run()
        if args.json:
            print(json.dumps(serialize_summary(summary), indent=2))
        else:
            print(format_summary(summary))
        return 0

    if args.command == "ingest":
        if args.limit is not None:
            config = config.__class__(
                database_path=config.database_path,
                twitter_source_path=config.twitter_source_path,
                news_source_path=config.news_source_path,
                output_dir=config.output_dir,
                max_records_per_source=args.limit,
            )
            pipeline = Pipeline(config)
        records = pipeline.ingest()
        print(f"Ingested {len(records)} records")
        return 0

    if args.command == "analyze":
        result = pipeline.analyzer.analyze(args.text)
        print(
            json.dumps(
                {
                    "sentiment": result.label,
                    "polarity": result.polarity,
                    "matches": result.matches,
                },
                indent=2,
            )
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
