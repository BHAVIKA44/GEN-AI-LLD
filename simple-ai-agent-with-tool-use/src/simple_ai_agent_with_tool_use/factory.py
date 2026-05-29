from __future__ import annotations

from .agent import SimpleToolAgent
from .tools import MockSearchTool, SafeCalculator


def build_default_agent() -> SimpleToolAgent:
    return SimpleToolAgent(calculator=SafeCalculator(), search_tool=MockSearchTool())
