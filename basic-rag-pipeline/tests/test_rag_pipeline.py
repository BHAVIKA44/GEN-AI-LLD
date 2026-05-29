from basic_rag_pipeline.factory import build_default_rag


def test_index_and_answer() -> None:
    indexer, rag = build_default_rag()
    count = indexer.index_texts(
        [
            "RAG combines retrieval and generation for grounded answers.",
            "FAISS is a local vector index used for similarity search.",
        ]
    )

    result = rag.answer("What is RAG?", top_k=2)

    assert count >= 2
    assert len(result.sources) == 2
    assert isinstance(result.answer, str)
    assert result.answer


def test_empty_query_raises() -> None:
    _, rag = build_default_rag()
    try:
        rag.answer("  ")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "query" in str(exc)


def test_top_k_validation() -> None:
    _, rag = build_default_rag()
    try:
        rag.answer("What is FAISS?", top_k=0)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "top_k" in str(exc)
