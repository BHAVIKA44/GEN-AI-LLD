from __future__ import annotations

from typing import Protocol

from .models import GuardrailInput, Signal


class OutputCheck(Protocol):
    def run(self, data: GuardrailInput) -> Signal | None:
        ...
