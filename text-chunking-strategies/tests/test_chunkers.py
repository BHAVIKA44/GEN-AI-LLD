from text_chunking_strategies.fixed_size import FixedSizeChunker
from text_chunking_strategies.recursive import RecursiveChunker
from text_chunking_strategies.semantic import SemanticChunker


def test_fixed_size_chunking_with_overlap() -> None:
    chunker = FixedSizeChunker(chunk_size=10, overlap=2)
    chunks = chunker.chunk("abcdefghijklmnopqrstuvwxyz")

    assert len(chunks) == 3
    assert chunks[0].text == "abcdefghij"
    assert chunks[1].text.startswith("ijkl")


def test_recursive_chunking_respects_max_chars() -> None:
    text = "Paragraph one is short.\n\nParagraph two contains more words and should be separated carefully."
    chunker = RecursiveChunker(max_chars=45)

    chunks = chunker.chunk(text)

    assert len(chunks) >= 2
    assert all(len(c.text) <= 45 for c in chunks)


def test_semantic_chunking_splits_topic_shift() -> None:
    text = (
        "Python code uses classes and methods. "
        "Inheritance helps software design. "
        "Football teams train daily for matches. "
        "Goalkeepers defend the net strongly."
    )
    chunker = SemanticChunker(max_sentences_per_chunk=3)

    chunks = chunker.chunk(text)

    assert len(chunks) >= 2
    assert "Python" in chunks[0].text


def test_empty_text_returns_no_chunks() -> None:
    assert FixedSizeChunker().chunk("   ") == []
    assert RecursiveChunker().chunk("\n") == []
    assert SemanticChunker().chunk("") == []


def test_langchain_recursive_chunker_optional() -> None:
    try:
        from text_chunking_strategies.langchain_adapter import LangChainRecursiveChunker
    except Exception:
        return

    try:
        chunker = LangChainRecursiveChunker(chunk_size=30, chunk_overlap=5)
    except ImportError:
        return

    chunks = chunker.chunk("This is a sentence. This is another sentence. And one more sentence.")
    assert len(chunks) >= 2
