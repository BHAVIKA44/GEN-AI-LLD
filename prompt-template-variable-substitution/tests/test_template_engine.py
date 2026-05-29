from prompt_template_variable_substitution.errors import (
    MissingVariableError,
    TemplateValidationError,
)
from prompt_template_variable_substitution.models import PromptTemplate
from prompt_template_variable_substitution.template_engine import PromptTemplateEngine


def test_render_substitutes_all_variables() -> None:
    engine = PromptTemplateEngine()
    template = PromptTemplate(
        name="support_reply",
        version="v1",
        template="Hello {{ user_name }}, your ticket {{ ticket_id }} is {{ status }}.",
    )

    out = engine.render(
        template,
        {"user_name": "Ava", "ticket_id": 42, "status": "resolved"},
    )

    assert out == "Hello Ava, your ticket 42 is resolved."


def test_missing_variable_strict_mode_raises() -> None:
    engine = PromptTemplateEngine()
    template = PromptTemplate(name="x", version="v1", template="Hi {{name}} {{city}}")

    try:
        engine.render(template, {"name": "Sam"}, strict=True)
        assert False, "expected MissingVariableError"
    except MissingVariableError as exc:
        assert "city" in str(exc)


def test_missing_variable_lenient_mode_keeps_placeholder() -> None:
    engine = PromptTemplateEngine()
    template = PromptTemplate(name="x", version="v1", template="Hi {{name}} from {{city}}")

    out = engine.render(template, {"name": "Sam"}, strict=False)

    assert out == "Hi Sam from {{city}}"


def test_required_variables_extraction() -> None:
    engine = PromptTemplateEngine()
    required = engine.required_variables("Q: {{question}} | Tone: {{ tone }}")

    assert required == {"question", "tone"}


def test_invalid_template_raises() -> None:
    engine = PromptTemplateEngine()

    try:
        engine.validate("hello {{1bad}}")
        assert False, "expected TemplateValidationError"
    except TemplateValidationError:
        pass
