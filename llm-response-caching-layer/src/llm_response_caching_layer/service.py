from __future__ import annotations

import hashlib

from .interfaces import CacheStore, LLMProvider
from .models import LLMRequest, LLMResponse


class CachedLLMService:
    def __init__(self, provider: LLMProvider, cache: CacheStore, ttl_seconds: int = 300) -> None:
        if ttl_seconds < 0:
            raise ValueError("ttl_seconds must be >= 0")
        self._provider = provider
        self._cache = cache
        self._ttl_seconds = ttl_seconds

    def generate(self, request: LLMRequest) -> tuple[LLMResponse, bool]:
        key = self._cache_key(request)
        cached = self._cache.get(key)
        if cached is not None:
            return cached, True

        response = self._provider.generate(request)
        self._cache.set(key, response, self._ttl_seconds)
        return response, False

    @staticmethod
    def _cache_key(request: LLMRequest) -> str:
        raw = f"{request.model}|{request.temperature}|{request.prompt}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()
