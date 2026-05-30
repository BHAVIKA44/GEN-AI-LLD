from __future__ import annotations

from .interfaces import PlannerAgent, ResearchAgent, WriterAgent
from .models import CollaborationResult, ResearchBundle, TaskRequest


class MultiAgentOrchestrator:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: WriterAgent) -> None:
        self._planner = planner
        self._researcher = researcher
        self._writer = writer

    def run(self, request: TaskRequest) -> CollaborationResult:
        if not request.task.strip():
            raise ValueError("task must not be empty")

        plan = self._planner.plan(request.task)
        findings = [self._researcher.research(step) for step in plan.steps]
        bundle = ResearchBundle(findings=findings)
        final_output = self._writer.write(request.task, plan, bundle)

        return CollaborationResult(final_output=final_output, plan=plan, findings=findings)
