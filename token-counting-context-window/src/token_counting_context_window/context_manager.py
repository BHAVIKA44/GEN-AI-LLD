from __future__ import annotations

from .interfaces import TokenCounter
from .models import ChatMessage, ContextBuildResult


class ContextWindowManager:
    def __init__(self, token_counter: TokenCounter, max_tokens: int, reserved_output_tokens: int = 0) -> None:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be > 0")
        if reserved_output_tokens < 0:
            raise ValueError("reserved_output_tokens must be >= 0")
        if reserved_output_tokens >= max_tokens:
            raise ValueError("reserved_output_tokens must be < max_tokens")

        self._counter = token_counter
        self._max_tokens = max_tokens
        self._reserved = reserved_output_tokens

    def build_context(self, messages: list[ChatMessage]) -> ContextBuildResult:
        budget = self._max_tokens - self._reserved
        used = 0
        kept_reversed: list[ChatMessage] = []

        for msg in reversed(messages):
            msg_tokens = self._message_tokens(msg)
            if used + msg_tokens > budget:
                continue
            kept_reversed.append(msg)
            used += msg_tokens

        kept = list(reversed(kept_reversed))
        dropped = len(messages) - len(kept)
        return ContextBuildResult(messages=kept, used_tokens=used, dropped_messages=dropped)

    def count_message_tokens(self, message: ChatMessage) -> int:
        return self._message_tokens(message)

    def _message_tokens(self, message: ChatMessage) -> int:
        role_tokens = self._counter.count_text_tokens(message.role)
        content_tokens = self._counter.count_text_tokens(message.content)
        # Small structural overhead per message.
        return role_tokens + content_tokens + 2
