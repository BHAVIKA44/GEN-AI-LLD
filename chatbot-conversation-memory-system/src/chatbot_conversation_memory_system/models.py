from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class Turn:
    user_message: str
    assistant_message: str
