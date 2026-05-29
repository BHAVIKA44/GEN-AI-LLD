# Problem Statement

Implement a retry mechanism with exponential backoff for LLM API calls.

# Requirements

## Functional requirements
- Retry transient LLM call failures.
- Stop immediately for non-retryable errors.
- Use exponential backoff between retries.
- Cap max delay.
- Support optional jitter.

## Non-functional requirements
- Interview-sized implementation.
- Deterministic unit tests.
- Extensible error handling.

## Assumptions
- Errors are classified into retryable and non-retryable.
- Sync operation wrapper is sufficient for this round.

# Design Overview

Main components:
- `RetryConfig`: retry policy parameters.
- `RetryExecutor`: executes operation with retry/backoff policy.
- Error types for classification and terminal failure.

Data flow:
1. Execute operation.
2. On retryable error, sleep with backoff (and jitter), then retry.
3. On non-retryable error, fail fast.
4. On exhausted attempts, raise `RetryExhaustedError`.

# Class / Module Design

- `models.py`: `RetryConfig`
- `errors.py`: `RetryableLLMError`, `NonRetryableLLMError`, `RetryExhaustedError`
- `retry.py`: `RetryExecutor`

# Technology Selection Rationale

- LangChain/LangGraph: Not used.
  - Why: this is transport reliability logic and is cleaner as a focused utility.
- External queues/workflows: Not used.
  - Why: out of scope for 1-hour coding round.

# Error Handling

- Config validation on initialization.
- Non-retryable failures propagate immediately.
- Retry exhaustion wraps the last retryable error.

# Testing Strategy

- Retries then success path.
- Exhausted retries path.
- Fail-fast non-retryable path.
- Invalid config validation.

# Tradeoffs

- Sync API only (no async wrapper yet).
- No retry budget/timeout deadline tracking.
- No circuit breaker integration.

# How to Run

Install:
```bash
cd retry-exponential-backoff-llm
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
