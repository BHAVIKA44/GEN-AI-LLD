from __future__ import annotations

from typing import Protocol

from .models import DetectionResult


class InjectionDetector(Protocol):
    def detect(self, user_input: str) -> DetectionResult:
        ...
