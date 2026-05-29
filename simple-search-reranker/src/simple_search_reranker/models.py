from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    doc_id: str
    text: str
    base_score: float


@dataclass(frozen=True)
class RankedResult:
    doc_id: str
    text: str
    base_score: float
    rerank_score: float
