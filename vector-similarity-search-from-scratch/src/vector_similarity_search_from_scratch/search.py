from __future__ import annotations

from .errors import DimensionMismatchError
from .index import InMemoryVectorIndex
from .models import SearchResult
from .similarity import cosine_similarity


class VectorSimilaritySearch:
    def __init__(self, index: InMemoryVectorIndex) -> None:
        self._index = index

    def search(self, query_vector: list[float], top_k: int = 3) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be > 0")
        if len(query_vector) != self._index.dimension:
            raise DimensionMismatchError(
                f"expected query dimension {self._index.dimension}, got {len(query_vector)}"
            )

        scored: list[SearchResult] = []
        for record in self._index.get_all():
            score = cosine_similarity(query_vector, record.vector)
            scored.append(
                SearchResult(
                    record_id=record.record_id,
                    score=score,
                    payload=record.payload,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
