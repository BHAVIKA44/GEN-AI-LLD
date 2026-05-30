from llm_output_guardrails_offtopic_pii.checks import OffTopicCheck, PIICheck
from llm_output_guardrails_offtopic_pii.guardrails import OutputGuardrails
from llm_output_guardrails_offtopic_pii.models import GuardrailInput


def build_guardrails() -> OutputGuardrails:
    return OutputGuardrails(checks=[OffTopicCheck(), PIICheck()], redact_threshold=0.35, block_threshold=0.75)


def test_pass_for_relevant_non_pii_output() -> None:
    gr = build_guardrails()
    result = gr.evaluate(
        GuardrailInput(
            user_query="Explain vector databases",
            llm_output="Vector databases store embeddings and support similarity search.",
        )
    )

    assert result.action == "pass"
    assert result.output_text.startswith("Vector databases")


def test_redact_when_pii_detected() -> None:
    gr = build_guardrails()
    result = gr.evaluate(
        GuardrailInput(
            user_query="Share support contact",
            llm_output="Contact me at alice@example.com or 555-123-4567.",
        )
    )

    assert result.action in {"redact", "block"}
    if result.action == "redact":
        assert "[REDACTED_EMAIL]" in result.output_text


def test_block_when_high_risk_combined() -> None:
    gr = build_guardrails()
    result = gr.evaluate(
        GuardrailInput(
            user_query="Explain embeddings",
            llm_output="Call 555-123-4567. Also, here is random football gossip unrelated to your request.",
        )
    )

    assert result.action in {"redact", "block"}
