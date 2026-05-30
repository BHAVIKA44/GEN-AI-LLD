# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/semantic_caching_llm_queries/__init__.py`
- `src/semantic_caching_llm_queries/models.py`
- `src/semantic_caching_llm_queries/interfaces.py`
- `src/semantic_caching_llm_queries/embeddings.py`
- `src/semantic_caching_llm_queries/cache.py`
- `src/semantic_caching_llm_queries/service.py`
- `tests/test_semantic_cache.py`

# Main Abstractions

- `EmbeddingProvider`
- `LLMProvider`
- `InMemorySemanticCache`
- `SemanticCachedLLMService`

# Design Choices

- Cosine-similarity threshold for semantic hits.
- Cache entries include query embedding and model identity.
- TTL-based expiration.

# Technology Choices

- Pure Python baseline.
- No external vector DB in interview scope.

# GenAI-Specific Considerations

- Reduces repeated LLM calls for paraphrased queries.
- Model-specific isolation avoids cross-model leakage.

# Testing Strategy

- Hit/miss behavior for similar queries.
- Model isolation verification.
- TTL expiry verification.

# Extension Points

- Replace in-memory list with FAISS/Redis/Vector DB backend.
- Add semantic+exact hybrid keying.
- Add score margin checks before serving cached response.

# Known Tradeoffs

- Linear scan lookup.
- Embedding quality determines hit accuracy.

# Final Interview Summary

This solution implements a practical semantic cache for LLM queries using embeddings and cosine similarity with TTL and model isolation, kept intentionally compact for a 1-hour LLD interview.
