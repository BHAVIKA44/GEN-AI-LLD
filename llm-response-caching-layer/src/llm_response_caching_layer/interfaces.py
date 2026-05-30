from __future__ import annotations

from typing import Protocol

from .models import LLMRequest, LLMResponse


class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        ...


class CacheStore(Protocol):
    def get(self, key: str) -> LLMResponse | None:
        ...

    def set(self, key: str, value: LLMResponse, ttl_seconds: int) -> None:
        ...
