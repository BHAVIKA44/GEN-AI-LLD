# Problem Statement

Implement a prompt template system with variable substitution.

# Requirements

## Functional requirements
- Define prompt templates with named placeholders.
- Substitute runtime variables into template.
- Support validation of template syntax.
- Support strict mode (fail on missing variables).
- Support lenient mode (leave unresolved placeholders).

## Non-functional requirements
- Interview-friendly and easy to explain.
- Clean module boundaries.
- Deterministic tests without external services.

## Assumptions
- Placeholder syntax is `{{ variable_name }}`.
- Variables are scalar values (`str`, `int`, `float`).

# Design Overview

Main components:
- `PromptTemplate` data model.
- `PromptTemplateEngine` for validation and rendering.
- Custom errors for validation and missing variables.

Data flow:
1. Validate template syntax.
2. Extract required variables from template.
3. Render by substituting provided variables.
4. Raise or preserve placeholders based on strict/lenient mode.

# Class / Module Design

- `models.py`: `PromptTemplate`
- `errors.py`: `TemplateValidationError`, `MissingVariableError`
- `template_engine.py`: parse, validate, render logic

# Technology Selection Rationale

- LangChain: Not used.
  - Why: this is a focused template engine primitive; direct implementation is faster and clearer for 1-hour LLD.
  - Tradeoff: fewer built-in integrations out of the box.
- LangGraph: Not used.
  - Why: no multi-step workflow or state transitions.
- RAG/Agents/Vector DB: Not used.
  - Why: not part of this problem scope.

# Error Handling

- Empty template rejected.
- Unbalanced braces rejected.
- Invalid variable names rejected.
- Missing required variables raise `MissingVariableError` in strict mode.

# Testing Strategy

- Successful substitution path.
- Strict-mode missing variable failure.
- Lenient-mode unresolved placeholder behavior.
- Required variable extraction.
- Invalid syntax validation.

# Tradeoffs

- No nested expressions/functions in placeholders.
- No conditionals/loops in templates.
- No persistence/version registry service layer.

# How to Run

Install:
```bash
cd prompt-template-variable-substitution
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
