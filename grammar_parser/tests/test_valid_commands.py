from grammar_parser import parse
import pytest

valid_commands = [
    'CLIMB TO 500 METERS',
    'DESCEND TO 100 METERS',
    'GO TO BRAVO',
    'GO TO WAYPOINT ALPHA',
    'FORMATION WEDGE',
    'FORMATION DIAMOND',
    'FORMATION LINE',
    'LOITER',
    'LOITER FOR 20 SECONDS',
    'LOITER FOR 2 MINUTES',
    'RTL',
    'RETURN HOME',
    'ABORT',
]

@pytest.mark.parametrize('cmd', valid_commands)
def test_valid_commands(cmd):
    r = parse(cmd)
    assert r.success, f"Expected success for: {cmd}, errors={r.errors}"

