# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/basic_rag_pipeline/__init__.py`
- `src/basic_rag_pipeline/models.py`
- `src/basic_rag_pipeline/interfaces.py`
- `src/basic_rag_pipeline/langchain_adapters.py`
- `src/basic_rag_pipeline/factory.py`
- `src/basic_rag_pipeline/api.py`
- `tests/test_rag_pipeline.py`

# Main Abstractions

- `KnowledgeIndexer`
- `QueryAnsweringService`
- Adapter implementations using LangChain + FAISS

# Design Choices

- Use modern GenAI primitives instead of hand-rolled chunker/retriever/prompt logic.
- Keep framework dependency behind project-specific interfaces.
- Add minimal FastAPI boundary for realistic API exposure.

# Technology Choices

- Used: LangChain, FAISS, FastAPI, Pydantic.
- Not used: LangGraph (not required for linear basic RAG).

# GenAI-Specific Considerations

- Prompt template included explicitly.
- Retrieval done with vector similarity search.
- Source attribution returned with scores.
- Fake model/providers keep tests deterministic and offline.

# Testing Strategy

- Covers happy-path ingest + answer.
- Covers invalid query and invalid `top_k`.
- No external service dependencies.

# Extension Points

- Swap fake embeddings with managed embedding provider.
- Swap offline model with real chat model adapter.
- Add LangGraph if workflow expands to retries/tooling/HITL.
- Add observability (LangSmith/Langfuse) and eval tooling (Ragas/DeepEval).

# Known Tradeoffs

- Simplified answer generation.
- No production-scale persistence and ops.
- No advanced guardrails/caching/background jobs.

# Final Interview Summary

This solution uses modern GenAI tooling where it matters (splitter, vector retrieval, prompting, API boundary) while preserving clean LLD principles: interfaces, dependency injection, separation of concerns, and offline testability. It remains intentionally compact for a 1-hour interview.
