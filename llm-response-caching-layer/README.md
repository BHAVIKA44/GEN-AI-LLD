# Problem Statement

Implement a caching layer for LLM responses.

# Requirements

## Functional requirements
- Cache LLM responses by request key.
- Return cached responses on repeated requests.
- Support TTL expiration.
- Distinguish cache hit vs miss.

## Non-functional requirements
- Interview-size and easy to explain.
- Pluggable cache/provider interfaces.
- Deterministic tests without external services.

## Assumptions
- Request uniqueness is based on prompt + model + temperature.
- In-memory cache is sufficient for baseline.

# Design Overview

Main components:
- `CachedLLMService`: cache-aside wrapper around LLM provider.
- `InMemoryTTLCache`: in-memory cache with expiration.
- `LLMRequest` / `LLMResponse` models.

Data flow:
1. Build cache key from request fields.
2. Check cache.
3. On hit: return cached response.
4. On miss: call provider, cache result, return response.

# Class / Module Design

- `models.py`: request/response/cache entry
- `interfaces.py`: `LLMProvider`, `CacheStore`
- `cache.py`: `InMemoryTTLCache`
- `service.py`: `CachedLLMService`

# Technology Selection Rationale

- Pure Python: Used.
  - Why: keeps focus on caching logic for 1-hour LLD.
- Redis/External cache: Not used in code.
  - Why: out of scope; interface allows swap later.
- LangChain/LangGraph: Not used.
  - Why: this is infra utility, not orchestration flow.

# Error Handling

- Invalid negative TTL rejected.
- TTL <= 0 results in no-op caching behavior.
- Expired entries are evicted lazily on `get`.

# Testing Strategy

- Cache hit avoids second provider call.
- TTL expiration triggers fresh provider call.
- Different requests produce cache misses.

# Tradeoffs

- In-memory single-process cache only.
- No cache size limit/eviction policy.
- No per-tenant namespace isolation.

# How to Run

Install:
```bash
cd llm-response-caching-layer
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
