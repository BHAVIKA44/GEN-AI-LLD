from __future__ import annotations

import re

from .models import TextChunk


class SemanticChunker:
    """Simple semantic chunker using sentence boundaries + topic similarity heuristic."""

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        if max_sentences_per_chunk <= 0:
            raise ValueError("max_sentences_per_chunk must be > 0")
        self._max_sentences = max_sentences_per_chunk

    def chunk(self, text: str) -> list[TextChunk]:
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        chunks: list[list[str]] = []
        current: list[str] = [sentences[0]]

        for sentence in sentences[1:]:
            if len(current) >= self._max_sentences:
                chunks.append(current)
                current = [sentence]
                continue

            prev_terms = self._keywords(" ".join(current))
            next_terms = self._keywords(sentence)
            overlap = len(prev_terms & next_terms)

            if overlap == 0 and current:
                chunks.append(current)
                current = [sentence]
            else:
                current.append(sentence)

        if current:
            chunks.append(current)

        return [TextChunk(chunk_id=f"semantic-{i}", text=" ".join(group)) for i, group in enumerate(chunks)]

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        cleaned = text.strip()
        if not cleaned:
            return []
        parts = re.split(r"(?<=[.!?])\s+", cleaned)
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _keywords(text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z]{4,}", text.lower())
        stop = {"this", "that", "with", "from", "have", "will", "would", "about"}
        return {w for w in words if w not in stop}
