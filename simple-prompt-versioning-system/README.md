# Problem Statement

Build a simple prompt versioning system.

# Requirements

## Functional requirements
- Create prompt versions.
- List all versions for a prompt.
- Fetch a specific version.
- Track and fetch active version.
- Activate any existing version.

## Non-functional requirements
- Interview-scale simplicity.
- Clear versioning semantics.
- Deterministic in-memory behavior for tests.

## Assumptions
- Version numbers are auto-incremented integers per prompt name.
- Prompt versions are immutable once created.

# Design Overview

Main components:
- `PromptVersion` model.
- `InMemoryPromptStore` repository.
- `PromptVersioningService` domain operations.

Data flow:
1. New template -> `create_version` -> incremented version stored.
2. `activate_version` updates active flag across versions.
3. Read APIs fetch versions/active version.

# Class / Module Design

- `models.py`: `PromptVersion`
- `errors.py`: `PromptNotFoundError`, `PromptValidationError`
- `store.py`: in-memory storage abstraction
- `service.py`: business logic for create/get/list/activate

# Technology Selection Rationale

- Pure Python: Used.
  - Why: problem is domain logic around version lifecycle.
- LangChain/LangGraph: Not used.
  - Why: no orchestration or retrieval pipeline needed.

# Error Handling

- Reject empty prompt name/template.
- Raise `PromptNotFoundError` for missing prompts/versions.
- Validate activation target exists.

# Testing Strategy

- Create/list version flow.
- Activate version flow.
- Missing prompt error path.
- Fetch specific version.

# Tradeoffs

- In-memory only (no persistence/audit trail).
- No branch/experiment labels beyond metadata.
- No concurrent write control.

# How to Run

Install:
```bash
cd simple-prompt-versioning-system
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
