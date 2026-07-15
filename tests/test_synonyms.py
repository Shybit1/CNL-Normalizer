"""
Tests for the synonyms module.
"""

from normalizer import synonyms


class TestReplaceSynonyms:
    def test_climb_variants(self):
        assert synonyms.replace_synonyms("ascend") == "CLIMB"
        assert synonyms.replace_synonyms("rise") == "CLIMB"
        assert synonyms.replace_synonyms("climb") == "CLIMB"

    def test_go_up(self):
        assert synonyms.replace_synonyms("go up") == "CLIMB"

    def test_go_upward(self):
        assert synonyms.replace_synonyms("go upward") == "CLIMB"

    def test_take_us_up(self):
        assert synonyms.replace_synonyms("take us up") == "CLIMB"

    def test_increase_altitude(self):
        assert synonyms.replace_synonyms("increase altitude") == "CLIMB"

    def test_descend_variants(self):
        assert synonyms.replace_synonyms("descend") == "DESCEND"
        assert synonyms.replace_synonyms("go down") == "DESCEND"
        assert synonyms.replace_synonyms("drop") == "DESCEND"
        assert synonyms.replace_synonyms("sink") == "DESCEND"

    def test_go_variants(self):
        assert synonyms.replace_synonyms("move") == "GO"
        assert synonyms.replace_synonyms("fly") == "GO"
        assert synonyms.replace_synonyms("proceed") == "GO"
        assert synonyms.replace_synonyms("head") == "GO"

    def test_rtl_variants(self):
        assert synonyms.replace_synonyms("return to launch") == "RTL"
        assert synonyms.replace_synonyms("rtl") == "RTL"
        assert synonyms.replace_synonyms("return") == "RTL"

    def test_loiter_variants(self):
        assert synonyms.replace_synonyms("hover") == "LOITER"
        assert synonyms.replace_synonyms("stay") == "LOITER"
        assert synonyms.replace_synonyms("circle") == "LOITER"
        assert synonyms.replace_synonyms("orbit") == "LOITER"

    def test_formation_variants(self):
        assert synonyms.replace_synonyms("form up") == "FORMATION"
        assert synonyms.replace_synonyms("formation") == "FORMATION"

    def test_avoid(self):
        assert synonyms.replace_synonyms("avoid") == "AVOID"
        assert synonyms.replace_synonyms("stay clear of") == "AVOID"

    def test_land(self):
        assert synonyms.replace_synonyms("land") == "LAND"
        assert synonyms.replace_synonyms("touch down") == "LAND"

    def test_takeoff(self):
        assert synonyms.replace_synonyms("take off") == "TAKEOFF"
        assert synonyms.replace_synonyms("launch") == "TAKEOFF"

    def test_scan(self):
        assert synonyms.replace_synonyms("scan") == "SCAN"
        assert synonyms.replace_synonyms("survey") == "SCAN"

    def test_follow(self):
        assert synonyms.replace_synonyms("follow") == "FOLLOW"
        assert synonyms.replace_synonyms("track") == "FOLLOW"

    def test_multi_word_before_single_word(self):
        result = synonyms.replace_synonyms("go up to 500")
        assert result == "CLIMB to 500"

    def test_sentence_with_synonyms(self):
        result = synonyms.replace_synonyms("please climb to 500 meters")
        assert result == "please CLIMB to 500 meters"

    def test_no_match(self):
        assert synonyms.replace_synonyms("hello world") == "hello world"

    def test_empty_string(self):
        assert synonyms.replace_synonyms("") == ""

    def test_go_vs_go_up_not_confused(self):
        result = synonyms.replace_synonyms("go to waypoint")
        assert "CLIMB" not in result
        assert "GO" in result