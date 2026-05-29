from __future__ import annotations

from .models import TextChunk


class FixedSizeChunker:
    def __init__(self, chunk_size: int = 120, overlap: int = 20) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if overlap < 0 or overlap >= chunk_size:
            raise ValueError("overlap must be >= 0 and < chunk_size")
        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk(self, text: str) -> list[TextChunk]:
        cleaned = text.strip()
        if not cleaned:
            return []

        out: list[TextChunk] = []
        step = self._chunk_size - self._overlap
        idx = 0
        for start in range(0, len(cleaned), step):
            segment = cleaned[start : start + self._chunk_size]
            if not segment:
                break
            out.append(TextChunk(chunk_id=f"fixed-{idx}", text=segment))
            idx += 1
            if start + self._chunk_size >= len(cleaned):
                break
        return out
