from __future__ import annotations

import math

from .embeddings import FakeEmbeddings
from .index import IndexedRow
from .interfaces import EmbeddingProvider, SemanticSearchService
from .models import SearchDocument, SearchHit


class InMemorySemanticSearch(SemanticSearchService):
    def __init__(self, embedding_provider: EmbeddingProvider | None = None) -> None:
        self._embedding_provider = embedding_provider or FakeEmbeddings()
        self._rows: list[IndexedRow] = []

    def index(self, documents: list[SearchDocument]) -> int:
        valid_docs = [d for d in documents if d.text.strip()]
        if not valid_docs:
            return 0

        vectors = self._embedding_provider.embed_documents([d.text for d in valid_docs])
        for doc, vector in zip(valid_docs, vectors):
            self._rows.append(IndexedRow(document=doc, embedding=vector))
        return len(valid_docs)

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be > 0")
        if not self._rows:
            return []

        qvec = self._embedding_provider.embed_query(query)
        hits: list[SearchHit] = []
        for row in self._rows:
            score = self._cosine_similarity(qvec, row.embedding)
            hits.append(SearchHit(doc_id=row.document.doc_id, text=row.document.text, score=score))

        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:top_k]

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        if len(a) != len(b):
            raise ValueError("embedding dimension mismatch")
        dot = sum(x * y for x, y in zip(a, b))
        an = math.sqrt(sum(x * x for x in a))
        bn = math.sqrt(sum(y * y for y in b))
        if an == 0 or bn == 0:
            return 0.0
        return dot / (an * bn)
