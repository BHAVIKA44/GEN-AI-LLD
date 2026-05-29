from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LLMOutput:
    prompt: str
    answer: str
    retrieved_context: str
    confidence: float | None = None


@dataclass(frozen=True)
class HallucinationSignal:
    detector_name: str
    score: float
    message: str


@dataclass(frozen=True)
class DetectionResult:
    risk_score: float
    signals: list[HallucinationSignal]


@dataclass(frozen=True)
class HandledResponse:
    final_answer: str
    action: str
    risk_score: float
    signals: list[HallucinationSignal]
