from grammar_parser import parse

invalid_commands = [
    'CLIMB',
    'CLIMB TO',
    'CLIMB TO METERS',
    'GO',
    'GO BRAVO',
    'FORMATION',
    'FORMATION TO WEDGE',
    'LOITER FOR',
    'LOITER 20',
    'RETURN',
    'HOME',
    'RTL NOW',
    'ABORT NOW',
    'CLIMB TO -10 METERS',
]


def test_invalid_commands():
    for cmd in invalid_commands:
        r = parse(cmd)
        assert not r.success, f"Expected failure for: {cmd}"

