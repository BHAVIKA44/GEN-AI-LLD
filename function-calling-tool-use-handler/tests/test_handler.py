from function_calling_tool_use_handler.handler import FunctionCallingHandler
from function_calling_tool_use_handler.models import ToolCall
from function_calling_tool_use_handler.tools import build_default_registry


def test_calculator_tool_success() -> None:
    handler = FunctionCallingHandler(build_default_registry())

    result = handler.handle(ToolCall(tool_name="calculator", arguments={"a": 2, "b": 3, "op": "*"}))

    assert result.success is True
    assert result.output == {"result": 6.0}


def test_web_search_tool_success() -> None:
    handler = FunctionCallingHandler(build_default_registry())

    result = handler.handle(ToolCall(tool_name="web_search", arguments={"query": "capital of france"}))

    assert result.success is True
    assert "Paris" in (result.output or {}).get("summary", "")


def test_missing_args_returns_error() -> None:
    handler = FunctionCallingHandler(build_default_registry())

    result = handler.handle(ToolCall(tool_name="calculator", arguments={"a": 2}))

    assert result.success is False
    assert "missing required args" in (result.error or "")


def test_unknown_tool_returns_error() -> None:
    handler = FunctionCallingHandler(build_default_registry())

    result = handler.handle(ToolCall(tool_name="weather", arguments={"city": "NYC"}))

    assert result.success is False
    assert "tool not found" in (result.error or "")
