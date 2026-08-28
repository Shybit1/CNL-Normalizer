"""
cfr_types.py — Data structures for Command Formal Representation.

The CFR is the canonical output of Layer 1.
It contains everything Layer 2 needs to know about the operator's request,
without requiring any understanding of natural language.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CFR:
    """
    Command Formal Representation — the boundary artifact between Layer 1 and Layer 2.

    Attributes:
        schema_version: Version of CFR structure (e.g., "1.0")
        grammar_version: Version of grammar that parsed the command
        constraint_version: Version of constraint vocabulary
        timestamp: When the command was processed (ISO 8601)
        intent: Intent type (e.g., "ALTITUDE_CHANGE", "WAYPOINT_NAVIGATION")
        parameters: Mission parameters (e.g., target_altitude=500, unit="meters")
        constraints: Operational restrictions (max_g=2.0, no_fly_zones=["ALPHA"], etc.)
        mission_phase: Explicit mission phase if provided by operator; null otherwise
        confidence: Confidence score (1.0 = maximum confidence)
        metadata: Optional extended metadata
    """
    schema_version: str
    grammar_version: str
    constraint_version: str
    timestamp: str  # ISO 8601
    intent: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    mission_phase: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert CFR to dictionary representation."""
        return asdict(self)

    def __repr__(self) -> str:
        return (
            f"CFR(intent={self.intent}, confidence={self.confidence}, "
            f"params={len(self.parameters)}, constraints={len(self.constraints)})"
        )
