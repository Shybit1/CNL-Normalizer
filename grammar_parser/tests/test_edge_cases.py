from grammar_parser import parse


def test_whitespace_and_edge_cases():
    assert not parse('').success
    assert not parse('\n').success
    assert parse('   CLIMB TO 000500 METERS   ').success
    assert parse('LOITER FOR 0005 SECONDS').success
    assert parse('GO TO BASE_7').success
    assert parse('FORMATION CUSTOM_FORMATION').success
