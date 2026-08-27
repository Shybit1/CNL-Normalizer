"""
extractor.py — Main constraint extraction logic.

Receives ParseResult from the Grammar Parser and produces ConstraintResult.
Recognizes constraint patterns in slots and produces typed constraint objects.

Per PRD §23-28:
- Recognizes a closed constraint language
- Validates constraint structure
- Detects duplicates and conflicts
- Resolves entities (must exist in known dictionaries)
- Does NOT perform feasibility analysis
"""

import sys
import os
from typing import List

# Load entity dictionaries from normalizer
_VALID_WAYPOINTS = None


def _load_entities():
    """Lazy-load entity dictionaries from the CNL Normalizer."""
    global _VALID_WAYPOINTS
    if _VALID_WAYPOINTS is not None:
        return

    try:
        from normalizer.entities import WAYPOINTS
        _VALID_WAYPOINTS = frozenset(WAYPOINTS.keys())
    except ImportError:
        # Fallback
        _VALID_WAYPOINTS = frozenset({
            'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
            'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima',
            'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo',
            'sierra', 'tango', 'uniform', 'victor', 'whiskey',
            'xray', 'yankee', 'zulu',
            'sector', 'zone', 'point', 'waypoint', 'home', 'base',
            'rally', 'landing'
        })


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
from grammar_parser import ParseResult


def extract_constraints(parse_result: ParseResult) -> ConstraintResult:
    """
    Extract typed constraints from a ParseResult.

    The extractor looks for constraint patterns in the parse result slots
    and produces a list of typed constraint objects.

    Args:
        parse_result: Output from the Grammar Parser.

    Returns:
        ConstraintResult with typed constraints or errors.
    """
    if not parse_result.success:
        return ConstraintResult(
            success=False,
            errors=["Cannot extract constraints from failed parse"],
        )

    constraints: List[Constraint] = []
    errors: List[str] = []

    slots = parse_result.slots or {}

    # Load entities for validation
    _load_entities()

    # Check for MAX_G_FORCE constraint
    # Pattern: slots contains "max_g" or "max_g_force"
    for key in ['max_g', 'max_g_force']:
        if key in slots:
            try:
                value = float(slots[key])
                if value <= 0:
                    errors.append(f"Max G-force must be positive, got {value}")
                else:
                    constraints.append(MaxGForceConstraint(value))
            except (ValueError, TypeError):
                errors.append(f"Invalid max G-force value: {slots[key]}")

    # Check for NO_FLY_ZONE constraints
    # Pattern: slots contains "no_fly_zones" or "avoiding" or "avoid"
    for key in ['no_fly_zones', 'avoiding', 'avoid']:
        if key in slots:
            zones = slots[key]
            if isinstance(zones, str):
                zones = [zones]
            elif not isinstance(zones, list):
                zones = [str(zones)]

            for zone in zones:
                zone_lower = zone.lower() if isinstance(zone, str) else str(zone).lower()
                # Validate zone exists
                if zone_lower not in _VALID_WAYPOINTS:
                    errors.append(f"Unknown no-fly zone: {zone}")
                else:
                    constraints.append(NoFlyZoneConstraint(zone_lower))

    # Check for TIME constraints
    # Pattern: slots contains "time", "within", "by"
    if 'within' in slots:
        try:
            value = float(slots['within'])
            unit = slots.get('within_unit', 'SECONDS')
            if unit.upper() not in ('SECONDS', 'MINUTES', 'HOURS'):
                errors.append(f"Invalid time unit: {unit}")
            else:
                constraints.append(
                    TimeConstraint(
                        constraint_type='WITHIN',
                        value=value,
                        unit=unit.upper(),
                    )
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid within time value: {slots['within']}")

    if 'by' in slots:
        try:
            value = slots['by']
            constraints.append(
                TimeConstraint(
                    constraint_type='BY',
                    value=value,
                    unit=None,
                )
            )
        except (ValueError, TypeError):
            errors.append(f"Invalid by time value: {slots['by']}")

    # Check for MAX_SPEED constraint
    if 'max_speed' in slots:
        try:
            value = float(slots['max_speed'])
            unit = slots.get('speed_unit', 'KMH')
            if unit.upper() not in ('KMH', 'MPH', 'MPS', 'KNOTS'):
                errors.append(f"Invalid speed unit: {unit}")
            else:
                constraints.append(
                    MaxSpeedConstraint(value, unit.upper())
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid max speed value: {slots['max_speed']}")

    # Check for MIN_SPEED constraint
    if 'min_speed' in slots:
        try:
            value = float(slots['min_speed'])
            unit = slots.get('speed_unit', 'KMH')
            if unit.upper() not in ('KMH', 'MPH', 'MPS', 'KNOTS'):
                errors.append(f"Invalid speed unit: {unit}")
            else:
                constraints.append(
                    MinSpeedConstraint(value, unit.upper())
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid min speed value: {slots['min_speed']}")

    # Check for MAX_ALTITUDE constraint
    if 'max_altitude' in slots:
        try:
            value = float(slots['max_altitude'])
            unit = slots.get('altitude_unit', 'METERS')
            if unit.upper() not in ('METERS', 'FEET'):
                errors.append(f"Invalid altitude unit: {unit}")
            else:
                constraints.append(
                    MaxAltitudeConstraint(value, unit.upper())
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid max altitude value: {slots['max_altitude']}")

    # Check for MIN_ALTITUDE constraint
    if 'min_altitude' in slots:
        try:
            value = float(slots['min_altitude'])
            unit = slots.get('altitude_unit', 'METERS')
            if unit.upper() not in ('METERS', 'FEET'):
                errors.append(f"Invalid altitude unit: {unit}")
            else:
                constraints.append(
                    MinAltitudeConstraint(value, unit.upper())
                )
        except (ValueError, TypeError):
            errors.append(f"Invalid min altitude value: {slots['min_altitude']}")

    # Detect duplicate constraint types
    constraint_types_seen = {}
    for constraint in constraints:
        ctype = type(constraint).__name__
        constraint_types_seen[ctype] = constraint_types_seen.get(ctype, 0) + 1

    for ctype, count in constraint_types_seen.items():
        if count > 1 and ctype not in ('NoFlyZoneConstraint',):  # Multiple no-fly zones are OK
            errors.append(f"Duplicate constraint type: {ctype}")

    # Detect conflicts (max/min pairs)
    has_max_alt = any(isinstance(c, MaxAltitudeConstraint) for c in constraints)
    has_min_alt = any(isinstance(c, MinAltitudeConstraint) for c in constraints)
    if has_max_alt and has_min_alt:
        max_alt = next(c.value for c in constraints if isinstance(c, MaxAltitudeConstraint))
        min_alt = next(c.value for c in constraints if isinstance(c, MinAltitudeConstraint))
        if min_alt > max_alt:
            errors.append(
                f"Constraint conflict: min_altitude ({min_alt}) > max_altitude ({max_alt})"
            )

    has_max_speed = any(isinstance(c, MaxSpeedConstraint) for c in constraints)
    has_min_speed = any(isinstance(c, MinSpeedConstraint) for c in constraints)
    if has_max_speed and has_min_speed:
        max_speed = next(c.value for c in constraints if isinstance(c, MaxSpeedConstraint))
        min_speed = next(c.value for c in constraints if isinstance(c, MinSpeedConstraint))
        if min_speed > max_speed:
            errors.append(
                f"Constraint conflict: min_speed ({min_speed}) > max_speed ({max_speed})"
            )

    success = len(errors) == 0
    return ConstraintResult(
        success=success,
        constraints=constraints,
        errors=errors,
    )
