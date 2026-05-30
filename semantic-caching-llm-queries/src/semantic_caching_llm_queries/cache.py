from __future__ import annotations

import math
import time

from .models import LLMAnswer, LLMQuery, SemanticCacheEntry


class InMemorySemanticCache:
    def __init__(self, similarity_threshold: float = 0.9, now_fn=None) -> None:
        if not (0 <= similarity_threshold <= 1):
            raise ValueError("similarity_threshold must be between 0 and 1")
        self._threshold = similarity_threshold
        self._now = now_fn or time.time
        self._entries: list[SemanticCacheEntry] = []

    def lookup(self, query: LLMQuery, embedding: list[float]) -> LLMAnswer | None:
        self._evict_expired()
        best: tuple[float, LLMAnswer] | None = None
        for e in self._entries:
            if e.query.model != query.model:
                continue
            sim = self._cosine(embedding, e.embedding)
            if sim >= self._threshold and (best is None or sim > best[0]):
                best = (sim, e.answer)
        return None if best is None else best[1]

    def store(self, query: LLMQuery, embedding: list[float], answer: LLMAnswer, ttl_seconds: int) -> None:
        if ttl_seconds <= 0:
            return
        self._entries.append(
            SemanticCacheEntry(
                query=query,
                embedding=embedding,
                answer=answer,
                expires_at=self._now() + ttl_seconds,
            )
        )

    def _evict_expired(self) -> None:
        now = self._now()
        self._entries = [e for e in self._entries if e.expires_at > now]

    @staticmethod
    def _cosine(a: list[float], b: list[float]) -> float:
        if len(a) != len(b):
            raise ValueError("embedding dimension mismatch")
        dot = sum(x * y for x, y in zip(a, b))
        an = math.sqrt(sum(x * x for x in a))
        bn = math.sqrt(sum(y * y for y in b))
        if an == 0 or bn == 0:
            return 0.0
        return dot / (an * bn)
