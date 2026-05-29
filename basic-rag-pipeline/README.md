# Problem Statement

Implement a basic RAG pipeline using an embedding model and a vector database.

# Requirements

## Functional requirements
- Ingest documents.
- Split into chunks.
- Embed and index chunks in a vector DB.
- Retrieve top-k relevant chunks.
- Generate answer using retrieved context.
- Return answer with sources.

## Non-functional requirements
- Interview-friendly (1 hour).
- Clean abstractions and dependency injection.
- Tests run offline without API keys or external services.

## Assumptions
- Local FAISS index is sufficient.
- Deterministic fake embedding/model are acceptable for tests.

# Design Overview

Components:
- `LangChainFaissIndexer`: uses LangChain text splitter + FAISS vector store.
- `LangChainRAGService`: retrieval + prompt template + chat model invocation.
- `FakeEmbeddings`: deterministic local embedding adapter.
- `OfflineContextEchoModel`: deterministic local chat model adapter.
- `create_app` (FastAPI): minimal API for ingest/query endpoints.

Data flow:
1. Texts -> splitter -> chunk docs -> FAISS indexing.
2. Query -> similarity search -> prompt template with context -> chat model -> answer + sources.

# Class / Module Design

- `interfaces.py`: `KnowledgeIndexer`, `QueryAnsweringService`
- `models.py`: `SourceChunk`, `RAGResult`
- `langchain_adapters.py`: framework-backed implementations
- `factory.py`: dependency wiring
- `api.py`: optional API boundary

# Technology Selection Rationale

- LangChain: Used.
  - Why: provides splitters, prompt templates, model abstraction, and vector store integration.
  - Tradeoff: extra dependency weight.
- LangGraph: Not used.
  - Why: basic RAG is a linear flow; no workflow graph/agent orchestration needed.
  - Tradeoff: retry/HITL flows are future additions.
- Vector DB: Used via FAISS.
  - Why: modern local vector store for interview realism.
  - Tradeoff: in-memory/local, not distributed.
- FastAPI + Pydantic: Used (minimal API layer).
  - Why: realistic service boundary and validation.
  - Tradeoff: more files than pure library approach.
- Evaluation/Observability/Guardrails/Caching: Not implemented in code.
  - Why: out-of-scope for 1 hour; documented as extension points.

# Error Handling

- Rejects empty query.
- Rejects invalid `top_k`.
- Skips blank input texts.
- Deterministic fallback text when context is missing.

# Testing Strategy

- Unit tests for indexing/retrieval/answering behavior.
- Validation tests for error paths.
- Fully offline tests using fake providers.

# Tradeoffs

- No external LLM or production embedding provider.
- No persistence beyond local FAISS process state.
- No reranking/guardrails/evaluation pipeline.

# How to Run

Install:
```bash
cd basic-rag-pipeline
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
