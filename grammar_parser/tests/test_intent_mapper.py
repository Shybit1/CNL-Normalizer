from grammar_parser.ast import AltitudeCommand, NavigationCommand, FormationCommand, LoiterCommand, AbortCommand
from grammar_parser.intent_mapper import map_intent


def test_intent_mapping_altitude():
    ast = AltitudeCommand(action='CLIMB', altitude=500, unit='METERS')
    r = map_intent(ast)
    assert r.intent == 'ALTITUDE_CHANGE'
    assert r.slots['target_altitude'] == 500

def test_intent_mapping_navigation():
    ast = NavigationCommand(destination='BRAVO')
    r = map_intent(ast)
    assert r.intent == 'WAYPOINT_NAVIGATION'
    assert r.slots['destination'] == 'BRAVO'
