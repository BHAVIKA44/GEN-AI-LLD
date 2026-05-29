from __future__ import annotations

from langchain_core.embeddings import Embeddings


class FakeEmbeddings(Embeddings):
    """Deterministic local embeddings for offline tests."""

    def __init__(self, dims: int = 24) -> None:
        if dims <= 0:
            raise ValueError("dims must be > 0")
        self._dims = dims

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self._dims
        for i, ch in enumerate(text.lower()):
            vec[i % self._dims] += (ord(ch) % 37) / 37.0
        norm = sum(v * v for v in vec) ** 0.5
        return vec if norm == 0 else [v / norm for v in vec]
