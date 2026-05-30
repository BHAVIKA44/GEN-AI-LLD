from vector_metrics_from_scratch.metrics import (
    cosine_similarity,
    dot_product,
    euclidean_distance,
)


def test_dot_product() -> None:
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32


def test_euclidean_distance() -> None:
    distance = euclidean_distance([1, 2], [4, 6])
    assert round(distance, 6) == 5.0


def test_cosine_similarity() -> None:
    score = cosine_similarity([1, 0, 1], [1, 1, 0])
    assert round(score, 6) == round(0.5, 6)


def test_cosine_similarity_zero_vector_returns_zero() -> None:
    assert cosine_similarity([0, 0], [1, 2]) == 0.0


def test_dimension_mismatch_raises() -> None:
    try:
        dot_product([1, 2], [1])
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "same dimension" in str(exc)


def test_empty_vector_raises() -> None:
    try:
        euclidean_distance([], [])
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "must not be empty" in str(exc)
