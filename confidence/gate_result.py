"""
gate_result.py — Result type for confidence/ambiguity gate.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(frozen=True)
class GateResult:
    """
    Result of confidence and ambiguity scoring.
    
    Attributes:
        accept: Whether to accept (True) or reject/clarify (False)
        confidence: Computed confidence score (0.0 to 1.0)
        ambiguities: List of detected ambiguities (empty if none)
        evidence: Dict of evidence factors and their values
        reasons: List of human-readable reasons for decision
    """
    accept: bool
    confidence: float
    ambiguities: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        status = "ACCEPT" if self.accept else "REJECT/CLARIFY"
        return (
            f"GateResult({status}, confidence={self.confidence:.2f}, "
            f"ambiguities={len(self.ambiguities)})"
        )
