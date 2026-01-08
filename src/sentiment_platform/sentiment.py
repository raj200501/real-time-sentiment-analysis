"""Sentiment analysis implementation used by the pipeline."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Iterable, Tuple

from .lexicon import NEGATIVE_WORDS, NEGATORS, POSITIVE_WORDS

TOKEN_PATTERN = re.compile(r"[a-zA-Z']+")


@dataclass(frozen=True)
class SentimentResult:
    label: str
    polarity: float
    matches: Tuple[str, ...]


class SentimentAnalyzer:
    """Deterministic sentiment analyzer based on a curated lexicon."""

    def __init__(self, positive: Iterable[str] | None = None, negative: Iterable[str] | None = None):
        self.positive = set(word.lower() for word in (positive or POSITIVE_WORDS))
        self.negative = set(word.lower() for word in (negative or NEGATIVE_WORDS))

    def tokenize(self, text: str) -> Tuple[str, ...]:
        return tuple(match.group(0).lower() for match in TOKEN_PATTERN.finditer(text))

    def score(self, tokens: Iterable[str]) -> Tuple[float, Tuple[str, ...]]:
        score = 0.0
        matches = []
        previous_token = ""
        for token in tokens:
            modifier = -1 if previous_token in NEGATORS else 1
            if token in self.positive:
                score += 1.0 * modifier
                matches.append(token)
            elif token in self.negative:
                score -= 1.0 * modifier
                matches.append(token)
            previous_token = token
        return score, tuple(matches)

    def analyze(self, text: str) -> SentimentResult:
        tokens = self.tokenize(text)
        score, matches = self.score(tokens)
        polarity = math.tanh(score / 3.0) if score else 0.0
        if polarity > 0.05:
            label = "positive"
        elif polarity < -0.05:
            label = "negative"
        else:
            label = "neutral"
        return SentimentResult(label=label, polarity=polarity, matches=matches)
