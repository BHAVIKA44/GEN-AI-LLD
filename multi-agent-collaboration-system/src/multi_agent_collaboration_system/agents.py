from __future__ import annotations

from .models import Plan, ResearchBundle


class SimplePlannerAgent:
    def plan(self, task: str) -> Plan:
        clean = task.strip()
        if not clean:
            return Plan(steps=["Clarify task objective"])
        return Plan(
            steps=[
                f"Define objective for: {clean}",
                "Identify key constraints and assumptions",
                "Draft concise deliverable",
            ]
        )


class SimpleResearchAgent:
    def research(self, step: str) -> str:
        return f"Finding: {step} -> include practical and realistic details."


class SimpleWriterAgent:
    def write(self, task: str, plan: Plan, research: ResearchBundle) -> str:
        lines: list[str] = [f"Task: {task}", "", "Plan:"]
        lines.extend(f"- {s}" for s in plan.steps)
        lines.append("")
        lines.append("Findings:")
        lines.extend(f"- {f}" for f in research.findings)
        lines.append("")
        lines.append("Final Draft:")
        lines.append("Deliver a concise solution using the plan and findings above.")
        return "\n".join(lines)
