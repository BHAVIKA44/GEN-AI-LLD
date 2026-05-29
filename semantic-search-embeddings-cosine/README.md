# Problem Statement

Implement semantic search using embeddings and cosine similarity.

# Requirements

## Functional requirements
- Index input documents.
- Generate embeddings for documents and query.
- Compute cosine similarity between query embedding and document embeddings.
- Return top-k ranked results.

## Non-functional requirements
- Keep implementation small and interview-friendly.
- Use clean interfaces and dependency injection.
- Run tests offline without API keys/external services.

## Assumptions
- In-memory index is sufficient.
- Deterministic fake embeddings are acceptable in interview environment.

# Design Overview

Main components:
- `InMemorySemanticSearch`: core indexing and search service.
- `EmbeddingProvider` interface.
- `FakeEmbeddings` adapter (LangChain `Embeddings` compatible).
- `IndexedRow` internal storage model.

Data flow:
1. Documents -> embedding provider -> in-memory indexed rows.
2. Query -> query embedding -> cosine scores against rows -> sorted top-k hits.

# Class / Module Design

- `models.py`: `SearchDocument`, `SearchHit`
- `interfaces.py`: `EmbeddingProvider`, `SemanticSearchService`
- `embeddings.py`: `FakeEmbeddings`
- `index.py`: `IndexedRow`
- `search.py`: `InMemorySemanticSearch`

# Technology Selection Rationale

- LangChain: Used minimally (`langchain-core` embeddings interface).
  - Why: modern GenAI compatibility and easy provider swap later.
  - Tradeoff: small dependency overhead.
- LangGraph: Not used.
  - Why: no workflow/state-machine; this is a single linear similarity operation.
- RAG/Agents/Vector DB frameworks: Not used.
  - Why: problem is semantic search core, not full RAG agent system.
- Caching/Guardrails/Evaluation/Observability: Not used.
  - Why: out of scope for 1-hour basic implementation.

# Error Handling

- Reject empty query.
- Reject invalid top_k.
- Ignore empty documents during indexing.
- Validate embedding dimension consistency in cosine function.

# Testing Strategy

- Index count behavior.
- Ranked retrieval behavior.
- Empty query validation.
- top_k validation.

# Tradeoffs

- In-memory storage only.
- No approximate nearest neighbor index optimization.
- Fake embeddings instead of production model provider.

# How to Run

Install:
```bash
cd semantic-search-embeddings-cosine
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
