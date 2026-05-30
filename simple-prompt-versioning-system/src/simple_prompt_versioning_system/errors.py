class PromptNotFoundError(KeyError):
    """Raised when prompt or version is not found."""


class PromptValidationError(ValueError):
    """Raised for invalid prompt inputs."""
