from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    model: str
    temperature: float = 0.0


@dataclass(frozen=True)
class LLMResponse:
    text: str


@dataclass(frozen=True)
class CacheEntry:
    value: LLMResponse
    expires_at: float
