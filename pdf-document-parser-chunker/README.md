# Problem Statement

Build a basic document parser that extracts text from PDFs and splits it into chunks.

# Requirements

## Functional requirements
- Read text from a PDF file.
- Combine extracted page text.
- Split text into chunks.
- Return chunked output for downstream usage.

## Non-functional requirements
- Interview-friendly scope.
- Clean parser/chunker separation.
- Testable without real PDF dependency in unit tests.

## Assumptions
- Text-based PDFs (not OCR image-only PDFs).
- Word-based chunking is sufficient for baseline.

# Design Overview

Main components:
- `PyPDFParser`: extracts text from PDF pages.
- `FixedWordChunker`: splits text using configurable size and overlap.
- `DocumentParseAndChunkService`: orchestrates parse + chunk workflow.

Data flow:
1. Input PDF path sent to parser.
2. Parser returns consolidated raw text.
3. Chunker splits text into chunk list.
4. Service returns chunks.

# Class / Module Design

- `models.py`: `ParsedDocument`, `TextChunk`
- `interfaces.py`: `PDFParser`, `Chunker`
- `parser.py`: `PyPDFParser`
- `chunker.py`: `FixedWordChunker`
- `service.py`: orchestration service

# Technology Selection Rationale

- `pypdf`: Used.
  - Why: lightweight, common Python PDF text extraction library.
  - Tradeoff: OCR support is limited for scanned PDFs.
- LangChain: Not used.
  - Why: this problem is a small parser/chunker primitive; direct implementation is faster for 1-hour round.
- LangGraph: Not used.
  - Why: no multi-step stateful orchestration needed.

# Error Handling

- Empty `pdf_path` validation.
- Chunker constructor validates size/overlap constraints.
- Missing page text handled with empty fallback.

# Testing Strategy

- Service behavior with fake parser and deterministic chunking.
- Empty text path.
- Invalid input validation.

# Tradeoffs

- No OCR pipeline.
- No token-aware chunking.
- No metadata extraction (title/author/page offsets).

# How to Run

Install:
```bash
cd pdf-document-parser-chunker
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
