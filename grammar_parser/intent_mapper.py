"""
intent_mapper.py — Maps parsed command structures to intent types.

Intent labels from the PRD:
- ALTITUDE_CHANGE: CLIMB/DESCEND commands
- WAYPOINT_NAVIGATION: GO TO commands
- FORMATION_CHANGE: FORMATION commands
- HOLD_LOITER: LOITER/HOLD commands
- ABORT_RTL: RTL/RETURN HOME/ABORT commands
"""

from enum import Enum


class Intent(str, Enum):
    """Canonical intent types for drone commands."""
    ALTITUDE_CHANGE = "ALTITUDE_CHANGE"
    WAYPOINT_NAVIGATION = "WAYPOINT_NAVIGATION"
    FORMATION_CHANGE = "FORMATION_CHANGE"
    HOLD_LOITER = "HOLD_LOITER"
    ABORT_RTL = "ABORT_RTL"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Intent.{self.value}"


# Map command types to intents
COMMAND_INTENT_MAP = {
    "altitude": Intent.ALTITUDE_CHANGE,
    "navigation": Intent.WAYPOINT_NAVIGATION,
    "formation": Intent.FORMATION_CHANGE,
    "loiter": Intent.HOLD_LOITER,
    "abort": Intent.ABORT_RTL,
}


def get_intent(command_type: str) -> Intent:
    """
    Return the Intent enum for a given command type string.

    Args:
        command_type: Lowercase command type name ('altitude', 'navigation', etc.)

    Returns:
        The corresponding Intent enum value.

    Raises:
        KeyError: If the command type is unknown.
    """
    return COMMAND_INTENT_MAP[command_type]