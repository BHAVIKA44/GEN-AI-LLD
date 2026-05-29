from vector_similarity_search_from_scratch.errors import DimensionMismatchError
from vector_similarity_search_from_scratch.index import InMemoryVectorIndex
from vector_similarity_search_from_scratch.models import VectorRecord
from vector_similarity_search_from_scratch.search import VectorSimilaritySearch


def test_search_returns_ranked_results() -> None:
    index = InMemoryVectorIndex(dimension=3)
    index.upsert(VectorRecord(record_id="a", vector=[1.0, 0.0, 0.0], payload="doc-a"))
    index.upsert(VectorRecord(record_id="b", vector=[0.0, 1.0, 0.0], payload="doc-b"))
    index.upsert(VectorRecord(record_id="c", vector=[0.8, 0.2, 0.0], payload="doc-c"))

    search = VectorSimilaritySearch(index)
    results = search.search([1.0, 0.0, 0.0], top_k=2)

    assert len(results) == 2
    assert results[0].record_id == "a"
    assert results[0].score >= results[1].score


def test_upsert_replaces_existing_record() -> None:
    index = InMemoryVectorIndex(dimension=2)
    index.upsert(VectorRecord(record_id="x", vector=[1.0, 0.0]))
    index.upsert(VectorRecord(record_id="x", vector=[0.0, 1.0]))

    search = VectorSimilaritySearch(index)
    results = search.search([0.0, 1.0], top_k=1)

    assert index.size() == 1
    assert results[0].record_id == "x"
    assert results[0].score == 1.0


def test_dimension_mismatch_raises() -> None:
    index = InMemoryVectorIndex(dimension=3)

    try:
        index.upsert(VectorRecord(record_id="bad", vector=[1.0, 2.0]))
        assert False, "expected DimensionMismatchError"
    except DimensionMismatchError:
        pass


def test_invalid_top_k_raises() -> None:
    index = InMemoryVectorIndex(dimension=2)
    index.upsert(VectorRecord(record_id="x", vector=[1.0, 0.0]))
    search = VectorSimilaritySearch(index)

    try:
        search.search([1.0, 0.0], top_k=0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "top_k" in str(exc)
