"""
Tests for formation commands.
"""

from grammar_parser import parse, Intent


class TestFormationCommands:
    """Valid formation commands."""

    def test_formation_wedge(self):
        r = parse("FORMATION WEDGE")
        assert r.success is True
        assert r.intent == Intent.FORMATION_CHANGE
        assert r.slots["formation"] == "wedge"

    def test_formation_diamond(self):
        r = parse("FORMATION DIAMOND")
        assert r.success is True
        assert r.slots["formation"] == "diamond"

    def test_formation_line(self):
        r = parse("FORMATION LINE")
        assert r.success is True

    def test_formation_echelon(self):
        r = parse("FORMATION ECHELON")
        assert r.success is True

    def test_formation_arrowhead(self):
        r = parse("FORMATION ARROWHEAD")
        assert r.success is True

    def test_formation_box(self):
        r = parse("FORMATION BOX")
        assert r.success is True

    def test_formation_v(self):
        r = parse("FORMATION V")
        assert r.success is True

    def test_formation_vic(self):
        r = parse("FORMATION VIC")
        assert r.success is True

    def test_formation_in_wedge(self):
        r = parse("FORMATION IN WEDGE")
        assert r.success is True
        assert r.slots["formation"] == "wedge"

    def test_formation_wedge_formation(self):
        r = parse("FORMATION WEDGE FORMATION")
        assert r.success is True
        assert r.slots["formation"] == "wedge"


class TestFormationErrors:
    """Invalid formation commands."""

    def test_no_formation_name(self):
        r = parse("FORMATION")
        assert r.success is False

    def test_formation_in(self):
        r = parse("FORMATION IN")
        assert r.success is False