from __future__ import annotations

from typing import Protocol

from .models import RAGResult


class KnowledgeIndexer(Protocol):
    def index_texts(self, texts: list[str]) -> int:
        """Index raw documents and return indexed chunk count."""


class QueryAnsweringService(Protocol):
    def answer(self, query: str, top_k: int = 3) -> RAGResult:
        """Answer a question with retrieval-augmented context."""
