from __future__ import annotations

from .errors import ToolNotFoundError, ToolValidationError
from .models import ToolCall, ToolResult
from .tools import ToolRegistry


class FunctionCallingHandler:
    def __init__(self, registry: ToolRegistry) -> None:
        self._registry = registry

    def handle(self, tool_call: ToolCall) -> ToolResult:
        spec = self._registry.get(tool_call.tool_name)
        if spec is None:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=f"tool not found: {tool_call.tool_name}",
            )

        try:
            spec.validate(tool_call.arguments)
            output = spec.handler(tool_call.arguments)
            return ToolResult(tool_name=tool_call.tool_name, success=True, output=output)
        except (ToolValidationError, ValueError, ZeroDivisionError) as exc:
            return ToolResult(
                tool_name=tool_call.tool_name,
                success=False,
                error=str(exc),
            )

    def handle_many(self, calls: list[ToolCall]) -> list[ToolResult]:
        return [self.handle(call) for call in calls]
