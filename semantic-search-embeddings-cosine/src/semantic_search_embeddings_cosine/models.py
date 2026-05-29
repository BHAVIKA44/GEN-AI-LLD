from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchDocument:
    doc_id: str
    text: str


@dataclass(frozen=True)
class SearchHit:
    doc_id: str
    text: str
    score: float
