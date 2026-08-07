# Generated from DroneCommands.g4 by ANTLR 4.13.2
# DO NOT modify manually — regenerate from the .g4 file when the grammar changes.

from antlr4 import Parser, ParserRuleContext, Token, RecognitionException
from antlr4.atn.ATN import ATN
from antlr4.dfa.DFA import DFA
from antlr4.error.Errors import FailedPredicateException
from antlr4.error.ErrorStrategy import BailErrorStrategy
from typing import Optional, List


class DroneCommandsParser(Parser):
    """Generated parser for drone command canonical text."""

    grammarFileName = "DroneCommands.g4"

    atn = ATN(0, 0)  # Placeholder — not used by our deterministic parser
    decisionsToDFA = [DFA(0, 0, None)]

    sharedContextCache = None

    # Token type constants
    CLIMB = 1
    DESCEND = 2
    GO = 3
    TO = 4
    FORMATION = 5
    LOITER = 6
    HOLD = 7
    RTL = 8
    RETURN = 9
    ABORT = 10
    FOR = 11
    AT = 12
    IN = 13
    AVOID = 14
    HOME = 15
    WAYPOINT = 16
    SECTOR = 17
    ZONE = 18
    POINT = 19
    BASE = 20
    RALLY = 21
    LANDING = 22
    POSITION = 23
    METERS = 24
    FEET = 25
    SECONDS = 26
    MINUTES = 27
    HOURS = 28
    IDENTIFIER = 29
    INTEGER = 30
    WS = 31
    ERROR_CHAR = 32

    # Rule indices
    RULE_command = 0
    RULE_altitudeCommand = 1
    RULE_navigationCommand = 2
    RULE_formationCommand = 3
    RULE_loiterCommand = 4
    RULE_abortCommand = 5

    ruleNames = [
        "command", "altitudeCommand", "navigationCommand",
        "formationCommand", "loiterCommand", "abortCommand"
    ]

    literalNames = [
        None, "'CLIMB'", "'DESCEND'", "'GO'", "'TO'", "'FORMATION'",
        "'LOITER'", "'HOLD'", "'RTL'", "'RETURN'", "'ABORT'", "'FOR'",
        "'AT'", "'IN'", "'AVOID'", "'HOME'", "'WAYPOINT'", "'SECTOR'",
        "'ZONE'", "'POINT'", "'BASE'", "'RALLY'", "'LANDING'", "'POSITION'",
        "'METERS'", "'FEET'", "'SECONDS'", "'MINUTES'", "'HOURS'"
    ]

    symbolicNames = [
        None, "CLIMB", "DESCEND", "GO", "TO", "FORMATION",
        "LOITER", "HOLD", "RTL", "RETURN", "ABORT", "FOR",
        "AT", "IN", "AVOID", "HOME", "WAYPOINT", "SECTOR",
        "ZONE", "POINT", "BASE", "RALLY", "LANDING", "POSITION",
        "METERS", "FEET", "SECONDS", "MINUTES", "HOURS",
        "IDENTIFIER", "INTEGER", "WS", "ERROR_CHAR"
    ]

    EOF = Token.EOF

    def __init__(self, input):
        super().__init__(input)
        self._interp = None

    @property
    def interpreter(self):
        return self._interp

    @interpreter.setter
    def interpreter(self, value):
        self._interp = value

    # ---- Parse tree context classes ----

    class CommandContext(ParserRuleContext):
        def __init__(self, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)

    class AltitudeCommandContext(ParserRuleContext):
        def __init__(self, parent=None, invokingState=-1):
            super().__init__(parent, invokingState)


# Export context classes at module level
CommandContext = DroneCommandsParser.CommandContext
AltitudeCommandContext = DroneCommandsParser.AltitudeCommandContext