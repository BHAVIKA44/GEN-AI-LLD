# Problem Statement

Implement cosine similarity, dot product, and Euclidean distance functions from scratch.

# Requirements

## Functional requirements
- Implement `dot_product(a, b)`.
- Implement `euclidean_distance(a, b)`.
- Implement `cosine_similarity(a, b)`.
- Validate input dimensions.

## Non-functional requirements
- Interview-sized, readable implementation.
- Deterministic and testable.

## Assumptions
- Input vectors are numeric and dense.
- Vectors must be non-empty and same dimension.

# Design Overview

Main components:
- `metrics.py` with pure functions.
- Shared dimension validation helper.

Data flow:
1. Validate vectors.
2. Compute metric using direct math formulas.

# Class / Module Design

- `metrics.py`: `dot_product`, `euclidean_distance`, `cosine_similarity`
- `__init__.py`: public exports

# Technology Selection Rationale

- Pure Python used.
  - Why: this is a math primitive problem and from-scratch implementation is expected.
- No LangChain/LangGraph.
  - Why: not relevant for low-level vector math utility.

# Error Handling

- Raises `ValueError` on empty vectors.
- Raises `ValueError` on dimension mismatch.
- Cosine similarity returns `0.0` if either vector norm is zero.

# Testing Strategy

- Known-value tests for all three metrics.
- Edge cases: zero vector, mismatch, empty vector.

# Tradeoffs

- No NumPy acceleration.
- No sparse vector optimization.

# How to Run

Install:
```bash
cd vector-metrics-from-scratch
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
