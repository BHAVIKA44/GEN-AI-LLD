from chatbot_conversation_memory_system.memory import (
    BufferMemory,
    SlidingWindowMemory,
    SummaryMemory,
)


def test_buffer_memory_keeps_full_history() -> None:
    mem = BufferMemory()
    mem.add_turn("hi", "hello")
    mem.add_turn("how are you", "great")

    ctx = mem.get_context()

    assert len(ctx) == 4
    assert ctx[0].content == "hi"
    assert ctx[-1].content == "great"


def test_sliding_window_keeps_latest_turns_only() -> None:
    mem = SlidingWindowMemory(window_size=2)
    mem.add_turn("u1", "a1")
    mem.add_turn("u2", "a2")
    mem.add_turn("u3", "a3")

    ctx = mem.get_context()

    assert len(ctx) == 4
    assert ctx[0].content == "u2"
    assert ctx[-1].content == "a3"


def test_summary_memory_includes_summary_and_recent() -> None:
    mem = SummaryMemory(recent_turns=1)
    mem.add_turn("book me a flight", "Sure, where to?")
    mem.add_turn("to Delhi", "What date?")

    ctx = mem.get_context()

    assert ctx[0].role == "system"
    assert "Conversation summary" in ctx[0].content
    assert ctx[-2].content == "to Delhi"
    assert ctx[-1].content == "What date?"


def test_clear_resets_memories() -> None:
    mem = BufferMemory()
    mem.add_turn("x", "y")
    mem.clear()

    assert mem.get_context() == []
