class TemplateValidationError(ValueError):
    """Raised when template syntax is invalid."""


class MissingVariableError(KeyError):
    """Raised when required template variable is missing."""
