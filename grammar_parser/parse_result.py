"""
parse_result.py — Immutable result object from the Grammar Parser.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any


@dataclass(frozen=True)
class ParseResult:
    """
    Immutable result of parsing a drone command.

    Attributes:
        success: Whether the parse succeeded (valid command syntax).
        intent: The recognized intent type (e.g., ALTITUDE_CHANGE).
        slots: Named values extracted from the command (e.g., altitude=500).
        parse_tree: Reference to the parse tree structure.
        errors: List of error messages (empty on success).
    """
    success: bool
    intent: Optional[str] = None
    slots: Dict[str, Any] = field(default_factory=dict)
    parse_tree: Optional[Any] = None
    errors: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        status = "OK" if self.success else "FAIL"
        return f"ParseResult({status}, intent={self.intent}, slots={self.slots})"