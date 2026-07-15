"""
Tests for the cleaner module.
"""

from normalizer import cleaner


class TestCleaner:
    def test_lowercase(self):
        assert cleaner.clean("GO UP TO 500 METERS") == "go up to 500 meters"

    def test_strip_punctuation(self):
        assert cleaner.clean("Go up to 500 meters.") == "go up to 500 meters"

    def test_multiple_punctuation(self):
        assert cleaner.clean("Go up to 500 meters!!!") == "go up to 500 meters"

    def test_collapse_whitespace(self):
        assert cleaner.clean("Go   up    to 500  meters") == "go up to 500 meters"

    def test_tabs_and_newlines(self):
        assert cleaner.clean("Go up\nto 500\tmeters") == "go up to 500 meters"

    def test_trim(self):
        assert cleaner.clean("  go up to 500 meters  ") == "go up to 500 meters"

    def test_preserves_hyphenated_words(self):
        assert cleaner.clean("twenty-one") == "twenty-one"

    def test_preserves_apostrophes(self):
        assert cleaner.clean("drone's position") == "drone's position"

    def test_special_chars(self):
        assert cleaner.clean("@#$%^&*()") == ""

    def test_empty_string(self):
        assert cleaner.clean("") == ""

    def test_whitespace_only(self):
        assert cleaner.clean("   ") == ""

    def test_mixed_punctuation_and_whitespace(self):
        assert cleaner.clean("  Hello, World!!  How are you?  ") == "hello world how are you"

    def test_commas_and_semicolons(self):
        assert cleaner.clean("set, altitude; 300") == "set altitude 300"

    def test_quotes(self):
        assert cleaner.clean('"go to point alpha"') == "go to point alpha"

    def test_colons(self):
        assert cleaner.clean("target: alpha") == "target alpha"

    def test_parens(self):
        assert cleaner.clean("avoid (sector bravo)") == "avoid sector bravo"

    def test_dashes_as_separators(self):
        assert cleaner.clean("go to -- point") == "go to point"

    def test_no_change_needed(self):
        assert cleaner.clean("go up to 500 meters") == "go up to 500 meters"