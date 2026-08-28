"""
errors.py — Exception types for CFR generation and validation.
"""


class CFRError(Exception):
    """Base exception for CFR-related errors."""
    pass


class CFRGenerationError(CFRError):
    """Raised when CFR generation fails."""
    pass


class CFRValidationError(CFRError):
    """Raised when CFR validation fails."""
    pass


class SchemaLoadError(CFRError):
    """Raised when schema.json cannot be loaded."""
    pass
