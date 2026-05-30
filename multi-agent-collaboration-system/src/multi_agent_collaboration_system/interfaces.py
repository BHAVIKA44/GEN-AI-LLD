from __future__ import annotations

from typing import Protocol

from .models import Plan, ResearchBundle


class PlannerAgent(Protocol):
    def plan(self, task: str) -> Plan:
        ...


class ResearchAgent(Protocol):
    def research(self, step: str) -> str:
        ...


class WriterAgent(Protocol):
    def write(self, task: str, plan: Plan, research: ResearchBundle) -> str:
        ...
