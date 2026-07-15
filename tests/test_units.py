"""
Tests for the units module.
"""

from normalizer import units


class TestNormalizeUnits:
    def test_meters(self):
        assert units.normalize_units("500 meters") == "500 METERS"
        assert units.normalize_units("500 meter") == "500 METERS"
        assert units.normalize_units("500 m") == "500 METERS"

    def test_metres(self):
        assert units.normalize_units("500 metres") == "500 METERS"
        assert units.normalize_units("500 metre") == "500 METERS"

    def test_kilometers(self):
        assert units.normalize_units("10 kilometers") == "10 KILOMETERS"
        assert units.normalize_units("10 km") == "10 KILOMETERS"

    def test_kilometres(self):
        assert units.normalize_units("10 kilometres") == "10 KILOMETERS"

    def test_klick(self):
        assert units.normalize_units("5 klicks") == "5 KILOMETERS"
        assert units.normalize_units("5 klick") == "5 KILOMETERS"

    def test_feet(self):
        assert units.normalize_units("1000 feet") == "1000 FEET"
        assert units.normalize_units("1000 ft") == "1000 FEET"
        assert units.normalize_units("1000 foot") == "1000 FEET"

    def test_seconds(self):
        assert units.normalize_units("30 seconds") == "30 SECONDS"
        assert units.normalize_units("30 sec") == "30 SECONDS"
        assert units.normalize_units("30 secs") == "30 SECONDS"
        assert units.normalize_units("30 s") == "30 SECONDS"

    def test_minutes(self):
        assert units.normalize_units("5 minutes") == "5 MINUTES"
        assert units.normalize_units("5 min") == "5 MINUTES"
        assert units.normalize_units("5 mins") == "5 MINUTES"

    def test_hours(self):
        assert units.normalize_units("2 hours") == "2 HOURS"
        assert units.normalize_units("2 hr") == "2 HOURS"
        assert units.normalize_units("2 hrs") == "2 HOURS"

    def test_kmh(self):
        assert units.normalize_units("50 kmh") == "50 KMH"
        assert units.normalize_units("50 kph") == "50 KMH"
        assert units.normalize_units("50 km/h") == "50 KMH"

    def test_multi_word_kmh(self):
        assert units.normalize_units("50 kilometers per hour") == "50 KMH"

    def test_mph(self):
        assert units.normalize_units("30 mph") == "30 MPH"
        assert units.normalize_units("30 miles per hour") == "30 MPH"

    def test_mps(self):
        assert units.normalize_units("10 m/s") == "10 MPS"
        assert units.normalize_units("10 meters per second") == "10 MPS"

    def test_knots(self):
        assert units.normalize_units("15 knots") == "15 KNOTS"
        assert units.normalize_units("15 kts") == "15 KNOTS"

    def test_degrees(self):
        assert units.normalize_units("90 degrees") == "90 DEGREES"
        assert units.normalize_units("90 deg") == "90 DEGREES"

    def test_percent(self):
        assert units.normalize_units("50 percent") == "50 PERCENT"
        assert units.normalize_units("50 per cent") == "50 PERCENT"

    def test_not_a_unit(self):
        assert units.normalize_units("go to alpha") == "go to alpha"

    def test_empty_string(self):
        assert units.normalize_units("") == ""

    def test_multi_word_before_single_word(self):
        result = units.normalize_units("50 kilometers per hour")
        assert "KMH" in result
        assert "KILOMETERS" not in result