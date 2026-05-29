from __future__ import annotations

from .errors import DimensionMismatchError
from .models import VectorRecord


class InMemoryVectorIndex:
    def __init__(self, dimension: int) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be > 0")
        self._dimension = dimension
        self._records: dict[str, VectorRecord] = {}

    @property
    def dimension(self) -> int:
        return self._dimension

    def upsert(self, record: VectorRecord) -> None:
        self._validate_dimension(record.vector)
        self._records[record.record_id] = record

    def get_all(self) -> list[VectorRecord]:
        return list(self._records.values())

    def size(self) -> int:
        return len(self._records)

    def _validate_dimension(self, vector: list[float]) -> None:
        if len(vector) != self._dimension:
            raise DimensionMismatchError(
                f"expected dimension {self._dimension}, got {len(vector)}"
            )
