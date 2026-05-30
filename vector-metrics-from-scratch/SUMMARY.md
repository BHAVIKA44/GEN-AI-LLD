# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/vector_metrics_from_scratch/__init__.py`
- `src/vector_metrics_from_scratch/metrics.py`
- `tests/test_metrics.py`

# Main Abstractions

- Pure metric functions with shared validation

# Design Choices

- Kept functions stateless and reusable.
- Added explicit validation and edge-case handling.

# Technology Choices

- Pure Python baseline for from-scratch requirement.

# GenAI-Specific Considerations

- These metrics are core primitives for embeddings and retrieval systems.

# Testing Strategy

- Golden-value numeric tests and failure-path tests.

# Extension Points

- NumPy vectorization.
- Sparse vector support.
- Batch metric operations.

# Known Tradeoffs

- Not optimized for large-scale numeric workloads.

# Final Interview Summary

This solution provides clean, correct implementations of three foundational vector similarity/distance metrics with strong validation and tests, scoped appropriately for a 1-hour LLD round.
