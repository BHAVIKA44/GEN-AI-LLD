from __future__ import annotations

import json
from typing import AsyncIterator

from .interfaces import LLMProvider


class LLMService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def generate(self, prompt: str) -> str:
        return await self._provider.generate(prompt)

    async def stream_sse(self, prompt: str) -> AsyncIterator[str]:
        async for token in self._provider.stream_generate(prompt):
            payload = {"type": "token", "text": token}
            yield f"data: {json.dumps(payload)}\n\n"

        done = {"type": "done"}
        yield f"data: {json.dumps(done)}\n\n"
