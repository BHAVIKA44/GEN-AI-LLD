from __future__ import annotations

import time

from .models import CacheEntry, LLMResponse


class InMemoryTTLCache:
    def __init__(self, now_fn=None) -> None:
        self._now = now_fn or time.time
        self._data: dict[str, CacheEntry] = {}

    def get(self, key: str) -> LLMResponse | None:
        entry = self._data.get(key)
        if entry is None:
            return None
        if self._now() >= entry.expires_at:
            self._data.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: LLMResponse, ttl_seconds: int) -> None:
        if ttl_seconds <= 0:
            return
        self._data[key] = CacheEntry(value=value, expires_at=self._now() + ttl_seconds)
