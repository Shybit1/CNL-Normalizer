grammar DroneCommands;

/*
 * DroneCommands.g4 — ANTLR4 grammar for Canonical Aero CNL Commands.
 *
 * Accepts canonical normalized commands from the CNL Normalizer.
 * All commands are UPPERCASE, space-separated.
 *
 * Five command families:
 * 1. Altitude:  CLIMB | DESCEND TO NUMBER (METERS | FEET)
 * 2. Navigation: GO TO (WAYPOINT)? IDENTIFIER
 * 3. Formation: FORMATION IDENTIFIER
 * 4. Loiter:    LOITER (FOR NUMBER (SECONDS | MINUTES))?
 * 5. Abort:     RTL | RETURN HOME | ABORT
 *
 * Dynamic validation (waypoint names, formation names) is handled
 * by the visitor — NOT hardcoded in the grammar.
 */

command
    : altitudeCommand EOF
    | navigationCommand EOF
    | formationCommand EOF
    | loiterCommand EOF
    | abortCommand EOF
    ;

// ALTITUDE: CLIMB | DESCEND TO NUMBER (METERS | FEET)
altitudeCommand
    : altitudeVerb TO altitude=INTEGER unit=altitudeUnit
    ;

altitudeVerb
    : CLIMB
    | DESCEND
    ;

altitudeUnit
    : METERS
    | FEET
    ;

// NAVIGATION: GO TO (WAYPOINT)? IDENTIFIER
navigationCommand
    : GO TO waypointType? target=IDENTIFIER
    ;

waypointType
    : WAYPOINT
    | SECTOR
    | ZONE
    | POINT
    | HOME
    | BASE
    | RALLY
    | LANDING
    ;

// FORMATION: FORMATION IDENTIFIER
formationCommand
    : FORMATION IN? formation=IDENTIFIER FORMATION?
    | FORMATION formation=IDENTIFIER IN? FORMATION?
    ;

// LOITER: LOITER (FOR NUMBER (SECONDS | MINUTES))?
loiterCommand
    : LOITER (AT NUMBER altitudeUnit)? (FOR duration=INTEGER durationUnit=loiterDurationUnit)?
    | HOLD POSITION? (FOR duration=INTEGER durationUnit=loiterDurationUnit)?
    ;

loiterDurationUnit
    : SECONDS
    | MINUTES
    | HOURS
    ;

// ABORT: RTL | RETURN HOME | ABORT
abortCommand
    : RTL
    | RETURN HOME
    | ABORT
    ;

// ---- Lexer Rules ----

CLIMB    : 'CLIMB' ;
DESCEND  : 'DESCEND' ;
GO       : 'GO' ;
TO       : 'TO' ;
FORMATION : 'FORMATION' ;
LOITER   : 'LOITER' ;
HOLD     : 'HOLD' ;
RTL      : 'RTL' ;
RETURN   : 'RETURN' ;
ABORT    : 'ABORT' ;
FOR      : 'FOR' ;
AT       : 'AT' ;
IN       : 'IN' ;
AVOID    : 'AVOID' ;
HOME     : 'HOME' ;
WAYPOINT : 'WAYPOINT' ;
SECTOR   : 'SECTOR' ;
ZONE     : 'ZONE' ;
POINT    : 'POINT' ;
BASE     : 'BASE' ;
RALLY    : 'RALLY' ;
LANDING  : 'LANDING' ;
POSITION : 'POSITION' ;

// Units
METERS   : 'METERS' ;
FEET     : 'FEET' ;
SECONDS  : 'SECONDS' ;
MINUTES  : 'MINUTES' ;
HOURS    : 'HOURS' ;

// An identifier is an uppercase word not matching any keyword above.
IDENTIFIER : [A-Z][A-Z0-9]* ;

// Integers (always from normalizer's number stage)
INTEGER : [0-9]+ ;

// Skip whitespace
WS : [ \t\r\n]+ -> skip ;

// Error handling: any unexpected character
ERROR_CHAR : . ;