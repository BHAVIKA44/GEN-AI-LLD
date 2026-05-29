from __future__ import annotations

from typing import Protocol

from .models import RankedResult, SearchResult


class ReRanker(Protocol):
    def rerank(self, query: str, results: list[SearchResult], top_k: int | None = None) -> list[RankedResult]:
        ...
