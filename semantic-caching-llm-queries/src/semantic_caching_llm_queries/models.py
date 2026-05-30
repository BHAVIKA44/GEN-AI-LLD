from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMQuery:
    text: str
    model: str


@dataclass(frozen=True)
class LLMAnswer:
    text: str


@dataclass(frozen=True)
class SemanticCacheEntry:
    query: LLMQuery
    embedding: list[float]
    answer: LLMAnswer
    expires_at: float
