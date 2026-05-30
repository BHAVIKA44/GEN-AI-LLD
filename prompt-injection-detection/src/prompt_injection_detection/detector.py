from __future__ import annotations

import re

from .models import DetectionResult, DetectionSignal


class RuleBasedPromptInjectionDetector:
    def __init__(self) -> None:
        self._patterns: list[tuple[str, float, str]] = [
            (r"ignore\s+previous\s+instructions", 0.45, "Attempts to override existing instructions."),
            (r"disregard\s+(all|your)\s+(rules|instructions)", 0.45, "Explicit instruction bypass attempt."),
            (r"reveal\s+(system\s+prompt|hidden\s+prompt)", 0.4, "Attempts to exfiltrate hidden prompt."),
            (r"developer\s+message", 0.35, "References privileged instruction layers."),
            (r"jailbreak|bypass\s+safety", 0.4, "Tries to bypass safety boundaries."),
            (r"act\s+as\s+if\s+you\s+are\s+not\s+bound", 0.3, "Role manipulation attempt."),
        ]

    def detect(self, user_input: str) -> DetectionResult:
        text = user_input.lower().strip()
        if not text:
            return DetectionResult(risk_score=0.0, signals=[])

        signals: list[DetectionSignal] = []
        for pattern, score, reason in self._patterns:
            if re.search(pattern, text):
                signals.append(DetectionSignal(name=pattern, score=score, reason=reason))

        if self._contains_many_imperatives(text):
            signals.append(
                DetectionSignal(
                    name="imperative_density",
                    score=0.2,
                    reason="High imperative density often appears in injection attempts.",
                )
            )

        risk = min(1.0, sum(s.score for s in signals))
        return DetectionResult(risk_score=risk, signals=signals)

    @staticmethod
    def _contains_many_imperatives(text: str) -> bool:
        cues = ["ignore", "reveal", "print", "dump", "show", "override", "bypass", "disclose"]
        count = sum(1 for c in cues if c in text)
        return count >= 3
