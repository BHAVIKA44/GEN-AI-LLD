from __future__ import annotations

from .interfaces import EmbeddingProvider, LLMProvider
from .models import LLMAnswer, LLMQuery
from .cache import InMemorySemanticCache


class SemanticCachedLLMService:
    def __init__(
        self,
        llm_provider: LLMProvider,
        embedding_provider: EmbeddingProvider,
        cache: InMemorySemanticCache,
        ttl_seconds: int = 300,
    ) -> None:
        self._llm = llm_provider
        self._emb = embedding_provider
        self._cache = cache
        self._ttl = ttl_seconds

    def generate(self, query: LLMQuery) -> tuple[LLMAnswer, bool]:
        vector = self._emb.embed_query(query.text)
        cached = self._cache.lookup(query, vector)
        if cached is not None:
            return cached, True

        fresh = self._llm.generate(query)
        self._cache.store(query, vector, fresh, self._ttl)
        return fresh, False
