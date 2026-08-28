"""
Tests for navigation commands (GO TO).
"""

from grammar_parser import parse, Intent


class TestNavigationCommands:
    """Valid navigation commands."""

    def test_go_to_waypoint(self):
        r = parse("GO TO WAYPOINT ALPHA")
        assert r.success is True
        assert r.intent == Intent.WAYPOINT_NAVIGATION
        assert r.slots["target"] == "alpha"
        assert r.slots["waypoint_type"] == "waypoint"

    def test_go_to_sector(self):
        r = parse("GO TO SECTOR BRAVO")
        assert r.success is True
        assert r.slots["target"] == "bravo"
        assert r.slots["waypoint_type"] == "sector"

    def test_go_to_zone(self):
        r = parse("GO TO ZONE CHARLIE")
        assert r.success is True

    def test_go_to_point(self):
        r = parse("GO TO POINT DELTA")
        assert r.success is True

    def test_go_to_home(self):
        r = parse("GO TO HOME")
        assert r.success is True
        assert r.slots["target"] == "home"

    def test_go_to_base(self):
        r = parse("GO TO BASE")
        assert r.success is True
        assert r.slots["target"] == "base"

    def test_go_to_without_prefix(self):
        r = parse("GO TO ALPHA")
        assert r.success is True
        assert r.slots["target"] == "alpha"
        assert "waypoint_type" not in r.slots

    def test_go_to_rally(self):
        r = parse("GO TO RALLY")
        assert r.success is True

    def test_go_to_landing(self):
        r = parse("GO TO LANDING")
        assert r.success is True

    def test_go_to_zulu(self):
        r = parse("GO TO ZULU")
        assert r.success is True
        assert r.slots["target"] == "zulu"


class TestNavigationErrors:
    """Invalid navigation commands."""

    def test_missing_to(self):
        r = parse("GO WAYPOINT ALPHA")
        assert r.success is False
        assert any("TO" in e for e in r.errors)

    def test_no_target(self):
        r = parse("GO TO")
        assert r.success is False
        assert any("target" in e.lower() or "short" in e.lower() for e in r.errors)

    def test_bad_target(self):
        r = parse("GO TO WAYPOINT 123")
        assert r.success is False