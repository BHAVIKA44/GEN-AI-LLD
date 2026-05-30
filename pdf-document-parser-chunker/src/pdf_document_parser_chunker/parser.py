from __future__ import annotations

from pypdf import PdfReader

from .models import ParsedDocument


class PyPDFParser:
    def parse(self, pdf_path: str) -> ParsedDocument:
        reader = PdfReader(pdf_path)
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")

        text = "\n".join(pages).strip()
        return ParsedDocument(source_path=pdf_path, text=text)
