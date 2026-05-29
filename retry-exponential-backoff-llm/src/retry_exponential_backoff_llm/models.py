from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int = 4
    initial_delay_seconds: float = 0.2
    backoff_multiplier: float = 2.0
    max_delay_seconds: float = 5.0
    jitter_ratio: float = 0.0

    def validate(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be > 0")
        if self.initial_delay_seconds < 0:
            raise ValueError("initial_delay_seconds must be >= 0")
        if self.backoff_multiplier < 1:
            raise ValueError("backoff_multiplier must be >= 1")
        if self.max_delay_seconds < 0:
            raise ValueError("max_delay_seconds must be >= 0")
        if not (0 <= self.jitter_ratio <= 1):
            raise ValueError("jitter_ratio must be between 0 and 1")
