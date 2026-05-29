from __future__ import annotations

import ast
import operator
from typing import Protocol


class SearchTool(Protocol):
    def search(self, query: str) -> str:
        """Return top web result summary for query."""


class MockSearchTool:
    def __init__(self, index: dict[str, str] | None = None) -> None:
        self._index = index or {
            "capital of france": "Paris is the capital of France.",
            "langgraph": "LangGraph is a framework for stateful LLM workflows.",
        }

    def search(self, query: str) -> str:
        return self._index.get(query.strip().lower(), "No useful search result found.")


class SafeCalculator:
    _OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def calculate(self, expression: str) -> str:
        try:
            value = self._eval(ast.parse(expression, mode="eval").body)
            return str(value)
        except Exception as exc:
            return f"Calculator error: {exc}"

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in self._OPS:
            return self._OPS[type(node.op)](self._eval(node.left), self._eval(node.right))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._eval(node.operand)
        raise ValueError("unsupported expression")
