from __future__ import annotations

from typing import Protocol

from .models import SearchDocument, SearchHit


class EmbeddingProvider(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...


class SemanticSearchService(Protocol):
    def index(self, documents: list[SearchDocument]) -> int:
        ...

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        ...
