from __future__ import annotations

from .models import TextChunk


class LangChainRecursiveChunker:
    """Optional adapter over LangChain RecursiveCharacterTextSplitter."""

    def __init__(self, chunk_size: int = 140, chunk_overlap: int = 20) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
        except ImportError as exc:
            raise ImportError(
                "langchain-text-splitters is required for LangChainRecursiveChunker"
            ) from exc

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, text: str) -> list[TextChunk]:
        cleaned = text.strip()
        if not cleaned:
            return []

        parts = self._splitter.split_text(cleaned)
        return [TextChunk(chunk_id=f"lc-recursive-{i}", text=part) for i, part in enumerate(parts)]
