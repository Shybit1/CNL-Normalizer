"""
constraint_result.py — Immutable result object from the Constraint Extractor.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from .constraint_types import Constraint


@dataclass(frozen=True)
class ConstraintResult:
    """
    Immutable result of constraint extraction.

    Attributes:
        success: Whether extraction succeeded.
        constraints: List of typed Constraint objects.
        errors: List of error messages (empty on success).
    """
    success: bool
    constraints: List[Constraint] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert all constraints to dictionary list."""
        return [c.to_dict() for c in self.constraints]

    def __repr__(self) -> str:
        status = "OK" if self.success else "FAIL"
        return f"ConstraintResult({status}, {len(self.constraints)} constraints)"
