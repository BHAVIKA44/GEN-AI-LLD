from __future__ import annotations

from .interfaces import Chunker, PDFParser
from .models import TextChunk


class DocumentParseAndChunkService:
    def __init__(self, parser: PDFParser, chunker: Chunker) -> None:
        self._parser = parser
        self._chunker = chunker

    def run(self, pdf_path: str) -> list[TextChunk]:
        if not pdf_path.strip():
            raise ValueError("pdf_path must not be empty")
        parsed = self._parser.parse(pdf_path)
        return self._chunker.chunk(parsed.text)
