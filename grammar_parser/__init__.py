"""
Canonical Aero — Grammar Parser (Layer 1, Component 2)

ANTLR4-based deterministic syntactic parser for canonical drone commands.
Receives normalized commands from the CNL Normalizer and returns ParseResult objects.
"""

from .parser import parse
from .parse_result import ParseResult
from .intent_mapper import Intent

__all__ = ["parse", "ParseResult", "Intent"]