"""
Tests for loiter / hold commands.
"""

from grammar_parser import parse, Intent


class TestLoiterCommands:
    """Valid loiter/hold commands."""

    def test_loiter_basic(self):
        r = parse("LOITER")
        assert r.success is True
        assert r.intent == Intent.HOLD_LOITER

    def test_loiter_at_altitude(self):
        r = parse("LOITER AT 100 METERS")
        assert r.success is True
        assert r.slots["altitude"] == 100
        assert r.slots["unit"] == "meters"

    def test_loiter_for_seconds(self):
        r = parse("LOITER FOR 30 SECONDS")
        assert r.success is True
        assert r.slots["duration"] == 30
        assert r.slots["duration_unit"] == "seconds"

    def test_loiter_for_minutes(self):
        r = parse("LOITER FOR 5 MINUTES")
        assert r.success is True
        assert r.slots["duration"] == 5
        assert r.slots["duration_unit"] == "minutes"

    def test_loiter_at_and_for(self):
        r = parse("LOITER AT 200 FEET FOR 60 SECONDS")
        assert r.success is True
        assert r.slots["altitude"] == 200
        assert r.slots["unit"] == "feet"
        assert r.slots["duration"] == 60
        assert r.slots["duration_unit"] == "seconds"

    def test_hold_basic(self):
        r = parse("HOLD")
        assert r.success is True
        assert r.intent == Intent.HOLD_LOITER

    def test_hold_position(self):
        r = parse("HOLD POSITION")
        assert r.success is True

    def test_hold_for_minutes(self):
        r = parse("HOLD FOR 10 MINUTES")
        assert r.success is True
        assert r.slots["duration"] == 10
        assert r.slots["duration_unit"] == "minutes"

    def test_hold_position_for(self):
        r = parse("HOLD POSITION FOR 2 HOURS")
        assert r.success is True
        assert r.slots["duration"] == 2
        assert r.slots["duration_unit"] == "hours"


class TestLoiterErrors:
    """Invalid loiter commands."""

    def test_invalid_duration(self):
        r = parse("LOITER FOR ABC SECONDS")
        assert r.success is False

    def test_invalid_duration_unit(self):
        r = parse("LOITER FOR 30 METERS")
        assert r.success is False