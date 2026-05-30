from token_counting_context_window.context_manager import ContextWindowManager
from token_counting_context_window.models import ChatMessage
from token_counting_context_window.tokenizer import SimpleWhitespaceTokenCounter


def test_token_counter_counts_words_and_punctuation() -> None:
    counter = SimpleWhitespaceTokenCounter()
    assert counter.count_text_tokens("Hello, world!") == 4


def test_context_window_keeps_latest_messages_within_budget() -> None:
    manager = ContextWindowManager(SimpleWhitespaceTokenCounter(), max_tokens=20, reserved_output_tokens=5)
    messages = [
        ChatMessage(role="system", content="You are helpful."),
        ChatMessage(role="user", content="Tell me about embeddings and retrieval."),
        ChatMessage(role="assistant", content="Embeddings map text into vectors."),
        ChatMessage(role="user", content="Now explain cosine similarity quickly."),
    ]

    result = manager.build_context(messages)

    assert result.used_tokens <= 15
    assert len(result.messages) >= 1
    assert result.messages[-1].content == "Now explain cosine similarity quickly."


def test_context_window_drops_when_budget_small() -> None:
    manager = ContextWindowManager(SimpleWhitespaceTokenCounter(), max_tokens=10, reserved_output_tokens=3)
    messages = [
        ChatMessage(role="user", content="one two three four five six"),
        ChatMessage(role="assistant", content="alpha beta gamma delta epsilon"),
    ]

    result = manager.build_context(messages)

    assert result.used_tokens <= 7
    assert result.dropped_messages >= 1


def test_invalid_configuration_raises() -> None:
    try:
        ContextWindowManager(SimpleWhitespaceTokenCounter(), max_tokens=5, reserved_output_tokens=5)
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "reserved_output_tokens" in str(exc)
