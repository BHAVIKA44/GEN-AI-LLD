# Problem Statement

Build a multi-agent system where agents have different roles and collaborate on a task.

# Requirements

## Functional requirements
- Accept a task request.
- Use role-specific agents:
  - Planner agent
  - Research agent
  - Writer agent
- Coordinate collaboration across agents.
- Return final synthesized output with intermediate artifacts.

## Non-functional requirements
- Interview-size architecture.
- Extensible agent interfaces.
- Deterministic local tests.

## Assumptions
- Single collaborative workflow per request.
- Sequential collaboration is sufficient for baseline.

# Design Overview

Main components:
- `SimplePlannerAgent`: decomposes task into plan steps.
- `SimpleResearchAgent`: produces a finding per step.
- `SimpleWriterAgent`: synthesizes final output.
- `MultiAgentOrchestrator`: coordinates end-to-end flow.

Data flow:
1. Planner produces step-wise plan.
2. Researcher gathers findings for each step.
3. Writer composes final draft from task + plan + findings.

# Class / Module Design

- `models.py`: task, plan, research bundle, final result
- `interfaces.py`: protocols for planner/researcher/writer
- `agents.py`: default agent implementations
- `orchestrator.py`: collaboration coordinator

# Technology Selection Rationale

- LangGraph: Not used in code.
  - Why: flow is linear and small; a direct orchestrator is clearer for 1-hour round.
  - Tradeoff: less built-in state/retry tooling.
- LangChain: Not used.
  - Why: no model integration required in baseline.

# Error Handling

- Empty task validation.
- Deterministic fallbacks in planner for malformed input.

# Testing Strategy

- End-to-end multi-agent collaboration flow.
- Output structure validation.
- Invalid input validation.

# Tradeoffs

- Sequential execution only.
- No real LLM/tool integrations.
- No conflict-resolution between agents.

# How to Run

Install:
```bash
cd multi-agent-collaboration-system
python3 -m pip install -e ".[dev]"
```

Run tests:
```bash
python3 -m pytest
```
