from __future__ import annotations

from typing import Protocol

from .models import LLMAnswer, LLMQuery


class EmbeddingProvider(Protocol):
    def embed_query(self, text: str) -> list[float]: ...


class LLMProvider(Protocol):
    def generate(self, query: LLMQuery) -> LLMAnswer: ...
