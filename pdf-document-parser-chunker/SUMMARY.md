# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/pdf_document_parser_chunker/__init__.py`
- `src/pdf_document_parser_chunker/models.py`
- `src/pdf_document_parser_chunker/interfaces.py`
- `src/pdf_document_parser_chunker/parser.py`
- `src/pdf_document_parser_chunker/chunker.py`
- `src/pdf_document_parser_chunker/service.py`
- `tests/test_service.py`

# Main Abstractions

- `PDFParser`
- `Chunker`
- `DocumentParseAndChunkService`

# Design Choices

- Separate parsing and chunking responsibilities.
- Keep service orchestration minimal and testable.
- Use overlap-aware fixed word chunking for baseline quality.

# Technology Choices

- Used: `pypdf`
- Not used: LangChain/LangGraph (not necessary for this scope)

# GenAI-Specific Considerations

- Chunking is ready for embedding/RAG pipelines.
- Clear extension path to token-aware chunkers and metadata-aware chunks.

# Testing Strategy

- Unit tests via fake parser to avoid filesystem/PDF dependencies.
- Validation and empty-content scenarios covered.

# Extension Points

- OCR fallback for scanned PDFs.
- Token-based chunking with `tiktoken`.
- Page-aware chunk metadata and citation offsets.

# Known Tradeoffs

- Text-only PDF parsing.
- In-memory processing only.

# Final Interview Summary

This solution implements a clean PDF parse-and-chunk pipeline with clear boundaries and practical defaults, intentionally scoped for a 1-hour LLD round and easy extension into GenAI retrieval pipelines.
