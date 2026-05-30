from __future__ import annotations

from collections import defaultdict

from .models import PromptVersion


class InMemoryPromptStore:
    def __init__(self) -> None:
        self._data: dict[str, list[PromptVersion]] = defaultdict(list)

    def list_versions(self, prompt_name: str) -> list[PromptVersion]:
        return list(self._data.get(prompt_name, []))

    def save_versions(self, prompt_name: str, versions: list[PromptVersion]) -> None:
        self._data[prompt_name] = list(versions)
