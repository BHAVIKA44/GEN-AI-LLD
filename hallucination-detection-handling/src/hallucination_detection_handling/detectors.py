from __future__ import annotations

import re

from .models import DetectionResult, HallucinationSignal, LLMOutput


class CompositeHallucinationDetector:
    def __init__(self) -> None:
        self._checks = [
            self._grounding_check,
            self._confidence_check,
            self._suspicious_claim_check,
        ]

    def detect(self, output: LLMOutput) -> DetectionResult:
        signals: list[HallucinationSignal] = []
        for check in self._checks:
            signal = check(output)
            if signal is not None:
                signals.append(signal)

        risk = sum(s.score for s in signals)
        risk = min(1.0, risk)
        return DetectionResult(risk_score=risk, signals=signals)

    def _grounding_check(self, output: LLMOutput) -> HallucinationSignal | None:
        answer_terms = {w.lower() for w in re.findall(r"[a-zA-Z]{5,}", output.answer)}
        context_terms = {w.lower() for w in re.findall(r"[a-zA-Z]{5,}", output.retrieved_context)}

        if not answer_terms:
            return HallucinationSignal(
                detector_name="grounding",
                score=0.4,
                message="Answer contains insufficient grounded content.",
            )

        overlap = len(answer_terms & context_terms) / max(1, len(answer_terms))
        if overlap < 0.25:
            return HallucinationSignal(
                detector_name="grounding",
                score=0.5,
                message="Low overlap with retrieved context.",
            )
        return None

    def _confidence_check(self, output: LLMOutput) -> HallucinationSignal | None:
        if output.confidence is None:
            return None
        if output.confidence < 0.35:
            return HallucinationSignal(
                detector_name="confidence",
                score=0.3,
                message="Model confidence is low.",
            )
        return None

    def _suspicious_claim_check(self, output: LLMOutput) -> HallucinationSignal | None:
        suspicious = ["always", "guaranteed", "never fails", "100% accurate"]
        text = output.answer.lower()
        if any(p in text for p in suspicious):
            return HallucinationSignal(
                detector_name="claim_style",
                score=0.3,
                message="Answer uses absolute certainty language.",
            )
        return None
