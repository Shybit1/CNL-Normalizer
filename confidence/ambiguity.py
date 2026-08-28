"""
ambiguity.py — Ambiguity detection.

Per PRD §40: Ambiguity must stop the pipeline.
If the command is ambiguous, Layer 1 returns a clarification request
instead of a CFR.

Example:
  "Go to Alpha."
  If ALPHA could be both a waypoint and a sector:
    → "Do you mean waypoint ALPHA or sector ALPHA?"
"""

from typing import List, Optional, Dict, Any

from grammar_parser import ParseResult, Intent
from constraint_extractor import ConstraintResult


def detect_ambiguity(
    parse_result: Optional[ParseResult] = None,
    constraint_result: Optional[ConstraintResult] = None,
) -> List[str]:
    """
    Detect ambiguities in the parsed command and constraints.
    
    Returns a list of ambiguity descriptions.
    Empty list = no ambiguities.
    Non-empty list = ambiguities detected; operator clarification needed.
    
    Args:
        parse_result: Result from Grammar Parser
        constraint_result: Result from Constraint Extractor
    
    Returns:
        List of ambiguity strings (empty if no ambiguities found)
    """
    ambiguities: List[str] = []

    # Ambiguity 1: Entity could be multiple types
    if parse_result and parse_result.slots:
        ambiguities.extend(_check_entity_ambiguity(parse_result))

    # Ambiguity 2: Conflicting constraints
    if constraint_result and not constraint_result.success:
        ambiguities.extend(constraint_result.errors)

    # Ambiguity 3: Multiple constraint values for same type (detected by extractor)
    # Already handled by constraint extractor's duplicate detection

    # Ambiguity 4: Unclear time references
    if parse_result and parse_result.slots:
        ambiguities.extend(_check_time_ambiguity(parse_result))

    # Ambiguity 5: Unclear navigation target
    if parse_result and parse_result.slots:
        ambiguities.extend(_check_navigation_ambiguity(parse_result))

    return ambiguities


def _check_entity_ambiguity(parse_result: ParseResult) -> List[str]:
    """
    Check if entities referenced could be multiple types.
    
    Example: "ALPHA" could be WAYPOINT ALPHA, SECTOR ALPHA, etc.
    """
    ambiguities: List[str] = []
    slots = parse_result.slots or {}

    # If no waypoint_type specified, entity could be ambiguous
    if "target" in slots and "waypoint_type" not in slots:
        target = slots["target"]
        # This is potentially ambiguous; require operator to clarify
        ambiguities.append(
            f"Entity '{target}' is ambiguous. Please specify the type (e.g., WAYPOINT {target}, SECTOR {target})."
        )

    return ambiguities


def _check_time_ambiguity(parse_result: ParseResult) -> List[str]:
    """
    Check for ambiguous time references.
    
    Example: "WITHIN 30" (30 what? seconds? minutes?)
    """
    ambiguities: List[str] = []
    slots = parse_result.slots or {}

    # If duration specified but unit missing, it's ambiguous
    if "duration" in slots and "duration_unit" not in slots:
        ambiguities.append(
            f"Time duration '{slots['duration']}' is ambiguous. Specify unit (SECONDS, MINUTES, or HOURS)."
        )

    return ambiguities


def _check_navigation_ambiguity(parse_result: ParseResult) -> List[str]:
    """
    Check for ambiguous navigation commands.
    """
    ambiguities: List[str] = []
    slots = parse_result.slots or {}
    intent = parse_result.intent

    if intent == "WAYPOINT_NAVIGATION" and "target" not in slots:
        ambiguities.append("Navigation target is missing or unclear.")

    return ambiguities
