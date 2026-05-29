from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .errors import ToolValidationError


@dataclass(frozen=True)
class ToolSpec:
    name: str
    required_args: set[str]
    handler: Callable[[dict[str, Any]], dict[str, Any]]

    def validate(self, args: dict[str, Any]) -> None:
        missing = sorted(self.required_args - set(args.keys()))
        if missing:
            raise ToolValidationError(f"missing required args for {self.name}: {', '.join(missing)}")


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()

    def calculator(args: dict[str, Any]) -> dict[str, Any]:
        a = float(args["a"])
        b = float(args["b"])
        op = args.get("op", "+")
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = a / b
        else:
            raise ToolValidationError(f"unsupported op: {op}")
        return {"result": result}

    def web_search(args: dict[str, Any]) -> dict[str, Any]:
        query = str(args["query"]).strip().lower()
        fake_index = {
            "capital of france": "Paris is the capital of France.",
            "langchain": "LangChain provides building blocks for LLM apps.",
        }
        return {"summary": fake_index.get(query, "No relevant result found.")}

    registry.register(ToolSpec(name="calculator", required_args={"a", "b"}, handler=calculator))
    registry.register(ToolSpec(name="web_search", required_args={"query"}, handler=web_search))
    return registry
