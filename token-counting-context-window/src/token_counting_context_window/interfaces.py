from __future__ import annotations

from typing import Protocol


class TokenCounter(Protocol):
    def count_text_tokens(self, text: str) -> int:
        ...
