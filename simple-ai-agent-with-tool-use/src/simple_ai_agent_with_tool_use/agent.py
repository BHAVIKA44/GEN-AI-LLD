from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from .models import AgentResponse
from .tools import MockSearchTool, SafeCalculator, SearchTool


class AgentState(TypedDict, total=False):
    user_query: str
    selected_tool: str
    tool_input: str
    tool_output: str
    final_answer: str


class SimpleToolAgent:
    def __init__(self, calculator: SafeCalculator, search_tool: SearchTool) -> None:
        self._calculator = calculator
        self._search_tool = search_tool
        self._graph = self._build_graph().compile()

    def run(self, user_query: str) -> AgentResponse:
        state = self._graph.invoke({"user_query": user_query})
        return AgentResponse(
            answer=state["final_answer"],
            tool_used=state.get("selected_tool"),
            tool_output=state.get("tool_output"),
        )

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(AgentState)
        graph.add_node("decide", self._decide_tool)
        graph.add_node("use_calculator", self._use_calculator)
        graph.add_node("use_search", self._use_search)
        graph.add_node("finalize", self._finalize)

        graph.add_edge(START, "decide")
        graph.add_conditional_edges(
            "decide",
            self._route,
            {
                "calculator": "use_calculator",
                "search": "use_search",
                "finalize": "finalize",
            },
        )
        graph.add_edge("use_calculator", "finalize")
        graph.add_edge("use_search", "finalize")
        graph.add_edge("finalize", END)
        return graph

    def _decide_tool(self, state: AgentState) -> AgentState:
        q = state["user_query"].strip()
        lower = q.lower()

        if any(token in lower for token in ["calculate", "+", "-", "*", "/", "^"]):
            expr = lower.replace("calculate", "").strip() or q
            return {"selected_tool": "calculator", "tool_input": expr}

        if any(token in lower for token in ["search", "who", "what", "when", "where", "capital"]):
            cleaned = lower.replace("search", "").strip() or q
            return {"selected_tool": "search", "tool_input": cleaned}

        return {"selected_tool": "none", "final_answer": "I can help with calculations or web lookup. Please ask one of those."}

    def _route(self, state: AgentState) -> Literal["calculator", "search", "finalize"]:
        selected = state.get("selected_tool", "none")
        if selected == "calculator":
            return "calculator"
        if selected == "search":
            return "search"
        return "finalize"

    def _use_calculator(self, state: AgentState) -> AgentState:
        result = self._calculator.calculate(state.get("tool_input", ""))
        return {"tool_output": result}

    def _use_search(self, state: AgentState) -> AgentState:
        result = self._search_tool.search(state.get("tool_input", ""))
        return {"tool_output": result}

    def _finalize(self, state: AgentState) -> AgentState:
        if state.get("selected_tool") in {"calculator", "search"}:
            return {"final_answer": state.get("tool_output", "No result")}
        return {"final_answer": state.get("final_answer", "Unable to answer")}
