# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/prompt_injection_detection/__init__.py`
- `src/prompt_injection_detection/models.py`
- `src/prompt_injection_detection/interfaces.py`
- `src/prompt_injection_detection/detector.py`
- `src/prompt_injection_detection/handler.py`
- `tests/test_injection_detection.py`

# Main Abstractions

- `InjectionDetector`
- `RuleBasedPromptInjectionDetector`
- `PromptInjectionGuard`

# Design Choices

- Separate detection from policy actioning.
- Use additive risk signals for transparency.
- Keep threshold policy configurable.

# Technology Choices

- Pure Python baseline.
- No external guardrail service required.

# GenAI-Specific Considerations

- Detects attempts to override system/developer instructions.
- Explicitly checks hidden-prompt exfiltration patterns.

# Testing Strategy

- Unit tests for allow/warn/block behaviors and empty input handling.

# Extension Points

- Add embedding/LLM classifier for semantic detection.
- Add multilingual rules.
- Connect to central policy/audit logging.

# Known Tradeoffs

- Heuristic detector quality is limited.
- Not adversarially robust by itself.

# Final Interview Summary

This solution provides a practical first-line defense against prompt injection with transparent signals and configurable policy actions, intentionally scoped for a 1-hour LLD interview while leaving clear hardening paths.
