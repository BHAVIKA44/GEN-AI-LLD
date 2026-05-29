# Problem Statement

Implement streaming responses for an LLM API.

# Requirements

## Functional requirements
- Expose non-streaming text generation endpoint.
- Expose streaming endpoint for token-by-token output.
- Return well-formed stream completion signal.
- Keep provider behind interface for easy swapping.

## Non-functional requirements
- Interview-sized codebase.
- Offline testability (no external API keys).
- Clear API and service separation.

## Assumptions
- SSE (`text/event-stream`) is an acceptable streaming transport.
- Tokens can be approximated as whitespace-split chunks in fake provider.

# Design Overview

Main components:
- `LLMProvider` interface (`generate`, `stream_generate`).
- `FakeStreamingLLMProvider` deterministic local provider.
- `LLMService` for orchestration and SSE formatting.
- FastAPI app exposing `/generate` and `/generate/stream`.

Data flow:
1. API receives prompt.
2. Service calls provider.
3. Streaming endpoint emits SSE `token` events and final `done` event.

# Class / Module Design

- `models.py`: request/response schemas
- `interfaces.py`: provider protocol
- `providers.py`: fake streaming provider
- `service.py`: generation + SSE event framing
- `api.py`: FastAPI routes

# Technology Selection Rationale

- FastAPI + Pydantic: Used.
  - Why: practical and clean API boundary for LLM service patterns.
- LangChain/LangGraph: Not used.
  - Why: this problem is API streaming transport; framework orchestration is unnecessary here.
- SSE streaming: Used.
  - Why: simple, browser-friendly, and interview-friendly for token streams.

# Error Handling

- Request validation handled by Pydantic (`prompt` required, non-empty).
- Streaming always emits final `done` event after token stream completion.
- Provider errors can be wrapped in service layer in future extension.

# Testing Strategy

- Async test for standard `/generate` response.
- Async test for `/generate/stream` token events and terminal `done` event.
- Tests run fully offline against ASGI app.

# Tradeoffs

- Fake provider used instead of real LLM.
- No auth/rate limiting/timeout policies.
- No backpressure/cancellation handling beyond basic async generator behavior.

# How to Run

Install:
```bash
cd llm-api-streaming-responses
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```

Run API locally:
```bash
uvicorn llm_api_streaming_responses.api:create_app --factory --reload
```
