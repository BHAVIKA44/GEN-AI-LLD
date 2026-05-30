from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskRequest:
    task: str


@dataclass(frozen=True)
class Plan:
    steps: list[str]


@dataclass(frozen=True)
class ResearchBundle:
    findings: list[str]


@dataclass(frozen=True)
class CollaborationResult:
    final_output: str
    plan: Plan
    findings: list[str] = field(default_factory=list)
