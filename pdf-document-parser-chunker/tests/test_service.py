from pdf_document_parser_chunker.chunker import FixedWordChunker
from pdf_document_parser_chunker.models import ParsedDocument
from pdf_document_parser_chunker.service import DocumentParseAndChunkService


class FakeParser:
    def parse(self, pdf_path: str) -> ParsedDocument:
        return ParsedDocument(
            source_path=pdf_path,
            text="one two three four five six seven eight nine ten",
        )


def test_service_parses_and_chunks() -> None:
    service = DocumentParseAndChunkService(
        parser=FakeParser(),
        chunker=FixedWordChunker(words_per_chunk=4, overlap_words=1),
    )

    chunks = service.run("sample.pdf")

    assert len(chunks) == 3
    assert chunks[0].text == "one two three four"
    assert chunks[1].text == "four five six seven"


def test_empty_text_returns_no_chunks() -> None:
    class EmptyParser:
        def parse(self, pdf_path: str) -> ParsedDocument:
            return ParsedDocument(source_path=pdf_path, text="")

    service = DocumentParseAndChunkService(
        parser=EmptyParser(),
        chunker=FixedWordChunker(words_per_chunk=5, overlap_words=1),
    )

    assert service.run("empty.pdf") == []


def test_invalid_path_raises() -> None:
    service = DocumentParseAndChunkService(
        parser=FakeParser(),
        chunker=FixedWordChunker(words_per_chunk=5, overlap_words=1),
    )

    try:
        service.run("  ")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "pdf_path" in str(exc)
