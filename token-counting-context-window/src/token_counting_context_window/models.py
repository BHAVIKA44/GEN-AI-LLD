from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ContextBuildResult:
    messages: list[ChatMessage]
    used_tokens: int
    dropped_messages: int
