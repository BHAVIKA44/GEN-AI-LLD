# Problem Statement

Write a function calling (tool use) handler for an LLM API.

# Requirements

## Functional requirements
- Accept tool-call requests from LLM output.
- Resolve tool by name from registry.
- Validate required arguments.
- Execute tool function.
- Return structured success/error result.
- Support batch handling of multiple tool calls.

## Non-functional requirements
- Interview-sized implementation.
- Extensible tool registration model.
- Deterministic offline tests.

## Assumptions
- LLM output has already been parsed into `tool_name` + `arguments`.
- Tools are pure in-process functions.

# Design Overview

Main components:
- `ToolRegistry`: stores available tool specs.
- `ToolSpec`: tool metadata + required arg schema + handler function.
- `FunctionCallingHandler`: dispatches calls, validates args, captures errors.
- `ToolCall` / `ToolResult`: structured I/O models.

Data flow:
1. Handler receives `ToolCall`.
2. Registry lookup by tool name.
3. Validate required args.
4. Execute tool handler.
5. Return `ToolResult` with success output or error message.

# Class / Module Design

- `models.py`: `ToolCall`, `ToolResult`
- `errors.py`: `ToolNotFoundError`, `ToolValidationError`
- `tools.py`: `ToolSpec`, `ToolRegistry`, default tools
- `handler.py`: `FunctionCallingHandler`

# Technology Selection Rationale

- LangChain/LangGraph: Not used in baseline.
  - Why: this task targets core dispatch/validation logic; direct implementation is faster and clearer for a 1-hour round.
  - Tradeoff: fewer built-in tool-calling integrations.
- API framework: Not required.
  - Why: problem scope is handler component, not transport layer.

# Error Handling

- Unknown tool returns structured failure result.
- Missing required args returns structured validation error.
- Tool runtime failures (value/division errors) converted to safe error result.

# Testing Strategy

- Calculator tool success.
- Web search tool success.
- Missing args validation failure.
- Unknown tool failure.

# Tradeoffs

- Minimal schema validation (required-arg only).
- No async tool execution.
- No retries/timeouts/isolation sandbox.

# How to Run

Install:
```bash
cd function-calling-tool-use-handler
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
