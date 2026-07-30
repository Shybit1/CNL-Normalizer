"""
Tests for altitude commands (CLIMB, DESCEND).
"""

from grammar_parser import parse, Intent


class TestAltitudeCommands:
    """Valid altitude commands."""

    def test_climb_to_meters(self):
        r = parse("CLIMB TO 500 METERS")
        assert r.success is True
        assert r.intent == Intent.ALTITUDE_CHANGE
        assert r.slots["direction"] == "up"
        assert r.slots["altitude"] == 500
        assert r.slots["unit"] == "meters"

    def test_descend_to_meters(self):
        r = parse("DESCEND TO 300 METERS")
        assert r.success is True
        assert r.intent == Intent.ALTITUDE_CHANGE
        assert r.slots["direction"] == "down"
        assert r.slots["altitude"] == 300

    def test_climb_to_feet(self):
        r = parse("CLIMB TO 1000 FEET")
        assert r.success is True
        assert r.slots["unit"] == "feet"

    def test_descend_to_feet(self):
        r = parse("DESCEND TO 200 FEET")
        assert r.success is True
        assert r.slots["unit"] == "feet"

    def test_large_altitude(self):
        r = parse("CLIMB TO 99999 METERS")
        assert r.success is True
        assert r.slots["altitude"] == 99999

    def test_zero_altitude(self):
        r = parse("DESCEND TO 0 METERS")
        assert r.success is True
        assert r.slots["altitude"] == 0


class TestAltitudeErrors:
    """Invalid altitude commands."""

    def test_missing_to(self):
        r = parse("CLIMB 500 METERS")
        assert r.success is False
        assert any("TO" in e for e in r.errors)

    def test_missing_unit(self):
        r = parse("CLIMB TO 500")
        assert r.success is False
        assert any("unit" in e.lower() for e in r.errors)

    def test_invalid_number(self):
        r = parse("CLIMB TO ABC METERS")
        assert r.success is False
        assert any("altitude" in e.lower() for e in r.errors)

    def test_invalid_unit(self):
        r = parse("CLIMB TO 500 KILOMETERS")
        assert r.success is False
        assert any("unit" in e.lower() for e in r.errors)

    def test_too_few_tokens(self):
        r = parse("CLIMB")
        assert r.success is False

    def test_negative_number(self):
        r = parse("CLIMB TO -500 METERS")
        assert r.success is False

    def test_wrong_verb_order(self):
        r = parse("TO CLIMB 500 METERS")
        assert r.success is False