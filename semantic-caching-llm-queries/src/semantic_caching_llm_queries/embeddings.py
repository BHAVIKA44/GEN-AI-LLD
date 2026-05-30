from __future__ import annotations


class FakeEmbeddings:
    def __init__(self, dims: int = 24) -> None:
        self._dims = dims

    def embed_query(self, text: str) -> list[float]:
        vec = [0.0] * self._dims
        for i, ch in enumerate(text.lower()):
            vec[i % self._dims] += (ord(ch) % 31) / 31.0
        norm = sum(v * v for v in vec) ** 0.5
        return vec if norm == 0 else [v / norm for v in vec]
