"""Data models for the sentiment platform."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

SourceType = Literal["twitter", "news"]


@dataclass(frozen=True)
class IngestedRecord:
    """Normalized record from an ingestion source."""

    record_id: str
    source: SourceType
    text: str
    created_at: datetime
    raw_payload: dict


@dataclass(frozen=True)
class SentimentRecord:
    """Record enriched with sentiment analysis."""

    record_id: str
    source: SourceType
    text: str
    created_at: datetime
    sentiment: str
    polarity: float
    raw_payload: dict
