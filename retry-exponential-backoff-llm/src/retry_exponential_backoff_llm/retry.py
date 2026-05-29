from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar

from .errors import NonRetryableLLMError, RetryExhaustedError, RetryableLLMError
from .models import RetryConfig

T = TypeVar("T")


class RetryExecutor:
    def __init__(
        self,
        config: RetryConfig,
        sleep_fn: Callable[[float], None] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        config.validate()
        self._config = config
        self._sleep = sleep_fn or time.sleep
        self._rng = rng or random.Random()

    def run(self, operation: Callable[[], T]) -> T:
        attempt = 0
        delay = self._config.initial_delay_seconds
        last_error: Exception | None = None

        while attempt < self._config.max_attempts:
            attempt += 1
            try:
                return operation()
            except NonRetryableLLMError:
                raise
            except RetryableLLMError as exc:
                last_error = exc
                if attempt >= self._config.max_attempts:
                    break

                sleep_for = self._with_jitter(delay)
                self._sleep(sleep_for)
                delay = min(delay * self._config.backoff_multiplier, self._config.max_delay_seconds)

        raise RetryExhaustedError(f"operation failed after {self._config.max_attempts} attempts") from last_error

    def _with_jitter(self, base_delay: float) -> float:
        jitter = base_delay * self._config.jitter_ratio
        if jitter == 0:
            return base_delay
        return max(0.0, base_delay + self._rng.uniform(-jitter, jitter))
