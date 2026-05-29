from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceChunk:
    content: str
    score: float


@dataclass(frozen=True)
class RAGResult:
    answer: str
    sources: list[SourceChunk]
