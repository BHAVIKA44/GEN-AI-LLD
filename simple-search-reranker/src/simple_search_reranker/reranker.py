from __future__ import annotations

import re

from .models import RankedResult, SearchResult


class SimpleReRanker:
    def __init__(self, base_weight: float = 0.6, overlap_weight: float = 0.4) -> None:
        if base_weight < 0 or overlap_weight < 0:
            raise ValueError("weights must be >= 0")
        if base_weight == 0 and overlap_weight == 0:
            raise ValueError("at least one weight must be > 0")
        self._base_weight = base_weight
        self._overlap_weight = overlap_weight

    def rerank(self, query: str, results: list[SearchResult], top_k: int | None = None) -> list[RankedResult]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k is not None and top_k <= 0:
            raise ValueError("top_k must be > 0")

        query_terms = self._terms(query)
        reranked: list[RankedResult] = []

        for result in results:
            overlap = self._term_overlap_score(query_terms, self._terms(result.text))
            score = self._base_weight * result.base_score + self._overlap_weight * overlap
            reranked.append(
                RankedResult(
                    doc_id=result.doc_id,
                    text=result.text,
                    base_score=result.base_score,
                    rerank_score=score,
                )
            )

        reranked.sort(key=lambda r: r.rerank_score, reverse=True)
        return reranked if top_k is None else reranked[:top_k]

    @staticmethod
    def _terms(text: str) -> set[str]:
        return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))

    @staticmethod
    def _term_overlap_score(query_terms: set[str], doc_terms: set[str]) -> float:
        if not query_terms:
            return 0.0
        return len(query_terms & doc_terms) / len(query_terms)
