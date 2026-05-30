from __future__ import annotations

import re


class SimpleWhitespaceTokenCounter:
    """Interview-safe token counter approximation."""

    def count_text_tokens(self, text: str) -> int:
        if not text.strip():
            return 0
        # Approximate tokenization: words + punctuation groups.
        return len(re.findall(r"\w+|[^\w\s]", text))
