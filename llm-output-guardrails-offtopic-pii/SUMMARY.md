# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/llm_output_guardrails_offtopic_pii/__init__.py`
- `src/llm_output_guardrails_offtopic_pii/models.py`
- `src/llm_output_guardrails_offtopic_pii/interfaces.py`
- `src/llm_output_guardrails_offtopic_pii/checks.py`
- `src/llm_output_guardrails_offtopic_pii/guardrails.py`
- `tests/test_guardrails.py`

# Main Abstractions

- `OutputCheck`
- `OffTopicCheck`
- `PIICheck`
- `OutputGuardrails`

# Design Choices

- Modular checks + centralized policy handler.
- Signal-level transparency with risk scoring.
- Redaction-before-block policy tiering.

# Technology Choices

- Pure Python baseline for deterministic behavior.

# GenAI-Specific Considerations

- Protects output quality (topic relevance) and privacy (PII leakage).
- Easily composable with other safety checks.

# Testing Strategy

- Unit tests for pass/redact/block scenarios.

# Extension Points

- Semantic off-topic classifier.
- Additional PII entities (cards, addresses, IDs).
- Policy logging and audit hooks.

# Known Tradeoffs

- Regex + lexical checks can miss nuanced cases.

# Final Interview Summary

This solution implements a practical output guardrail layer with off-topic and PII checks, producing clear policy actions and keeping architecture compact and extensible for a 1-hour LLD interview.
