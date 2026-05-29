from __future__ import annotations

from typing import Protocol

from .models import TextChunk


class TextChunker(Protocol):
    def chunk(self, text: str) -> list[TextChunk]:
        ...
