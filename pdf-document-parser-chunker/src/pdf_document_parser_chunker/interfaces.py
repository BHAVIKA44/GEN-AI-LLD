from __future__ import annotations

from typing import Protocol

from .models import ParsedDocument, TextChunk


class PDFParser(Protocol):
    def parse(self, pdf_path: str) -> ParsedDocument:
        ...


class Chunker(Protocol):
    def chunk(self, text: str) -> list[TextChunk]:
        ...
