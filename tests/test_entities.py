"""
Tests for the entities module.
"""

from normalizer import entities


class TestNormalizeEntities:
    def test_waypoint_alpha(self):
        assert entities.normalize_entities("alpha") == "ALPHA"

    def test_waypoint_bravo(self):
        assert entities.normalize_entities("bravo") == "BRAVO"

    def test_waypoint_charlie(self):
        assert entities.normalize_entities("charlie") == "CHARLIE"

    def test_waypoint_sierra(self):
        assert entities.normalize_entities("sierra") == "SIERRA"

    def test_waypoint_zulu(self):
        assert entities.normalize_entities("zulu") == "ZULU"

    def test_sector(self):
        assert entities.normalize_entities("sector") == "SECTOR"

    def test_zone(self):
        assert entities.normalize_entities("zone") == "ZONE"

    def test_waypoint(self):
        assert entities.normalize_entities("waypoint") == "WAYPOINT"

    def test_home(self):
        assert entities.normalize_entities("home") == "HOME"

    def test_base(self):
        assert entities.normalize_entities("base") == "BASE"

    def test_formation_wedge(self):
        assert entities.normalize_entities("wedge") == "WEDGE"

    def test_formation_diamond(self):
        assert entities.normalize_entities("diamond") == "DIAMOND"

    def test_formation_line(self):
        assert entities.normalize_entities("line") == "LINE"

    def test_formation_echelon(self):
        assert entities.normalize_entities("echelon") == "ECHELON"

    def test_formation_arrowhead(self):
        assert entities.normalize_entities("arrowhead") == "ARROWHEAD"

    def test_formation_vic(self):
        assert entities.normalize_entities("vic") == "VIC"

    def test_mixed_entities(self):
        result = entities.normalize_entities("go to sector alpha in wedge formation")
        assert result == "go to SECTOR ALPHA in WEDGE formation"

    def test_avoiding_sector_alpha(self):
        result = entities.normalize_entities("avoiding sector alpha")
        assert result == "avoiding SECTOR ALPHA"

    def test_no_entities(self):
        assert entities.normalize_entities("go up to 500 meters") == "go up to 500 meters"

    def test_empty_string(self):
        assert entities.normalize_entities("") == ""

    def test_entity_in_middle_of_sentence(self):
        result = entities.normalize_entities("fly to point alpha")
        assert result == "fly to POINT ALPHA"