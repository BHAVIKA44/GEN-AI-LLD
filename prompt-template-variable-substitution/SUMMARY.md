# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/prompt_template_variable_substitution/__init__.py`
- `src/prompt_template_variable_substitution/models.py`
- `src/prompt_template_variable_substitution/errors.py`
- `src/prompt_template_variable_substitution/template_engine.py`
- `tests/test_template_engine.py`

# Main Abstractions

- `PromptTemplate`
- `PromptTemplateEngine`
- Custom typed errors

# Design Choices

- Minimal, explicit regex-based parsing.
- Strict vs lenient rendering mode for production flexibility.
- Separate validation from substitution logic.

# Technology Choices

- Pure Python for this focused primitive.
- No heavy framework dependency needed.

# GenAI-Specific Considerations

- Prompt templates are versioned via model fields (`name`, `version`).
- Missing-variable behavior is explicit and predictable.

# Testing Strategy

- Positive and negative rendering tests.
- Validation and required-variable extraction tests.

# Extension Points

- Template registry/storage backend.
- Default values and optional placeholders.
- Integration adapter to LangChain `PromptTemplate`.

# Known Tradeoffs

- Limited syntax by design.
- No advanced templating features.

# Final Interview Summary

This solution implements a clean prompt templating core with validation and variable substitution semantics that are practical for GenAI systems, while staying intentionally compact for a 1-hour LLD round.
