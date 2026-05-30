# Problem Statement

Implement semantic caching for LLM queries (cache responses for semantically similar queries).

# Requirements

## Functional requirements
- Cache LLM responses.
- Reuse cache for semantically similar queries.
- Support model-aware cache isolation.
- Support TTL expiration.
- Return hit/miss metadata.

## Non-functional requirements
- Interview-sized implementation.
- Deterministic tests without external services.
- Clear abstraction boundaries.

## Assumptions
- Semantic similarity is measured by cosine similarity over query embeddings.
- Fake embedding provider is acceptable for local tests.

# Design Overview

Main components:
- `SemanticCachedLLMService`: cache wrapper around LLM provider.
- `InMemorySemanticCache`: stores query embeddings + responses.
- `EmbeddingProvider` abstraction.
- `LLMProvider` abstraction.

Data flow:
1. Embed incoming query.
2. Find cached entry with same model and cosine similarity above threshold.
3. On hit: return cached answer.
4. On miss: call LLM, store new semantic cache entry with TTL.

# Class / Module Design

- `models.py`: query/answer/cache entry models
- `interfaces.py`: provider protocols
- `embeddings.py`: `FakeEmbeddings`
- `cache.py`: in-memory semantic cache
- `service.py`: orchestration service

# Technology Selection Rationale

- Pure Python: Used for baseline.
- LangChain/LangGraph: Not used.
  - Why: this is cache infrastructure logic, not orchestration/retrieval flow.
- Vector DB: Not used.
  - Why: 1-hour scope; in-memory list is sufficient.

# Error Handling

- Similarity threshold validation.
- Embedding dimension mismatch check.
- TTL <= 0 treated as no-store.

# Testing Strategy

- Similar-query cache hit behavior.
- Model-isolated cache behavior.
- TTL expiry behavior.

# Tradeoffs

- Brute-force semantic lookup O(n).
- Fake embeddings limit realism.
- No eviction policy besides TTL.

# How to Run

Install:
```bash
cd semantic-caching-llm-queries
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
