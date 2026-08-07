"""
exceptions.py — Custom exceptions for the Grammar Parser.
"""


class GrammarParserError(Exception):
    """Base exception for grammar parser errors."""
    pass


class TokenizationError(GrammarParserError):
    """Raised when tokenization fails (e.g., unknown characters)."""
    pass


class ParseError(GrammarParserError):
    """Raised when the command doesn't match any grammar rule."""
    pass


class ValidationError(GrammarParserError):
    """Raised when dynamic validation fails (invalid waypoint, formation, etc.)."""
    pass


class InputLimitError(GrammarParserError):
    """Raised when input exceeds token or character limits."""
    pass