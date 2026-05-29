from __future__ import annotations

from dataclasses import dataclass

from .models import SearchDocument


@dataclass(frozen=True)
class IndexedRow:
    document: SearchDocument
    embedding: list[float]
