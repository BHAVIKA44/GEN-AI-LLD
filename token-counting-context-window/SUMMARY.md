# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/token_counting_context_window/__init__.py`
- `src/token_counting_context_window/models.py`
- `src/token_counting_context_window/interfaces.py`
- `src/token_counting_context_window/tokenizer.py`
- `src/token_counting_context_window/context_manager.py`
- `tests/test_context_manager.py`

# Main Abstractions

- `TokenCounter`
- `ContextWindowManager`
- `ChatMessage` and `ContextBuildResult`

# Design Choices

- Keep tokenizer pluggable.
- Enforce explicit output-token reservation.
- Recency-based truncation for simple chat behavior.

# Technology Choices

- Pure Python baseline.
- No framework dependency for this primitive.

# GenAI-Specific Considerations

- Context-window budgeting is explicit and inspectable.
- Ready for model-specific tokenization swap.

# Testing Strategy

- Unit tests for counting, truncation, and config validation.

# Extension Points

- Role-aware retention (system > recent user > older history).
- Summary compression before truncation.
- Exact tokenizer adapters (`tiktoken`, sentencepiece).

# Known Tradeoffs

- Approximate token counting.
- No adaptive summarization built in.

# Final Interview Summary

This solution provides a clean token budgeting utility for chat contexts with pluggable token counting and predictable truncation behavior, appropriately scoped for a 1-hour LLD round.
