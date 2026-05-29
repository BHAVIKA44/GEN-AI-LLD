from __future__ import annotations

from typing import AsyncIterator, Protocol


class LLMProvider(Protocol):
    async def generate(self, prompt: str) -> str:
        ...

    async def stream_generate(self, prompt: str) -> AsyncIterator[str]:
        ...
