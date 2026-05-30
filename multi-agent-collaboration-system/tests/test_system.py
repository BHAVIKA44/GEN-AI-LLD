from multi_agent_collaboration_system.agents import (
    SimplePlannerAgent,
    SimpleResearchAgent,
    SimpleWriterAgent,
)
from multi_agent_collaboration_system.models import TaskRequest
from multi_agent_collaboration_system.orchestrator import MultiAgentOrchestrator


def build_system() -> MultiAgentOrchestrator:
    return MultiAgentOrchestrator(
        planner=SimplePlannerAgent(),
        researcher=SimpleResearchAgent(),
        writer=SimpleWriterAgent(),
    )


def test_multi_agent_flow_returns_result() -> None:
    orchestrator = build_system()
    result = orchestrator.run(TaskRequest(task="Prepare launch plan for a new AI feature"))

    assert len(result.plan.steps) >= 1
    assert len(result.findings) == len(result.plan.steps)
    assert "Final Draft:" in result.final_output


def test_writer_output_contains_plan_and_findings() -> None:
    orchestrator = build_system()
    result = orchestrator.run(TaskRequest(task="Create onboarding checklist"))

    assert "Plan:" in result.final_output
    assert "Findings:" in result.final_output


def test_empty_task_raises() -> None:
    orchestrator = build_system()
    try:
        orchestrator.run(TaskRequest(task="   "))
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "task" in str(exc)
