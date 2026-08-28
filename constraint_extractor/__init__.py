"""
Canonical Aero — Constraint Extractor (Layer 1, Component 3)

Constraint extraction sits between the Grammar Parser (syntactic boundary)
and CFR generation. Its question is:

> What restrictions did the operator explicitly impose on the requested mission?

The extractor recognizes a closed constraint language and produces typed constraint
objects. It validates structure, detects duplicates/conflicts, and resolves entities.
It does NOT perform mission feasibility analysis (that belongs in Layer 2).

See PRD §23-28.
"""

from .extractor import extract_constraints
from .constraint_types import (
    Constraint,
    MaxGForceConstraint,
    NoFlyZoneConstraint,
    TimeConstraint,
    MaxSpeedConstraint,
    MinSpeedConstraint,
    MaxAltitudeConstraint,
    MinAltitudeConstraint,
)
from .constraint_result import ConstraintResult

__all__ = [
    "extract_constraints",
    "Constraint",
    "MaxGForceConstraint",
    "NoFlyZoneConstraint",
    "TimeConstraint",
    "MaxSpeedConstraint",
    "MinSpeedConstraint",
    "MaxAltitudeConstraint",
    "MinAltitudeConstraint",
    "ConstraintResult",
]
