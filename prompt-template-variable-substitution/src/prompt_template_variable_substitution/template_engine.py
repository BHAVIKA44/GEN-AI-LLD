from __future__ import annotations

import re

from .errors import MissingVariableError, TemplateValidationError
from .models import PromptTemplate

_VAR_PATTERN = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


class PromptTemplateEngine:
    """Renders templates with {{ variable }} substitution."""

    def validate(self, template_text: str) -> None:
        if not template_text.strip():
            raise TemplateValidationError("template must not be empty")

        opens = template_text.count("{{")
        closes = template_text.count("}}")
        if opens != closes:
            raise TemplateValidationError("unbalanced template braces")

        invalid = re.findall(r"\{\{\s*([^{}\s][^{}]*)\}\}", template_text)
        for raw in invalid:
            stripped = raw.strip()
            if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", stripped):
                raise TemplateValidationError(f"invalid variable name: {stripped}")

    def required_variables(self, template_text: str) -> set[str]:
        self.validate(template_text)
        return set(_VAR_PATTERN.findall(template_text))

    def render(
        self,
        prompt_template: PromptTemplate,
        variables: dict[str, str | int | float],
        *,
        strict: bool = True,
    ) -> str:
        text = prompt_template.template
        self.validate(text)

        required = self.required_variables(text)
        missing = sorted(v for v in required if v not in variables)
        if strict and missing:
            raise MissingVariableError(f"missing variables: {', '.join(missing)}")

        def substitute(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in variables:
                return match.group(0)
            return str(variables[key])

        return _VAR_PATTERN.sub(substitute, text)
