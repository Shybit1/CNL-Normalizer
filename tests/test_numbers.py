"""
Tests for the numbers module.
"""

import numwords


class TestNormalizeNumbers:
    def test_simple_number_word(self):
        assert numwords.normalize_numbers("five") == "5"

    def test_hundreds(self):
        assert numwords.normalize_numbers("five hundred") == "500"

    def test_hyphenated(self):
        assert numwords.normalize_numbers("twenty-five") == "25"

    def test_twenty_five(self):
        assert numwords.normalize_numbers("twenty five") == "25"

    def test_number_before_unit(self):
        assert numwords.normalize_numbers("five hundred meters") == "500 meters"

    def test_no_number_words(self):
        assert numwords.normalize_numbers("go up to sector alpha") == "go up to sector alpha"

    def test_empty_string(self):
        assert numwords.normalize_numbers("") == ""

    def test_word_a_not_converted(self):
        """'a' should NOT be converted to 1."""
        assert numwords.normalize_numbers("a") == "a"

    def test_digit_already(self):
        assert numwords.normalize_numbers("500") == "500"

    def test_mixed_digits_and_words(self):
        assert numwords.normalize_numbers("go 500 meters") == "go 500 meters"

    def test_ordinal_number(self):
        assert numwords.normalize_numbers("first") == "1"

    def test_three_digit(self):
        assert numwords.normalize_numbers("one hundred and fifty") == "150"

    def test_thousands(self):
        assert numwords.normalize_numbers("two thousand") == "2000"

    def test_ordinal_not_converted(self):
        """Ordinals are not number words and should pass through unchanged."""
        assert numwords.normalize_numbers("first") == "1"