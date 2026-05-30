from __future__ import annotations

from .errors import PromptNotFoundError, PromptValidationError
from .models import PromptVersion
from .store import InMemoryPromptStore


class PromptVersioningService:
    def __init__(self, store: InMemoryPromptStore) -> None:
        self._store = store

    def create_version(self, prompt_name: str, template: str, metadata: dict[str, str] | None = None) -> PromptVersion:
        if not prompt_name.strip():
            raise PromptValidationError("prompt_name must not be empty")
        if not template.strip():
            raise PromptValidationError("template must not be empty")

        existing = self._store.list_versions(prompt_name)
        next_version = len(existing) + 1
        is_first = next_version == 1

        created = PromptVersion(
            prompt_name=prompt_name,
            version=next_version,
            template=template,
            metadata=metadata or {},
            is_active=is_first,
        )

        self._store.save_versions(prompt_name, existing + [created])
        return created

    def list_versions(self, prompt_name: str) -> list[PromptVersion]:
        versions = self._store.list_versions(prompt_name)
        if not versions:
            raise PromptNotFoundError(f"prompt not found: {prompt_name}")
        return versions

    def get_version(self, prompt_name: str, version: int) -> PromptVersion:
        for item in self._store.list_versions(prompt_name):
            if item.version == version:
                return item
        raise PromptNotFoundError(f"version {version} not found for prompt {prompt_name}")

    def get_active(self, prompt_name: str) -> PromptVersion:
        for item in self._store.list_versions(prompt_name):
            if item.is_active:
                return item
        raise PromptNotFoundError(f"active prompt not found for {prompt_name}")

    def activate_version(self, prompt_name: str, version: int) -> PromptVersion:
        versions = self._store.list_versions(prompt_name)
        if not versions:
            raise PromptNotFoundError(f"prompt not found: {prompt_name}")

        found = False
        updated: list[PromptVersion] = []
        for item in versions:
            active = item.version == version
            if active:
                found = True
            updated.append(
                PromptVersion(
                    prompt_name=item.prompt_name,
                    version=item.version,
                    template=item.template,
                    metadata=item.metadata,
                    is_active=active,
                )
            )

        if not found:
            raise PromptNotFoundError(f"version {version} not found for prompt {prompt_name}")

        self._store.save_versions(prompt_name, updated)
        return self.get_active(prompt_name)
