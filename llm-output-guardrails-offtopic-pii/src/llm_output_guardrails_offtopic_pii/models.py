from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailInput:
    user_query: str
    llm_output: str


@dataclass(frozen=True)
class Signal:
    name: str
    score: float
    reason: str


@dataclass(frozen=True)
class GuardrailResult:
    action: str
    output_text: str
    risk_score: float
    signals: list[Signal]
