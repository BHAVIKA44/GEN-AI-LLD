from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionSignal:
    name: str
    score: float
    reason: str


@dataclass(frozen=True)
class DetectionResult:
    risk_score: float
    signals: list[DetectionSignal]


@dataclass(frozen=True)
class GuardDecision:
    action: str
    risk_score: float
    message: str
    signals: list[DetectionSignal]
