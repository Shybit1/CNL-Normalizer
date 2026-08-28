"""
generator.py — CFR Generator (Layer 1, Stage 4)

Converts ParseResult + ConstraintResult → CFR candidate.

Maps AST slots to CFR parameters, assembles constraints into canonical form,
and constructs the command formal representation ready for validation.

Per PRD §29-34: The generator does NOT perform feasibility checks.
It only structures what was parsed.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional

from grammar_parser import ParseResult, Intent
from constraint_extractor import ConstraintResult
from .cfr_types import CFR


# CFR schema and grammar versions
CFR_SCHEMA_VERSION = "1.0"
GRAMMAR_VERSION = "1.0"
CONSTRAINT_VERSION = "1.0"


def generate_cfr(
    parse_result: ParseResult,
    constraint_result: Optional[ConstraintResult] = None,
) -> CFR:
    """
    Generate a CFR from a ParseResult and optional ConstraintResult.

    Args:
        parse_result: Output from Grammar Parser.
        constraint_result: Output from Constraint Extractor (optional).

    Returns:
        CFR candidate ready for schema validation.

    Raises:
        ValueError: If parse_result is not successful.
    """
    if not parse_result.success:
        raise ValueError(
            f"Cannot generate CFR from failed parse. Errors: {parse_result.errors}"
        )

    timestamp = datetime.now(timezone.utc).isoformat()
    intent = parse_result.intent
    slots = parse_result.slots or {}

    # Map slots to CFR parameters based on intent
    parameters = _map_slots_to_parameters(intent, slots)

    # Extract constraints from constraint_result
    constraints = {}
    if constraint_result and constraint_result.success:
        constraints = _extract_constraints_dict(constraint_result)

    # Mission phase: only set if explicitly provided in slots
    mission_phase = slots.get("mission_phase", None)

    # Build CFR
    cfr = CFR(
        schema_version=CFR_SCHEMA_VERSION,
        grammar_version=GRAMMAR_VERSION,
        constraint_version=CONSTRAINT_VERSION,
        timestamp=timestamp,
        intent=intent,
        parameters=parameters,
        constraints=constraints,
        mission_phase=mission_phase,
        confidence=1.0,  # Initially maximum; gate may adjust
        metadata={},
    )

    return cfr


def _map_slots_to_parameters(intent: str, slots: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map parsed slots to canonical CFR parameters based on intent type.

    Per PRD §32: Parameters describe the target of the mission.
    Each intent type has its own parameter schema.
    """
    params = {}

    if intent == Intent.ALTITUDE_CHANGE.value:
        # ALTITUDE_CHANGE: target_altitude, direction (up/down), unit
        if "target_altitude" in slots:
            params["target_altitude"] = slots["target_altitude"]
        if "direction" in slots:
            params["direction"] = slots["direction"]
        if "unit" in slots:
            params["unit"] = slots["unit"].upper()

    elif intent == Intent.WAYPOINT_NAVIGATION.value:
        # WAYPOINT_NAVIGATION: target, optional waypoint_type
        if "target" in slots:
            params["target"] = slots["target"].upper()
        if "waypoint_type" in slots:
            params["waypoint_type"] = slots["waypoint_type"].upper()

    elif intent == Intent.FORMATION_CHANGE.value:
        # FORMATION_CHANGE: formation name
        if "formation" in slots:
            params["formation"] = slots["formation"].upper()

    elif intent == Intent.HOLD_LOITER.value:
        # HOLD_LOITER: optional target_altitude, optional duration
        if "target_altitude" in slots:
            params["target_altitude"] = slots["target_altitude"]
        if "unit" in slots:
            params["unit"] = slots["unit"].upper()
        if "duration" in slots:
            params["duration"] = slots["duration"]
        if "duration_unit" in slots:
            params["duration_unit"] = slots["duration_unit"].upper()

    elif intent == Intent.ABORT_RTL.value:
        # ABORT_RTL: action type (rtl, return_home, abort)
        if "action" in slots:
            params["action"] = slots["action"].upper()

    return params


def _extract_constraints_dict(constraint_result: ConstraintResult) -> Dict[str, Any]:
    """
    Extract typed constraints from ConstraintResult into dict form.

    Per PRD §33: Constraints are kept separate from objective parameters.
    This gives Layer 2 a clean separation between what to accomplish vs.
    how it may be accomplished.
    """
    constraints_dict = {}

    if not constraint_result.constraints:
        return constraints_dict

    # Group constraints by type
    max_g_force_vals = []
    no_fly_zones = []
    time_constraints = []
    max_speed_vals = []
    min_speed_vals = []
    max_altitude_vals = []
    min_altitude_vals = []

    for constraint in constraint_result.constraints:
        constraint_dict = constraint.to_dict()
        ctype = constraint_dict.get("type")

        if ctype == "max_g_force":
            max_g_force_vals.append(constraint_dict.get("value"))
        elif ctype == "no_fly_zone":
            no_fly_zones.append(constraint_dict.get("entity"))
        elif ctype == "time":
            time_constraints.append(constraint_dict)
        elif ctype == "max_speed":
            max_speed_vals.append(constraint_dict)
        elif ctype == "min_speed":
            min_speed_vals.append(constraint_dict)
        elif ctype == "max_altitude":
            max_altitude_vals.append(constraint_dict)
        elif ctype == "min_altitude":
            min_altitude_vals.append(constraint_dict)

    # Assemble into constraints dict
    if max_g_force_vals:
        constraints_dict["max_g_force"] = max_g_force_vals[0] if len(max_g_force_vals) == 1 else max_g_force_vals

    if no_fly_zones:
        constraints_dict["no_fly_zones"] = no_fly_zones

    if time_constraints:
        constraints_dict["time"] = time_constraints[0] if len(time_constraints) == 1 else time_constraints

    if max_speed_vals:
        constraints_dict["max_speed"] = max_speed_vals[0] if len(max_speed_vals) == 1 else max_speed_vals

    if min_speed_vals:
        constraints_dict["min_speed"] = min_speed_vals[0] if len(min_speed_vals) == 1 else min_speed_vals

    if max_altitude_vals:
        constraints_dict["max_altitude"] = max_altitude_vals[0] if len(max_altitude_vals) == 1 else max_altitude_vals

    if min_altitude_vals:
        constraints_dict["min_altitude"] = min_altitude_vals[0] if len(min_altitude_vals) == 1 else min_altitude_vals

    return constraints_dict
