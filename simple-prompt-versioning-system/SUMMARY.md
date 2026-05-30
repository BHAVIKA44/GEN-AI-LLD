# Files Created

- `README.md`
- `SUMMARY.md`
- `pyproject.toml`
- `src/simple_prompt_versioning_system/__init__.py`
- `src/simple_prompt_versioning_system/models.py`
- `src/simple_prompt_versioning_system/errors.py`
- `src/simple_prompt_versioning_system/store.py`
- `src/simple_prompt_versioning_system/service.py`
- `tests/test_versioning.py`

# Main Abstractions

- `PromptVersion`
- `InMemoryPromptStore`
- `PromptVersioningService`

# Design Choices

- Immutable version records.
- Explicit active-version control.
- Store/service separation for easy backend swap.

# Technology Choices

- Pure Python baseline.
- No framework overhead required.

# GenAI-Specific Considerations

- Supports prompt evolution and rollback.
- Active-version switch enables controlled prompt rollout.

# Testing Strategy

- Unit tests for create/list/get/activate and error paths.

# Extension Points

- Persistent DB-backed store.
- Environment/stage-specific active versions.
- Prompt diffing and approval workflows.

# Known Tradeoffs

- No history audit metadata (author/timestamp) yet.
- No concurrency locking.

# Final Interview Summary

This solution provides a clean and practical prompt versioning core with immutable versions and explicit active version switching, appropriately scoped for a 1-hour LLD interview.
