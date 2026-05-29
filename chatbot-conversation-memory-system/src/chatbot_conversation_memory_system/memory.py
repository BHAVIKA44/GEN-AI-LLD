from __future__ import annotations

from collections import deque

from .models import Message, Turn


class BufferMemory:
    """Stores complete conversation history."""

    def __init__(self) -> None:
        self._turns: list[Turn] = []

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        self._turns.append(Turn(user_message=user_message, assistant_message=assistant_message))

    def get_context(self) -> list[Message]:
        out: list[Message] = []
        for turn in self._turns:
            out.append(Message(role="user", content=turn.user_message))
            out.append(Message(role="assistant", content=turn.assistant_message))
        return out

    def clear(self) -> None:
        self._turns.clear()


class SlidingWindowMemory:
    """Keeps only last N turns."""

    def __init__(self, window_size: int = 3) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be > 0")
        self._window = deque(maxlen=window_size)

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        self._window.append(Turn(user_message=user_message, assistant_message=assistant_message))

    def get_context(self) -> list[Message]:
        out: list[Message] = []
        for turn in self._window:
            out.append(Message(role="user", content=turn.user_message))
            out.append(Message(role="assistant", content=turn.assistant_message))
        return out

    def clear(self) -> None:
        self._window.clear()


class SummaryMemory:
    """Maintains running compact summary plus recent turns."""

    def __init__(self, recent_turns: int = 2) -> None:
        if recent_turns < 0:
            raise ValueError("recent_turns must be >= 0")
        self._recent_turns = recent_turns
        self._all_turns: list[Turn] = []
        self._summary: str = ""

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        turn = Turn(user_message=user_message, assistant_message=assistant_message)
        self._all_turns.append(turn)
        self._summary = self._build_summary(self._all_turns)

    def get_context(self) -> list[Message]:
        context: list[Message] = []
        if self._summary:
            context.append(Message(role="system", content=f"Conversation summary: {self._summary}"))

        recent = self._all_turns[-self._recent_turns :] if self._recent_turns > 0 else []
        for turn in recent:
            context.append(Message(role="user", content=turn.user_message))
            context.append(Message(role="assistant", content=turn.assistant_message))
        return context

    def clear(self) -> None:
        self._all_turns.clear()
        self._summary = ""

    @staticmethod
    def _build_summary(turns: list[Turn]) -> str:
        if not turns:
            return ""
        snippets = [f"U:{t.user_message[:40]} | A:{t.assistant_message[:40]}" for t in turns[-4:]]
        return " ; ".join(snippets)
