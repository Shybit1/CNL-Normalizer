"""
Canonical Aero — Confidence & Ambiguity Gate (Layer 1, Component 6)

Deterministic confidence scoring and ambiguity detection.

Per PRD §38-40:
Confidence should NOT be ML-generated probability.
Instead, derive confidence from deterministic evidence:
  - Grammar matched: YES/NO
  - Required parameters present: YES/NO
  - All entities resolved: YES/NO
  - Units canonical: YES/NO
  - No contradictions: YES/NO
  - No unsupported clauses: YES/NO
  - Schema valid: YES/NO

Ambiguity must stop the pipeline. If uncertain, operator gets clarification.

See PRD §38-40.
"""

from .scorer import score_confidence
from .ambiguity import detect_ambiguity
from .gate_result import GateResult

__all__ = [
    "score_confidence",
    "detect_ambiguity",
    "GateResult",
]
