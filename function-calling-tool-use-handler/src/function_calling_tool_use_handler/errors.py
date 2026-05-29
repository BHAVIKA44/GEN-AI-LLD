class ToolNotFoundError(KeyError):
    """Raised when requested tool is not registered."""


class ToolValidationError(ValueError):
    """Raised when tool arguments fail validation."""
