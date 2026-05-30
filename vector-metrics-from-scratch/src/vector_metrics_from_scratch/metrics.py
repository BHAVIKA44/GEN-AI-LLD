from __future__ import annotations

import math


def _validate_same_dimension(a: list[float], b: list[float]) -> None:
    if len(a) != len(b):
        raise ValueError("vectors must have same dimension")
    if not a:
        raise ValueError("vectors must not be empty")


def dot_product(a: list[float], b: list[float]) -> float:
    _validate_same_dimension(a, b)
    return sum(x * y for x, y in zip(a, b))


def euclidean_distance(a: list[float], b: list[float]) -> float:
    _validate_same_dimension(a, b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    _validate_same_dimension(a, b)
    numerator = dot_product(a, b)
    norm_a = math.sqrt(dot_product(a, a))
    norm_b = math.sqrt(dot_product(b, b))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return numerator / (norm_a * norm_b)
