from simple_search_reranker.models import SearchResult
from simple_search_reranker.reranker import SimpleReRanker


def test_rerank_promotes_overlap() -> None:
    reranker = SimpleReRanker(base_weight=0.5, overlap_weight=0.5)
    results = [
        SearchResult(doc_id="a", text="vector database indexing", base_score=0.9),
        SearchResult(doc_id="b", text="semantic search with embeddings", base_score=0.7),
    ]

    ranked = reranker.rerank("semantic embeddings", results)

    assert ranked[0].doc_id == "b"
    assert ranked[0].rerank_score >= ranked[1].rerank_score


def test_top_k_limits_results() -> None:
    reranker = SimpleReRanker()
    results = [
        SearchResult(doc_id="1", text="a", base_score=0.1),
        SearchResult(doc_id="2", text="b", base_score=0.2),
        SearchResult(doc_id="3", text="c", base_score=0.3),
    ]

    ranked = reranker.rerank("query", results, top_k=2)

    assert len(ranked) == 2


def test_empty_query_raises() -> None:
    reranker = SimpleReRanker()
    try:
        reranker.rerank("   ", [])
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "query" in str(exc)
