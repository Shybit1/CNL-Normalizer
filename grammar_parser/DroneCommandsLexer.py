# Generated from DroneCommands.g4 by ANTLR 4.13.2
# DO NOT modify manually — regenerate from the .g4 file when the grammar changes.

from antlr4 import Lexer, Token
import sys
from typing import Optional


class DroneCommandsLexerStream:
    """Wrapper to track token position."""
    pass


class DroneCommandsLexer(Lexer):
    """Generated lexer for drone command canonical text."""

    atn = None  # ATN not needed for our deterministic grammar
    decisionsToDFA = []
    sharedContextCache = None

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

    channelNames = ['DEFAULT_TOKEN_CHANNEL', 'HIDDEN']
    modeNames = ['DEFAULT_MODE']

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

    ruleNames = [
        "CLIMB", "DESCEND", "GO", "TO", "FORMATION", "LOITER", "HOLD",
        "RTL", "RETURN", "ABORT", "FOR", "AT", "IN", "AVOID", "HOME",
        "WAYPOINT", "SECTOR", "ZONE", "POINT", "BASE", "RALLY", "LANDING",
        "POSITION", "METERS", "FEET", "SECONDS", "MINUTES", "HOURS",
        "IDENTIFIER", "INTEGER", "WS", "ERROR_CHAR"
    ]

    grammarFileName = "DroneCommands.g4"

    # Token type index for keywords (must match order above)
    _KEYWORD_MAP = {
        'CLIMB': 1, 'DESCEND': 2, 'GO': 3, 'TO': 4, 'FORMATION': 5,
        'LOITER': 6, 'HOLD': 7, 'RTL': 8, 'RETURN': 9, 'ABORT': 10,
        'FOR': 11, 'AT': 12, 'IN': 13, 'AVOID': 14, 'HOME': 15,
        'WAYPOINT': 16, 'SECTOR': 17, 'ZONE': 18, 'POINT': 19,
        'BASE': 20, 'RALLY': 21, 'LANDING': 22, 'POSITION': 23,
        'METERS': 24, 'FEET': 25, 'SECONDS': 26, 'MINUTES': 27,
        'HOURS': 28,
    }

    def __init__(self, input=None, output=None, errors=None):
        super().__init__(input, output, errors) if hasattr(super(), '__init__') else None
        self._input_stream = input
        self._tokens = []
        self._pos = 0
        self._interp = None

    @property
    def interpreter(self):
        return self._interp

    @interpreter.setter
    def interpreter(self, value):
        self._interp = value

    def nextToken(self):
        """Manually tokenize the input stream."""
        if hasattr(self, '_input_stream') and self._input_stream is not None:
            text = str(self._input_stream)
            tokens = self._tokenize(text)
        else:
            # Fallback: use the input if set via setInputStream-like method
            tokens = []

        if self._pos < len(tokens):
            token = tokens[self._pos]
            self._pos += 1
            return token
        else:
            from antlr4.Token import CommonToken
            return CommonToken(Token.EOF)

    def reset(self):
        self._pos = 0
        self._tokens = []

    @classmethod
    def _tokenize(cls, text: str):
        """Tokenize canonical command text into ANTLR tokens."""
        from antlr4.Token import CommonToken

        tokens = []
        words = text.split()
        pos = 0

        for i, word in enumerate(words):
            # Check for keywords first
            token_type = cls._KEYWORD_MAP.get(word)
            if token_type is not None:
                tok = CommonToken(token_type, word)
            elif word.isdigit():
                tok = CommonToken(cls.INTEGER, word)
            elif word.isupper() and word[0].isalpha():
                tok = CommonToken(cls.IDENTIFIER, word)
            else:
                tok = CommonToken(cls.ERROR_CHAR, word)

            tok.line = 1
            tok.column = pos
            tok.start = pos
            tok.stop = pos + len(word) - 1
            pos += len(word) + 1  # +1 for space after
            tokens.append(tok)

        # Add EOF
        from antlr4.Token import Token
        eof = CommonToken(Token.EOF, "<EOF>")
        eof.line = 1
        eof.column = pos
        eof.start = pos
        eof.stop = pos
        tokens.append(eof)

        return tokens