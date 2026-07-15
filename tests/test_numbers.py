"""
Tests for the numbers module.
"""

from normalizer import numbers


class TestNormalizeNumbers:
    def test_simple_number_word(self):
        assert numbers.normalize_numbers("five") == "5"

    def test_hundreds(self):
        assert numbers.normalize_numbers("five hundred") == "500"

    def test_hyphenated(self):
        assert numbers.normalize_numbers("twenty-five") == "25"

    def test_twenty_five(self):
        assert numbers.normalize_numbers("twenty five") == "25"

    def test_number_before_unit(self):
        assert numbers.normalize_numbers("five hundred meters") == "500 meters"

    def test_no_number_words(self):
        assert numbers.normalize_numbers("go up to sector alpha") == "go up to sector alpha"

    def test_empty_string(self):
        assert numbers.normalize_numbers("") == ""

    def test_word_a_not_converted(self):
        """'a' should NOT be converted to 1."""
        assert numbers.normalize_numbers("a") == "a"

    def test_digit_already(self):
        assert numbers.normalize_numbers("500") == "500"

    def test_mixed_digits_and_words(self):
        assert numbers.normalize_numbers("go 500 meters") == "go 500 meters"

    def test_ordinal_not_converted(self):
        """Ordinals pass through unchanged."""
        assert numbers.normalize_numbers("first") == "first"

    def test_three_digit(self):
        assert numbers.normalize_numbers("one hundred and fifty") == "150"

    def test_thousands(self):
        assert numbers.normalize_numbers("two thousand") == "2000"