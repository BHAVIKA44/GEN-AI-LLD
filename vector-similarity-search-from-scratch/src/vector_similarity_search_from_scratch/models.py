from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VectorRecord:
    record_id: str
    vector: list[float]
    payload: str | None = None


@dataclass(frozen=True)
class SearchResult:
    record_id: str
    score: float
    payload: str | None
