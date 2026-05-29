from __future__ import annotations

from typing import Protocol

from .models import Message


class ConversationMemory(Protocol):
    def add_turn(self, user_message: str, assistant_message: str) -> None:
        ...

    def get_context(self) -> list[Message]:
        ...

    def clear(self) -> None:
        ...
