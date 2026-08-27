"""
constraint_types.py — Typed constraint objects for Layer 1.

Each constraint is a separate, immutable dataclass representing an explicit
operator restriction. The extractor produces these from parse results.

Per PRD §25: Typed objects include:
- NoFlyZoneConstraint
- MaxGForceConstraint
- TimeConstraint
- MaxSpeedConstraint
- MinSpeedConstraint
- MaxAltitudeConstraint
- MinAltitudeConstraint
"""

from dataclasses import dataclass
from typing import Any, Optional
from abc import ABC, abstractmethod


class Constraint(ABC):
    """Base class for all typed constraints."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert constraint to dictionary representation."""
        pass


@dataclass(frozen=True)
class NoFlyZoneConstraint(Constraint):
    """
    No-fly-zone constraint: operator specifies zones to avoid.
    Entity must be a known waypoint/zone identifier.
    """
    entity: str  # e.g., "ALPHA", "SECTOR_BRAVO"

    def to_dict(self) -> dict:
        return {"type": "no_fly_zone", "entity": self.entity}


@dataclass(frozen=True)
class MaxGForceConstraint(Constraint):
    """Maximum G-force constraint during maneuvers."""
    value: float

    def to_dict(self) -> dict:
        return {"type": "max_g_force", "value": self.value}


@dataclass(frozen=True)
class TimeConstraint(Constraint):
    """
    Time constraint: e.g., "WITHIN 5 MINUTES" or "BY 14:30".
    
    Attributes:
        constraint_type: 'WITHIN' or 'BY'
        value: numeric value (duration or deadline)
        unit: time unit ('SECONDS', 'MINUTES', 'HOURS') for WITHIN; None for BY
    """
    constraint_type: str  # 'WITHIN' or 'BY'
    value: float
    unit: Optional[str] = None  # SECONDS, MINUTES, HOURS for WITHIN

    def to_dict(self) -> dict:
        return {
            "type": "time",
            "constraint_type": self.constraint_type,
            "value": self.value,
            "unit": self.unit,
        }


@dataclass(frozen=True)
class MaxSpeedConstraint(Constraint):
    """Maximum speed constraint."""
    value: float
    unit: str  # KMH, MPH, MPS, KNOTS

    def to_dict(self) -> dict:
        return {"type": "max_speed", "value": self.value, "unit": self.unit}


@dataclass(frozen=True)
class MinSpeedConstraint(Constraint):
    """Minimum speed constraint."""
    value: float
    unit: str  # KMH, MPH, MPS, KNOTS

    def to_dict(self) -> dict:
        return {"type": "min_speed", "value": self.value, "unit": self.unit}


@dataclass(frozen=True)
class MaxAltitudeConstraint(Constraint):
    """Maximum altitude constraint."""
    value: float
    unit: str  # METERS, FEET

    def to_dict(self) -> dict:
        return {"type": "max_altitude", "value": self.value, "unit": self.unit}


@dataclass(frozen=True)
class MinAltitudeConstraint(Constraint):
    """Minimum altitude constraint."""
    value: float
    unit: str  # METERS, FEET

    def to_dict(self) -> dict:
        return {"type": "min_altitude", "value": self.value, "unit": self.unit}
