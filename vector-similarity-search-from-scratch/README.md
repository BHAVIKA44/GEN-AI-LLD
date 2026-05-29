# Problem Statement

Build a simple vector similarity search from scratch.

# Requirements

## Functional requirements
- Store vectors in an index.
- Support insert/upsert by record ID.
- Compute cosine similarity between query and stored vectors.
- Return top-k ranked results.

## Non-functional requirements
- Simple, interview-friendly implementation.
- Clean separation between index, similarity function, and search service.
- Deterministic tests without external dependencies.

## Assumptions
- In-memory index is sufficient.
- All vectors are dense float vectors with fixed dimension.

# Design Overview

Main components:
- `InMemoryVectorIndex`: stores `VectorRecord` objects with dimension validation.
- `cosine_similarity`: core scoring primitive.
- `VectorSimilaritySearch`: query-time ranking over indexed records.

Data flow:
1. Records are upserted into the index.
2. Query vector is validated and compared with each record.
3. Scores are sorted descending and top-k returned.

# Class / Module Design

- `models.py`: `VectorRecord`, `SearchResult`
- `errors.py`: `DimensionMismatchError`
- `index.py`: in-memory index and dimension checks
- `similarity.py`: cosine similarity implementation
- `search.py`: top-k ranking logic

# Technology Selection Rationale

- LangChain/LangGraph: Not used.
  - Why: problem explicitly asks for from-scratch vector similarity core.
  - Tradeoff: no built-in vector store integrations.
- External vector DB: Not used.
  - Why: from-scratch requirement and 1-hour scope.
  - Tradeoff: no ANN optimization or persistence.

# Error Handling

- Invalid index dimension rejected.
- Query/record dimension mismatch raises `DimensionMismatchError`.
- Invalid `top_k` rejected.

# Testing Strategy

- Ranking correctness for known vectors.
- Upsert replacement behavior.
- Dimension mismatch errors.
- Invalid `top_k` validation.

# Tradeoffs

- Brute-force scan (O(n*d)) instead of ANN.
- In-memory only.
- No metadata filters or hybrid retrieval.

# How to Run

Install:
```bash
cd vector-similarity-search-from-scratch
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
