from retry_exponential_backoff_llm.errors import (
    NonRetryableLLMError,
    RetryExhaustedError,
    RetryableLLMError,
)
from retry_exponential_backoff_llm.models import RetryConfig
from retry_exponential_backoff_llm.retry import RetryExecutor


def test_retries_then_succeeds() -> None:
    attempts = {"count": 0}
    sleeps: list[float] = []

    def op() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RetryableLLMError("temporary")
        return "ok"

    executor = RetryExecutor(
        RetryConfig(max_attempts=4, initial_delay_seconds=1.0, backoff_multiplier=2.0, max_delay_seconds=5.0),
        sleep_fn=sleeps.append,
    )

    result = executor.run(op)

    assert result == "ok"
    assert attempts["count"] == 3
    assert sleeps == [1.0, 2.0]


def test_exhausted_retries_raises() -> None:
    sleeps: list[float] = []

    def op() -> str:
        raise RetryableLLMError("still failing")

    executor = RetryExecutor(
        RetryConfig(max_attempts=3, initial_delay_seconds=0.5, backoff_multiplier=2.0, max_delay_seconds=2.0),
        sleep_fn=sleeps.append,
    )

    try:
        executor.run(op)
        assert False, "expected RetryExhaustedError"
    except RetryExhaustedError:
        pass

    assert sleeps == [0.5, 1.0]


def test_non_retryable_error_fails_fast() -> None:
    sleeps: list[float] = []

    def op() -> str:
        raise NonRetryableLLMError("bad request")

    executor = RetryExecutor(RetryConfig(max_attempts=5), sleep_fn=sleeps.append)

    try:
        executor.run(op)
        assert False, "expected NonRetryableLLMError"
    except NonRetryableLLMError:
        pass

    assert sleeps == []


def test_invalid_config_raises() -> None:
    try:
        RetryExecutor(RetryConfig(max_attempts=0))
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "max_attempts" in str(exc)
