from __future__ import annotations

from .interfaces import HallucinationDetector
from .models import HandledResponse, LLMOutput


class HallucinationHandler:
    def __init__(
        self,
        detector: HallucinationDetector,
        moderate_threshold: float = 0.4,
        high_threshold: float = 0.7,
    ) -> None:
        if not (0 <= moderate_threshold <= 1):
            raise ValueError("moderate_threshold must be between 0 and 1")
        if not (0 <= high_threshold <= 1):
            raise ValueError("high_threshold must be between 0 and 1")
        if moderate_threshold > high_threshold:
            raise ValueError("moderate_threshold must be <= high_threshold")

        self._detector = detector
        self._moderate = moderate_threshold
        self._high = high_threshold

    def process(self, output: LLMOutput) -> HandledResponse:
        result = self._detector.detect(output)

        if result.risk_score >= self._high:
            return HandledResponse(
                final_answer="I may be uncertain about this answer. Please verify with trusted sources.",
                action="abstain",
                risk_score=result.risk_score,
                signals=result.signals,
            )

        if result.risk_score >= self._moderate:
            sanitized = output.answer.replace("100% accurate", "likely accurate")
            return HandledResponse(
                final_answer=f"{sanitized}\n\nNote: This response may contain uncertainty.",
                action="sanitize",
                risk_score=result.risk_score,
                signals=result.signals,
            )

        return HandledResponse(
            final_answer=output.answer,
            action="pass",
            risk_score=result.risk_score,
            signals=result.signals,
        )
