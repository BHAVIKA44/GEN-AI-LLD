from __future__ import annotations

from .models import TextChunk


class RecursiveChunker:
    def __init__(self, max_chars: int = 140, separators: list[str] | None = None) -> None:
        if max_chars <= 0:
            raise ValueError("max_chars must be > 0")
        self._max_chars = max_chars
        self._separators = separators or ["\n\n", "\n", ". ", " "]

    def chunk(self, text: str) -> list[TextChunk]:
        cleaned = text.strip()
        if not cleaned:
            return []
        raw = self._split_recursive(cleaned, self._separators)
        return [TextChunk(chunk_id=f"recursive-{i}", text=part) for i, part in enumerate(raw)]

    def _split_recursive(self, text: str, separators: list[str]) -> list[str]:
        if len(text) <= self._max_chars:
            return [text]
        if not separators:
            return [text[i : i + self._max_chars] for i in range(0, len(text), self._max_chars)]

        sep = separators[0]
        pieces = text.split(sep)
        if len(pieces) == 1:
            return self._split_recursive(text, separators[1:])

        chunks: list[str] = []
        current = ""
        for piece in pieces:
            candidate = piece if not current else current + sep + piece
            if len(candidate) <= self._max_chars:
                current = candidate
            else:
                if current:
                    chunks.extend(self._split_recursive(current.strip(), separators[1:]))
                current = piece
        if current:
            chunks.extend(self._split_recursive(current.strip(), separators[1:]))
        return [c for c in chunks if c]
