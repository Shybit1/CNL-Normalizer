"""
parser.py — Main entry point for the Grammar Parser.

Integrates the lexer and visitor into a single parse() function.
"""

from .visitor import CommandVisitor
from .parse_result import ParseResult

# Singleton visitor — stateless and thread-safe
_visitor = CommandVisitor()


def parse(text: str) -> ParseResult:
    """
    Parse a canonical normalized drone command and return a ParseResult.

    This is the main entry point for the grammar parser layer.
    It receives output from the CNL Normalizer (uppercase, whitespace-normalized).

    Args:
        text: Canonical command string (e.g., "CLIMB TO 500 METERS").

    Returns:
        ParseResult with success flag, intent, slots, and any errors.
    """
    return _visitor.parse(text)