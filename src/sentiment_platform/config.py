"""Configuration loader for the sentiment platform."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable


@dataclass(frozen=True)
class Config:
    """Runtime configuration.

    Attributes:
        database_path: Path to the SQLite database file.
        twitter_source_path: Path to the sample twitter JSONL file.
        news_source_path: Path to the sample news JSONL file.
        output_dir: Directory for generated artifacts/logs.
        max_records_per_source: Optional limit for records ingested.
    """

    database_path: Path
    twitter_source_path: Path
    news_source_path: Path
    output_dir: Path
    max_records_per_source: int | None = None

    @property
    def resolved_database_path(self) -> Path:
        return self.database_path.expanduser().resolve()


DEFAULTS = {
    "DATABASE_PATH": "./var/sentiment.db",
    "TWITTER_SOURCE_PATH": "./data/sample_tweets.jsonl",
    "NEWS_SOURCE_PATH": "./data/sample_news.jsonl",
    "OUTPUT_DIR": "./var/output",
    "MAX_RECORDS_PER_SOURCE": "",
}


def _parse_env_value(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    return value


def _load_dotenv(dotenv_path: Path) -> Dict[str, str]:
    """Load dotenv-style key=value pairs.

    Lines starting with # are ignored. Quotes are stripped when present.
    """

    if not dotenv_path.exists():
        return {}

    entries: Dict[str, str] = {}
    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        value = value.strip().strip("'\"")
        entries[key.strip()] = value
    return entries


def load_config(env: Dict[str, str] | None = None, dotenv_path: Path | None = None) -> Config:
    env = dict(os.environ if env is None else env)
    dotenv_data: Dict[str, str] = {}
    if dotenv_path is None:
        dotenv_path = Path(".env")
    dotenv_data.update(_load_dotenv(dotenv_path))

    def get_value(key: str) -> str | None:
        return env.get(key) or dotenv_data.get(key) or DEFAULTS.get(key)

    database_path = Path(get_value("DATABASE_PATH") or DEFAULTS["DATABASE_PATH"])
    twitter_source_path = Path(
        get_value("TWITTER_SOURCE_PATH") or DEFAULTS["TWITTER_SOURCE_PATH"]
    )
    news_source_path = Path(get_value("NEWS_SOURCE_PATH") or DEFAULTS["NEWS_SOURCE_PATH"])
    output_dir = Path(get_value("OUTPUT_DIR") or DEFAULTS["OUTPUT_DIR"])
    max_records_value = _parse_env_value(get_value("MAX_RECORDS_PER_SOURCE") or "")
    max_records = int(max_records_value) if max_records_value else None

    return Config(
        database_path=database_path,
        twitter_source_path=twitter_source_path,
        news_source_path=news_source_path,
        output_dir=output_dir,
        max_records_per_source=max_records,
    )


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
