from __future__ import annotations

import asyncio
from typing import AsyncIterator


class FakeStreamingLLMProvider:
    """Deterministic local provider for interview/testing."""

    async def generate(self, prompt: str) -> str:
        return f"Echo: {prompt}"

    async def stream_generate(self, prompt: str) -> AsyncIterator[str]:
        output = f"Echo: {prompt}"
        for token in output.split(" "):
            await asyncio.sleep(0)
            yield token + " "
