class RetryExhaustedError(RuntimeError):
    """Raised when retry attempts are exhausted."""


class RetryableLLMError(Exception):
    """Represents transient failures (429, timeout, 5xx)."""


class NonRetryableLLMError(Exception):
    """Represents permanent failures (400, auth errors, validation)."""
