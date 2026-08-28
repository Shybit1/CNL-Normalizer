"""
scorer.py — Deterministic confidence scoring.

Computes confidence from evidence, not from ML probability.

Per PRD §38-39:
A deterministic parser often has a stronger property than a model probability.
Instead of "I am 87% confident this means CLIMB",
we can know:
  - Grammar matched: YES
  - Required altitude: YES
  - Unit: YES
  - Entity resolution: YES
  - Ambiguity: NO
  - Constraint conflict: NO
  - Schema: VALID

This is much more defensible for a safety-oriented system.
"""

from typing import Dict, Any, Optional

from grammar_parser import ParseResult, Intent
from constraint_extractor import ConstraintResult
from cfr import CFR


def score_confidence(
    parse_result: Optional[ParseResult] = None,
    constraint_result: Optional[ConstraintResult] = None,
    cfr: Optional[CFR] = None,
    schema_valid: bool = False,
) -> tuple[float, Dict[str, Any]]:
    """
    Compute confidence score from deterministic evidence.
    
    Args:
        parse_result: Result from Grammar Parser
        constraint_result: Result from Constraint Extractor
        cfr: Generated CFR (if available)
        schema_valid: Whether CFR passed schema validation
    
    Returns:
        Tuple of (confidence_score: float, evidence: Dict[str, Any])
        confidence_score ranges from 0.0 to 1.0
        evidence dict contains all factors considered
    """
    evidence: Dict[str, Any] = {}
    score = 0.0
    max_score = 0.0

    # Factor 1: Grammar parsing success
    max_score += 1.0
    if parse_result and parse_result.success:
        evidence["grammar_matched"] = True
        score += 1.0
    else:
        evidence["grammar_matched"] = False
        if parse_result:
            evidence["parse_errors"] = parse_result.errors

    # Factor 2: Required parameters present
    max_score += 1.0
    required_params = _get_required_parameters(parse_result)
    if parse_result and parse_result.slots:
        slots = parse_result.slots
        all_required_present = all(param in slots for param in required_params)
        evidence["required_parameters_present"] = all_required_present
        if all_required_present:
            score += 1.0
    else:
        evidence["required_parameters_present"] = False

    # Factor 3: Units canonical
    max_score += 1.0
    if parse_result and parse_result.slots:
        unit = parse_result.slots.get("unit") or parse_result.slots.get("duration_unit")
        if unit:
            is_canonical = unit.isupper()
            evidence["units_canonical"] = is_canonical
            if is_canonical:
                score += 1.0
        else:
            evidence["units_canonical"] = True  # No units required
            score += 1.0
    else:
        evidence["units_canonical"] = True
        score += 1.0

    # Factor 4: Entity resolution (waypoints, formations, zones)
    max_score += 1.0
    if parse_result and parse_result.slots:
        entity_resolved = _check_entity_resolution(parse_result)
        evidence["entities_resolved"] = entity_resolved
        if entity_resolved:
            score += 1.0
    else:
        evidence["entities_resolved"] = True
        score += 1.0

    # Factor 5: No constraint conflicts
    max_score += 1.0
    if constraint_result:
        no_conflicts = constraint_result.success and len(constraint_result.errors) == 0
        evidence["no_constraint_conflicts"] = no_conflicts
        if no_conflicts:
            score += 1.0
        else:
            evidence["constraint_errors"] = constraint_result.errors
    else:
        evidence["no_constraint_conflicts"] = True
        score += 1.0

    # Factor 6: Schema validation
    max_score += 1.0
    evidence["schema_valid"] = schema_valid
    if schema_valid:
        score += 1.0

    # Compute normalized confidence (0.0 to 1.0)
    confidence = score / max_score if max_score > 0 else 0.0
    evidence["score"] = score
    evidence["max_score"] = max_score

    return confidence, evidence


def _get_required_parameters(parse_result: Optional[ParseResult]) -> list[str]:
    """
    Determine required parameters based on intent.
    
    Per PRD §32: each intent type has specific required parameters.
    """
    if not parse_result or not parse_result.intent:
        return []

    intent = parse_result.intent

    if intent == Intent.ALTITUDE_CHANGE.value:
        return ["target_altitude", "direction", "unit"]
    elif intent == Intent.WAYPOINT_NAVIGATION.value:
        return ["target"]
    elif intent == Intent.FORMATION_CHANGE.value:
        return ["formation"]
    elif intent == Intent.HOLD_LOITER.value:
        return []  # LOITER can be minimal
    elif intent == Intent.ABORT_RTL.value:
        return ["action"]
    else:
        return []


def _check_entity_resolution(parse_result: ParseResult) -> bool:
    """
    Check if all referenced entities (waypoints, formations, zones) are known.
    
    Returns True if all entities are recognized or no entities are referenced.
    """
    if not parse_result.slots:
        return True

    slots = parse_result.slots

    # Check waypoint/navigation targets
    if "target" in slots:
        target = slots["target"]
        known_waypoints = {
            'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
            'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima',
            'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo',
            'sierra', 'tango', 'uniform', 'victor', 'whiskey',
            'xray', 'yankee', 'zulu',
            'sector', 'zone', 'point', 'waypoint', 'home', 'base',
            'rally', 'landing'
        }
        if target.lower() not in known_waypoints:
            return False

    # Check formation names
    if "formation" in slots:
        formation = slots["formation"]
        known_formations = {
            'wedge', 'diamond', 'line', 'echelon', 'staggered',
            'trail', 'column', 'arrowhead', 'box', 'v', 'vic',
            'finger', 'four'
        }
        if formation.lower() not in known_formations:
            return False

    return True
