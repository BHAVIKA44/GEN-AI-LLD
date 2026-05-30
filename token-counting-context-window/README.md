# Problem Statement

Write code to implement token counting and context window management.

# Requirements

## Functional requirements
- Count tokens for text/messages.
- Manage a model context window with max token budget.
- Support reserving output tokens.
- Truncate conversation context to fit budget.

## Non-functional requirements
- Interview-scale and easy to explain.
- Deterministic behavior.
- Clear abstractions for tokenizer swapping.

## Assumptions
- Token counting can be approximate for baseline.
- Context prioritizes latest messages.

# Design Overview

Main components:
- `TokenCounter` interface.
- `SimpleWhitespaceTokenCounter` implementation.
- `ContextWindowManager` to fit messages within token budget.

Data flow:
1. Count tokens per message (role + content + small overhead).
2. Compute available input budget (`max_tokens - reserved_output_tokens`).
3. Keep latest messages that fit within budget.
4. Return kept messages + token usage metadata.

# Class / Module Design

- `models.py`: `ChatMessage`, `ContextBuildResult`
- `interfaces.py`: `TokenCounter`
- `tokenizer.py`: `SimpleWhitespaceTokenCounter`
- `context_manager.py`: `ContextWindowManager`

# Technology Selection Rationale

- Pure Python: Used.
  - Why: core logic is simple and interview-friendly.
- LangChain/LangGraph: Not used.
  - Why: this is a low-level utility, not orchestration/retrieval workflow.

# Error Handling

- Invalid max/reserved token config rejected.
- Empty text safely returns zero tokens.
- Context building always returns bounded token usage.

# Testing Strategy

- Token counting behavior.
- Context truncation with reserved output budget.
- Latest-message retention behavior.
- Invalid config validation.

# Tradeoffs

- Token counting is approximate, not model-specific exact.
- No role-priority policy customization beyond recency.

# How to Run

Install:
```bash
cd token-counting-context-window
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```

# Production Extension

For production, replace `SimpleWhitespaceTokenCounter` with model-specific tokenizers (e.g., `tiktoken`) to align exact token limits and costs.
