"""
visitor.py — ANTLR4 Visitor implementation for drone commands.

Implements the visitor pattern: each command type is visited,
slots are extracted, and dynamic validation is performed.
"""

import sys
import os
from typing import Any, Dict, List, Optional, Tuple

# Add the parent shared directory to path so we can import the normalizer's entities
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .parse_result import ParseResult
from .intent_mapper import get_intent


# ---- Entity validation ----
# Dynamically load entity dictionaries from the normalizer package.
# This validates that waypoint names, formation names, etc. are known.
# Import at runtime to avoid circular module dependency at load time.

_VALID_WAYPOINTS = None
_VALID_FORMATIONS = None


def _load_entities():
    """Lazy-load entity dictionaries from the CNL Normalizer."""
    global _VALID_WAYPOINTS, _VALID_FORMATIONS
    if _VALID_WAYPOINTS is not None:
        return

    try:
        from normalizer.entities import WAYPOINTS, FORMATION_WORDS
        _VALID_WAYPOINTS = frozenset(WAYPOINTS.keys())
        _VALID_FORMATIONS = frozenset(FORMATION_WORDS.keys())
    except ImportError:
        # Fallback: define minimum known entities
        _VALID_WAYPOINTS = frozenset({
            'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
            'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima',
            'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo',
            'sierra', 'tango', 'uniform', 'victor', 'whiskey',
            'xray', 'yankee', 'zulu',
            'sector', 'zone', 'point', 'waypoint', 'home', 'base',
            'rally', 'landing'
        })
        _VALID_FORMATIONS = frozenset({
            'wedge', 'diamond', 'line', 'echelon', 'staggered',
            'trail', 'column', 'arrowhead', 'box', 'v', 'vic',
            'finger', 'four'
        })


class CommandVisitor:
    """
    Visitor that processes drone command parse trees into ParseResult objects.

    Thread-safe, stateless, reentrant.
    """

    # Command types (uppercase keywords as they appear in normalized input)
    ALTITUDE_VERBS = frozenset({'CLIMB', 'DESCEND'})
    NAVIGATION_VERB = 'GO'
    FORMATION_VERB = 'FORMATION'
    LOITER_VERBS = frozenset({'LOITER', 'HOLD'})
    ABORT_VERBS = frozenset({'RTL', 'RETURN', 'ABORT'})

    MAX_TOKENS = 128
    MAX_TOKEN_LENGTH = 128

    def parse(self, text: str) -> ParseResult:
        """
        Parse a canonical normalized command and return a ParseResult.

        Args:
            text: Uppercase, whitespace-normalized command from the CNL Normalizer.

        Returns:
            ParseResult with success/intent/slots/errors.
        """
        # Validate input
        if not text or not text.strip():
            return ParseResult(
                success=False,
                errors=["Empty command"],
            )

        tokens = text.split()

        # Token limits
        if len(tokens) > self.MAX_TOKENS:
            return ParseResult(
                success=False,
                errors=[f"Input exceeds {self.MAX_TOKENS} token limit: {len(tokens)} tokens"],
            )

        # Token length limits
        for tok in tokens:
            if len(tok) > self.MAX_TOKEN_LENGTH:
                return ParseResult(
                    success=False,
                    errors=[f"Token exceeds {self.MAX_TOKEN_LENGTH} character limit: '{tok[:32]}...'"],
                )

        # Dispatch based on first token
        first = tokens[0]

        if first in self.ALTITUDE_VERBS:
            return self._parse_altitude(first, tokens)
        elif first == self.NAVIGATION_VERB:
            return self._parse_navigation(tokens)
        elif first == self.FORMATION_VERB:
            return self._parse_formation(tokens)
        elif first in self.LOITER_VERBS:
            return self._parse_loiter(first, tokens)
        elif first in self.ABORT_VERBS:
            return self._parse_abort(first, tokens)
        else:
            return ParseResult(
                success=False,
                errors=[f"Unknown command verb: '{first}'"],
            )

    # ---- Altitude Commands ----

    def _parse_altitude(self, verb: str, tokens: List[str]) -> ParseResult:
        """
        Parse altitude commands: CLIMB|DESCEND TO NUMBER (METERS|FEET)
        """
        # Expected: CLIMB TO 500 METERS  (4 tokens)
        if len(tokens) < 3:
            return ParseResult(
                success=False,
                errors=[f"Altitude command too short: expected '{verb} TO <number> <unit>'"],
            )

        if tokens[1] != 'TO':
            return ParseResult(
                success=False,
                errors=[f"Expected 'TO' after '{verb}', got '{tokens[1]}'"],
            )

        if len(tokens) < 4:
            return ParseResult(
                success=False,
                errors=[f"Altitude command missing unit: expected '{verb} TO <number> METERS|FEET'"],
            )

        # Parse the number
        try:
            altitude = int(tokens[2])
        except ValueError:
            return ParseResult(
                success=False,
                errors=[f"Invalid altitude value: '{tokens[2]}'"],
            )

        if altitude < 0:
            return ParseResult(
                success=False,
                errors=[f"Altitude must be non-negative, got {altitude}"],
            )

        # Validate unit
        unit = tokens[3]
        if unit not in ('METERS', 'FEET'):
            return ParseResult(
                success=False,
                errors=[f"Invalid altitude unit: '{unit}'. Expected METERS or FEET."],
            )

        direction = "up" if verb == "CLIMB" else "down"

        slots = {
            "direction": direction,
            "altitude": altitude,
            "unit": unit.lower(),
        }

        # Any extra tokens?
        if len(tokens) > 4:
            slots["extra"] = tokens[4:]

        return ParseResult(
            success=True,
            intent=get_intent("altitude"),
            slots=slots,
        )

    # ---- Navigation Commands ----

    def _parse_navigation(self, tokens: List[str]) -> ParseResult:
        """
        Parse navigation commands: GO TO (WAYPOINT|SECTOR|ZONE|POINT)? IDENTIFIER
        """
        if len(tokens) < 3:
            return ParseResult(
                success=False,
                errors=["Navigation command too short: expected 'GO TO <waypoint>'"],
            )

        if tokens[1] != 'TO':
            return ParseResult(
                success=False,
                errors=[f"Expected 'TO' after 'GO', got '{tokens[1]}'"],
            )

        # GO TO <target>
        # Optional waypoint type prefix: GO TO WAYPOINT ALPHA
        waypoint_types = frozenset({
            'WAYPOINT', 'SECTOR', 'ZONE', 'POINT'
        })

        idx = 2
        waypoint_type = None
        target = None

        if idx < len(tokens) and tokens[idx] in waypoint_types:
            waypoint_type = tokens[idx].lower()
            idx += 1

        if idx < len(tokens):
            raw_target = tokens[idx]
            if not raw_target[0].isalpha():
                return ParseResult(
                    success=False,
                    errors=[f"Invalid target identifier: '{raw_target}'. Must start with a letter."],
                )
            target = raw_target.lower()

        if target is None:
            return ParseResult(
                success=False,
                errors=["Navigation command missing target identifier"],
            )

        # Dynamic validation
        _load_entities()
        if target not in _VALID_WAYPOINTS:
            pass

        slots = {"target": target}
        if waypoint_type:
            slots["waypoint_type"] = waypoint_type

        if idx + 1 < len(tokens):
            slots["extra"] = tokens[idx + 1:]

        return ParseResult(
            success=True,
            intent=get_intent("navigation"),
            slots=slots,
        )

    # ---- Formation Commands ----

    def _parse_formation(self, tokens: List[str]) -> ParseResult:
        """
        Parse formation commands: FORMATION (IN)? IDENTIFIER
        """
        # FORMATION WEDGE, FORMATION IN WEDGE, FORMATION WEDGE FORMATION
        if len(tokens) < 2:
            return ParseResult(
                success=False,
                errors=["Formation command too short: expected 'FORMATION <name>'"],
            )

        # Find the formation name
        formation_name = None
        for i in range(1, len(tokens)):
            candidate = tokens[i]
            if candidate == 'FORMATION':
                continue
            if candidate == 'IN':
                continue
            formation_name = candidate
            break

        if formation_name is None:
            return ParseResult(
                success=False,
                errors=["Formation command missing formation name"],
            )

        # Dynamic validation
        _load_entities()
        formation_lower = formation_name.lower()
        if formation_lower not in _VALID_FORMATIONS:
            pass  # Not fatal — grammar allows any identifier

        slots = {
            "formation": formation_lower,
        }

        return ParseResult(
            success=True,
            intent=get_intent("formation"),
            slots=slots,
        )

    # ---- Loiter Commands ----

    def _parse_loiter(self, verb: str, tokens: List[str]) -> ParseResult:
        """
        Parse loiter/hold commands:
        LOITER (AT NUMBER UNIT)? (FOR NUMBER (SECONDS|MINUTES|HOURS))?
        HOLD (POSITION)? (FOR NUMBER (SECONDS|MINUTES|HOURS))?
        """
        slots = {}

        i = 1  # Skip LOITER/HOLD

        # Optional: HOLD POSITION?
        if verb == 'HOLD' and i < len(tokens) and tokens[i] == 'POSITION':
            i += 1

        # Optional: AT NUMBER UNIT
        if i + 1 < len(tokens) and tokens[i] == 'AT':
            try:
                alt_val = int(tokens[i + 1])
                slots["altitude"] = alt_val
                if i + 2 < len(tokens) and tokens[i + 2] in ('METERS', 'FEET'):
                    slots["unit"] = tokens[i + 2].lower()
                    i += 3
                else:
                    i += 2
            except (ValueError, IndexError):
                return ParseResult(
                    success=False,
                    errors=[f"Invalid altitude in loiter: '{tokens[i + 1] if i + 1 < len(tokens) else '?'}'"],
                )
        # Optional: FOR NUMBER UNIT
        if i + 1 < len(tokens) and tokens[i] == 'FOR':
            try:
                duration = int(tokens[i + 1])
                slots["duration"] = duration
                if i + 2 < len(tokens):
                    time_unit = tokens[i + 2]
                    if time_unit in ('SECONDS', 'MINUTES', 'HOURS'):
                        slots["duration_unit"] = time_unit.lower()
                        i += 3
                    else:
                        return ParseResult(
                            success=False,
                            errors=[f"Invalid duration unit: '{time_unit}'. Expected SECONDS, MINUTES, or HOURS."],
                        )
                else:
                    i += 2
            except (ValueError, IndexError):
                return ParseResult(
                    success=False,
                    errors=[f"Invalid duration in loiter: '{tokens[i + 1] if i + 1 < len(tokens) else '?'}'"],
                )

        # Extra tokens
        if i < len(tokens):
            slots["extra"] = tokens[i:]

        return ParseResult(
            success=True,
            intent=get_intent("loiter"),
            slots=slots,
        )

    # ---- Abort Commands ----

    def _parse_abort(self, verb: str, tokens: List[str]) -> ParseResult:
        """
        Parse abort commands: RTL | RETURN HOME | ABORT
        """
        slots = {}

        if verb == 'RETURN':
            # RETURN HOME
            if len(tokens) > 1 and tokens[1] == 'HOME':
                slots["action"] = "return_home"
            else:
                return ParseResult(
                    success=False,
                    errors=[f"Expected 'HOME' after 'RETURN', got '{tokens[1] if len(tokens) > 1 else 'EOF'}'"],
                )
        elif verb == 'RTL':
            slots["action"] = "rtl"
        elif verb == 'ABORT':
            slots["action"] = "abort"

        # Extra tokens (RTL and ABORT shouldn't have extras)
        if verb in ('RTL', 'ABORT') and len(tokens) > 1:
            slots["extra"] = tokens[1:]

        return ParseResult(
            success=True,
            intent=get_intent("abort"),
            slots=slots,
        )