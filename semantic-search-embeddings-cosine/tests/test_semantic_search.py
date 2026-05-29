from semantic_search_embeddings_cosine.models import SearchDocument
from semantic_search_embeddings_cosine.search import InMemorySemanticSearch


def test_index_returns_count() -> None:
    service = InMemorySemanticSearch()
    count = service.index(
        [
            SearchDocument(doc_id="1", text="Python is used for backend APIs"),
            SearchDocument(doc_id="2", text=""),
        ]
    )
    assert count == 1


def test_semantic_search_returns_ranked_hits() -> None:
    service = InMemorySemanticSearch()
    service.index(
        [
            SearchDocument(doc_id="1", text="Neural networks for image classification"),
            SearchDocument(doc_id="2", text="Vector similarity search with embeddings"),
            SearchDocument(doc_id="3", text="Cooking recipe for pasta"),
        ]
    )

    hits = service.search("How do embeddings help semantic search?", top_k=2)

    assert len(hits) == 2
    assert hits[0].score >= hits[1].score


def test_empty_query_raises() -> None:
    service = InMemorySemanticSearch()
    service.index([SearchDocument(doc_id="1", text="sample")])

    try:
        service.search("   ")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "query" in str(exc)


def test_top_k_validation() -> None:
    service = InMemorySemanticSearch()
    service.index([SearchDocument(doc_id="1", text="sample")])

    try:
        service.search("sample", top_k=0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "top_k" in str(exc)
