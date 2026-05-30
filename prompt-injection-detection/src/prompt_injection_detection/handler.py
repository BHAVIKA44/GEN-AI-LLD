from __future__ import annotations

from .interfaces import InjectionDetector
from .models import GuardDecision


class PromptInjectionGuard:
    def __init__(self, detector: InjectionDetector, warn_threshold: float = 0.35, block_threshold: float = 0.65) -> None:
        if not (0 <= warn_threshold <= 1 and 0 <= block_threshold <= 1):
            raise ValueError("thresholds must be between 0 and 1")
        if warn_threshold > block_threshold:
            raise ValueError("warn_threshold must be <= block_threshold")
        self._detector = detector
        self._warn = warn_threshold
        self._block = block_threshold

    def evaluate(self, user_input: str) -> GuardDecision:
        result = self._detector.detect(user_input)

        if result.risk_score >= self._block:
            return GuardDecision(
                action="block",
                risk_score=result.risk_score,
                message="Input appears to contain prompt-injection attempts and was blocked.",
                signals=result.signals,
            )

        if result.risk_score >= self._warn:
            return GuardDecision(
                action="warn",
                risk_score=result.risk_score,
                message="Input may contain instruction-manipulation patterns. Proceed with caution.",
                signals=result.signals,
            )

        return GuardDecision(
            action="allow",
            risk_score=result.risk_score,
            message="Input passed prompt-injection checks.",
            signals=result.signals,
        )
