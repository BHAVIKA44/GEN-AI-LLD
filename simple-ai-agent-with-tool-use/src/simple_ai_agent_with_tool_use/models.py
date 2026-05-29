from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentResponse:
    answer: str
    tool_used: str | None
    tool_output: str | None
