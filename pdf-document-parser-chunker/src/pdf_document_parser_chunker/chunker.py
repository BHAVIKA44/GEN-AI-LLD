from __future__ import annotations

from .models import TextChunk


class FixedWordChunker:
    def __init__(self, words_per_chunk: int = 120, overlap_words: int = 20) -> None:
        if words_per_chunk <= 0:
            raise ValueError("words_per_chunk must be > 0")
        if overlap_words < 0 or overlap_words >= words_per_chunk:
            raise ValueError("overlap_words must be >= 0 and < words_per_chunk")
        self._words_per_chunk = words_per_chunk
        self._overlap_words = overlap_words

    def chunk(self, text: str) -> list[TextChunk]:
        words = text.split()
        if not words:
            return []

        step = self._words_per_chunk - self._overlap_words
        out: list[TextChunk] = []
        idx = 0
        for start in range(0, len(words), step):
            segment = words[start : start + self._words_per_chunk]
            if not segment:
                break
            out.append(TextChunk(chunk_id=f"chunk-{idx}", text=" ".join(segment)))
            idx += 1
            if start + self._words_per_chunk >= len(words):
                break
        return out
