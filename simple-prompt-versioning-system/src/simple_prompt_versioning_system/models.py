from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PromptVersion:
    prompt_name: str
    version: int
    template: str
    metadata: dict[str, str] = field(default_factory=dict)
    is_active: bool = False
