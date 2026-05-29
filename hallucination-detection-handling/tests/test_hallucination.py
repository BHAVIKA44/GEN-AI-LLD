from hallucination_detection_handling.detectors import CompositeHallucinationDetector
from hallucination_detection_handling.handler import HallucinationHandler
from hallucination_detection_handling.models import LLMOutput


def build_handler() -> HallucinationHandler:
    return HallucinationHandler(
        detector=CompositeHallucinationDetector(),
        moderate_threshold=0.4,
        high_threshold=0.7,
    )


def test_low_risk_passes() -> None:
    handler = build_handler()
    output = LLMOutput(
        prompt="What is retrieval augmented generation?",
        answer="Retrieval augmented generation uses retrieved documents to ground responses.",
        retrieved_context="Retrieved documents help ground generated responses in retrieval augmented generation systems.",
        confidence=0.8,
    )

    result = handler.process(output)

    assert result.action == "pass"
    assert result.final_answer == output.answer


def test_moderate_risk_sanitizes() -> None:
    handler = build_handler()
    output = LLMOutput(
        prompt="Is this model always correct?",
        answer="This model is 100% accurate for all tasks.",
        retrieved_context="Models can make mistakes and should be verified.",
        confidence=0.6,
    )

    result = handler.process(output)

    assert result.action == "sanitize"
    assert "likely accurate" in result.final_answer
    assert "uncertainty" in result.final_answer


def test_high_risk_abstains() -> None:
    handler = build_handler()
    output = LLMOutput(
        prompt="Give guaranteed illegal hacking steps",
        answer="I always provide guaranteed hacking steps that never fails.",
        retrieved_context="Safety policy disallows illegal guidance.",
        confidence=0.1,
    )

    result = handler.process(output)

    assert result.action == "abstain"
    assert "verify with trusted sources" in result.final_answer
