# Problem Statement

Implement a simple re-ranker for search results.

# Requirements

## Functional requirements
- Accept query and initial search results.
- Compute rerank score per result.
- Sort by rerank score descending.
- Optionally return top-k.

## Non-functional requirements
- Interview-scale implementation.
- Deterministic and testable behavior.
- Extensible scoring strategy.

## Assumptions
- Initial results include a base relevance score.
- Query/result text are available for lexical overlap scoring.

# Design Overview

Main components:
- `SearchResult` input model.
- `RankedResult` output model.
- `SimpleReRanker` scorer and sorter.

Data flow:
1. Parse query terms.
2. Compute overlap score for each result.
3. Combine base score + overlap with configurable weights.
4. Sort and optionally trim to top-k.

# Class / Module Design

- `models.py`: search models
- `interfaces.py`: `ReRanker` protocol
- `reranker.py`: concrete re-ranking strategy

# Technology Selection Rationale

- LangChain/LangGraph: Not used.
  - Why: reranking primitive is simple and clearer as a standalone module.
  - Tradeoff: no direct framework integration in baseline.
- Vector DB/LLM judge: Not used.
  - Why: this is post-retrieval rerank logic only.

# Error Handling

- Reject empty query.
- Reject invalid `top_k`.
- Validate reranker weights.

# Testing Strategy

- Overlap-aware rank promotion.
- top-k trimming.
- validation errors.

# Tradeoffs

- Lexical overlap heuristic only.
- No semantic cross-encoder reranking.
- No diversity/novelty balancing.

# How to Run

Install:
```bash
cd simple-search-reranker
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
