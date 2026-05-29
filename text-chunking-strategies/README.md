# Problem Statement

Write code for different text chunking strategies (fixed-size, recursive, semantic).

# Requirements

## Functional requirements
- Implement fixed-size chunking.
- Implement recursive chunking based on separator hierarchy.
- Implement semantic chunking that groups related sentences.
- Add optional LangChain recursive chunking adapter.
- Return chunk identifiers and chunk text.

## Non-functional requirements
- Interview-friendly scope and readability.
- Extensible strategy design.
- Strong unit tests for core behavior.

## Assumptions
- In-memory processing is sufficient.
- Semantic chunking can be heuristic for this round.

# Design Overview

Main components:
- `TextChunk` model.
- `TextChunker` interface.
- `FixedSizeChunker`.
- `RecursiveChunker`.
- `SemanticChunker`.
- `LangChainRecursiveChunker` (optional adapter).

Data flow:
1. Input text is passed to a selected strategy.
2. Strategy transforms text into `TextChunk` list.
3. Each chunk carries strategy-prefixed `chunk_id`.

# Class / Module Design

- `models.py`: `TextChunk`
- `interfaces.py`: `TextChunker` protocol
- `fixed_size.py`: character-based chunking with overlap
- `recursive.py`: separator-aware recursive splitting
- `semantic.py`: sentence grouping by keyword-overlap heuristic
- `langchain_adapter.py`: optional wrapper over LangChain `RecursiveCharacterTextSplitter`

# Technology Selection Rationale

- LangChain: Used optionally.
  - Why: adapter improves GenAI realism while keeping pure Python core strategies.
  - Tradeoff: optional dependency and extra adapter layer.
- LangGraph: Not used.
  - Why: no workflow/state orchestration required.
- RAG/Agents/Vector DB: Not used.
  - Why: problem is text chunking only.

# Error Handling

- Validate chunking parameters.
- Empty/whitespace input returns empty list.
- LangChain adapter raises clear import error if optional dependency missing.

# Testing Strategy

- Fixed-size behavior with overlap.
- Recursive max-length constraints.
- Semantic topic-shift behavior.
- Empty input handling.
- Optional LangChain adapter test (graceful if dependency absent).

# Tradeoffs

- Semantic chunking is heuristic, not embedding-based.
- Pure Python strategies are character/sentence-oriented.

# How to Run

Install core:
```bash
cd text-chunking-strategies
python3 -m pip install -e ".[dev]"
```

Install with optional LangChain adapter dependency:
```bash
python3 -m pip install -e ".[dev,langchain]"
```

Run tests:
```bash
python3 -m pytest
```

# Production Extension

For production GenAI systems, prefer tokenizer-aware chunking (`tiktoken` or model-native tokenizers) so chunk sizes align with model context windows and cost controls.
