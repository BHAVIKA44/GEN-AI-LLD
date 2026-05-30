from __future__ import annotations

import re

from .models import GuardrailInput, Signal


class OffTopicCheck:
    def run(self, data: GuardrailInput) -> Signal | None:
        query_terms = self._terms(data.user_query)
        output_terms = self._terms(data.llm_output)
        if not query_terms:
            return None

        overlap = len(query_terms & output_terms) / len(query_terms)
        if overlap < 0.2:
            return Signal(
                name="off_topic",
                score=0.45,
                reason="Low topical overlap between query and output.",
            )
        return None

    @staticmethod
    def _terms(text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z]{4,}", text.lower())
        stop = {"this", "that", "with", "from", "into", "about", "your", "what", "when"}
        return {w for w in words if w not in stop}


class PIICheck:
    EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    PHONE = re.compile(r"\b(?:\+?\d{1,2}[ -]?)?(?:\(?\d{3}\)?[ -]?)\d{3}[ -]?\d{4}\b")
    SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    def run(self, data: GuardrailInput) -> Signal | None:
        text = data.llm_output
        hits = 0
        if self.EMAIL.search(text):
            hits += 1
        if self.PHONE.search(text):
            hits += 1
        if self.SSN.search(text):
            hits += 1

        if hits == 0:
            return None

        return Signal(
            name="pii_leakage",
            score=min(1.0, 0.35 * hits + 0.25),
            reason="Potential PII detected in model output.",
        )


def redact_pii(text: str) -> str:
    text = PIICheck.EMAIL.sub("[REDACTED_EMAIL]", text)
    text = PIICheck.PHONE.sub("[REDACTED_PHONE]", text)
    text = PIICheck.SSN.sub("[REDACTED_SSN]", text)
    return text
