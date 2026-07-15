"""
Integration tests for the full CNL Normalizer pipeline.
"""

from normalizer import normalize


class TestNormalizer:
    """Core spec examples from the business plan."""

    def test_go_up_to_500_meters(self):
        result = normalize("Go up to 500 meters.")
        assert result == "CLIMB TO 500 METERS", f"Got: {result}"

    def test_ascend_to_500_m(self):
        result = normalize("Ascend to 500 m.")
        assert result == "CLIMB TO 500 METERS", f"Got: {result}"

    def test_increase_altitude_to_five_hundred(self):
        """No unit in input, so METERS is not added."""
        result = normalize("Increase altitude to five hundred.")
        assert result == "CLIMB TO 500", f"Got: {result}"

    def test_climb_to_500(self):
        """No unit in input, so METERS is not added."""
        result = normalize("Climb to 500.")
        assert result == "CLIMB TO 500", f"Got: {result}"

    def test_take_us_up_to_500(self):
        """No unit in input, so METERS is not added."""
        result = normalize("Take us up to 500.")
        assert result == "CLIMB TO 500", f"Got: {result}"

    def test_complex_command(self):
        result = normalize(
            "Could everyone please go up to five hundred metres "
            "while avoiding sector alpha?"
        )
        expected = "EVERYONE CLIMB TO 500 METERS AVOIDING SECTOR ALPHA"
        assert result == expected, f"Got: {result!r}"

    def test_could_you_please_climb(self):
        result = normalize("Could you please climb to 500 meters?")
        expected = "CLIMB TO 500 METERS"
        assert result == expected, f"Got: {result!r}"


class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_empty_string(self):
        assert normalize("") == ""

    def test_whitespace_only(self):
        assert normalize("   ") == ""

    def test_no_change_needed(self):
        result = normalize("land")
        assert result == "LAND"

    def test_multi_word_synonym(self):
        result = normalize("go up")
        assert result == "CLIMB"

    def test_punctuation_handling(self):
        result = normalize("Go!!! to... point... alpha?")
        assert result == "GO TO POINT ALPHA"

    def test_number_word_conversion(self):
        result = normalize("descend to three hundred meters")
        assert result == "DESCEND TO 300 METERS"

    def test_formation_command(self):
        result = normalize("form up in wedge formation")
        assert result == "FORMATION IN WEDGE FORMATION"

    def test_rtl_command(self):
        result = normalize("return to launch")
        assert result == "RTL"

    def test_loiter_command(self):
        result = normalize("hover at 100 meters for 30 seconds")
        assert result == "LOITER AT 100 METERS FOR 30 SECONDS"

    def test_follow_command(self):
        result = normalize("follow drone alpha")
        assert result == "FOLLOW DRONE ALPHA"

    def test_scan_command(self):
        result = normalize("scan sector bravo")
        assert result == "SCAN SECTOR BRAVO"

    def test_all_filler_words(self):
        result = normalize("please could you kindly just go up")
        assert result == "CLIMB"

    def test_avoid_command(self):
        result = normalize("stay clear of sector alpha")
        assert result == "AVOID SECTOR ALPHA"

    def test_takeoff(self):
        result = normalize("launch")
        assert result == "TAKEOFF"

    def test_land(self):
        result = normalize("touch down")
        assert result == "LAND"

    def test_units_multi_word(self):
        result = normalize("go at 50 kilometers per hour")
        assert result == "GO AT 50 KMH"

    def test_mixed_units(self):
        result = normalize("climb 500 meters at 10 m/s")
        assert result == "CLIMB 500 METERS AT 10 MPS"

    def test_numeric_phrases(self):
        result = normalize("set altitude to one thousand five hundred")
        assert result == "SET ALTITUDE TO 1500"

    def test_overlapping_synonyms(self):
        result = normalize("go up")
        assert result == "CLIMB"

    def test_case_insensitivity(self):
        result = normalize("CLIMB TO 500 METERS")
        assert result == "CLIMB TO 500 METERS"

    def test_deterministic(self):
        r1 = normalize("Could you please go up to five hundred metres?")
        r2 = normalize("Could you please go up to five hundred metres?")
        assert r1 == r2