from __future__ import annotations

from .checks import redact_pii
from .interfaces import OutputCheck
from .models import GuardrailInput, GuardrailResult


class OutputGuardrails:
    def __init__(
        self,
        checks: list[OutputCheck],
        redact_threshold: float = 0.35,
        block_threshold: float = 0.75,
    ) -> None:
        if not checks:
            raise ValueError("at least one check is required")
        if not (0 <= redact_threshold <= 1 and 0 <= block_threshold <= 1):
            raise ValueError("thresholds must be between 0 and 1")
        if redact_threshold > block_threshold:
            raise ValueError("redact_threshold must be <= block_threshold")

        self._checks = checks
        self._redact = redact_threshold
        self._block = block_threshold

    def evaluate(self, data: GuardrailInput) -> GuardrailResult:
        signals = [s for check in self._checks if (s := check.run(data)) is not None]
        risk = min(1.0, sum(s.score for s in signals))

        if risk >= self._block:
            return GuardrailResult(
                action="block",
                output_text="Response blocked due to safety guardrails.",
                risk_score=risk,
                signals=signals,
            )

        if risk >= self._redact:
            redacted = redact_pii(data.llm_output)
            return GuardrailResult(
                action="redact",
                output_text=redacted,
                risk_score=risk,
                signals=signals,
            )

        return GuardrailResult(
            action="pass",
            output_text=data.llm_output,
            risk_score=risk,
            signals=signals,
        )
