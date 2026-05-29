from simple_ai_agent_with_tool_use.factory import build_default_agent


def test_calculator_tool_use() -> None:
    agent = build_default_agent()

    result = agent.run("calculate 2 + 3 * 4")

    assert result.tool_used == "calculator"
    assert result.answer == "14.0"


def test_search_tool_use() -> None:
    agent = build_default_agent()

    result = agent.run("What is the capital of France")

    assert result.tool_used == "search"
    assert "Paris" in result.answer


def test_fallback_for_non_tool_query() -> None:
    agent = build_default_agent()

    result = agent.run("tell me a joke")

    assert result.tool_used == "none"
    assert "calculations or web lookup" in result.answer
