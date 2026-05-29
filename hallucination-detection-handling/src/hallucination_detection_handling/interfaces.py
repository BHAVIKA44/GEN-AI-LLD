from __future__ import annotations

from typing import Protocol

from .models import DetectionResult, LLMOutput


class HallucinationDetector(Protocol):
    def detect(self, output: LLMOutput) -> DetectionResult:
        ...
