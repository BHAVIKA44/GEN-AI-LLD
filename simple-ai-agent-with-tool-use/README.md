# Problem Statement

Build a simple AI agent with tool use (e.g., calculator, web search).

# Requirements

## Functional requirements
- Accept a user query.
- Decide whether to use calculator or web search tool.
- Execute selected tool.
- Return final answer and tool-use info.

## Non-functional requirements
- Keep implementation interview-sized (1 hour).
- Testable offline without API keys.
- Extensible tool and orchestration design.

## Assumptions
- Tool-selection heuristics are acceptable for a basic interview implementation.
- Web search is mocked locally for deterministic tests.

# Design Overview

Main components:
- `SimpleToolAgent` (LangGraph workflow orchestrator)
- `SafeCalculator` (math tool)
- `MockSearchTool` (search abstraction implementation)
- `build_default_agent()` (dependency composition)

Data flow:
1. `decide` node selects tool based on query.
2. Agent routes to `use_calculator` or `use_search`.
3. `finalize` returns user-facing answer.

# Class / Module Design

- `models.py`: `AgentResponse`
- `tools.py`: `SearchTool`, `MockSearchTool`, `SafeCalculator`
- `agent.py`: LangGraph state and nodes
- `factory.py`: object wiring

# Technology Selection Rationale

- LangChain: Not used directly.
  - Why: this problem is tool-orchestration focused, not prompt/retriever focused.
  - Tradeoff: fewer built-in LLM/prompt abstractions.
- LangGraph: Used.
  - Why: clean fit for stateful workflow (decide -> tool call -> finalize).
  - Tradeoff: slight framework overhead vs one service class.
- RAG/Vector DB: Not used.
  - Why: not required by this problem statement.
- Agents: Used.
  - Why: core requirement is tool-using agent behavior.
- Caching/Guardrails/Evaluation: Not implemented.
  - Why: out of 1-hour scope; easy to add later.

# Error Handling

- Calculator safely parses restricted arithmetic AST.
- Unsupported expressions return controlled error text.
- Unknown intent returns fallback guidance.

# Testing Strategy

- Tests validate:
  - Calculator tool routing and output
  - Search tool routing and output
  - Fallback behavior for unsupported query intent

# Tradeoffs

Intentionally simplified:
- Rule-based tool selection instead of LLM planner.
- Mock web search instead of real provider.
- Single-agent, single-turn workflow.

# How to Run

Install:
```bash
cd simple-ai-agent-with-tool-use
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
