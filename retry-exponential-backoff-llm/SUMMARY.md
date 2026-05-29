# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/retry_exponential_backoff_llm/__init__.py`
- `src/retry_exponential_backoff_llm/errors.py`
- `src/retry_exponential_backoff_llm/models.py`
- `src/retry_exponential_backoff_llm/retry.py`
- `tests/test_retry.py`

# Main Abstractions

- `RetryConfig`
- `RetryExecutor`
- Typed retry error classes

# Design Choices

- Clean separation of policy (config) and execution (executor).
- Typed error model for deterministic retry decisions.
- Injected sleep function for fast testability.

# Technology Choices

- Pure Python utility implementation.
- No framework overhead for this scoped reliability concern.

# GenAI-Specific Considerations

- Models common LLM failure modes (rate-limit/timeouts vs bad request).
- Backoff and jitter help reduce coordinated retry spikes.

# Testing Strategy

- Covers success, exhaustion, fail-fast, and config validation.
- No real waits or external API calls.

# Extension Points

- Async retry executor.
- Deadline-aware cancellation.
- Circuit breaker and observability hooks.

# Known Tradeoffs

- No distributed retry coordination.
- No built-in metrics exporter.

# Final Interview Summary

This solution provides a practical, production-aware retry core for LLM API calls with exponential backoff and clear error semantics, while staying intentionally compact for a 1-hour LLD interview.
