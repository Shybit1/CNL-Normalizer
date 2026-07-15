"""
Tests for the stopwords module.
"""

import stopwords


class TestRemoveStopwords:
    def test_please(self):
        assert stopwords.remove_stopwords("please climb") == "climb"

    def test_could(self):
        assert stopwords.remove_stopwords("could you climb") == "climb"

    def test_multiple_stopwords(self):
        result = stopwords.remove_stopwords("could you please climb")
        assert result == "climb"

    def test_the(self):
        assert stopwords.remove_stopwords("go to the waypoint") == "go to waypoint"

    def test_a_and_an(self):
        assert stopwords.remove_stopwords("a drone and an alt") == "drone and alt"

    def test_just(self):
        assert stopwords.remove_stopwords("just hover") == "hover"

    def test_kindly(self):
        assert stopwords.remove_stopwords("kindly land") == "land"

    def test_can_you(self):
        assert stopwords.remove_stopwords("can you go") == "go"

    def test_would(self):
        assert stopwords.remove_stopwords("would you go") == "go"

    def test_all_stopwords_sentence(self):
        result = stopwords.remove_stopwords(
            "could you please kindly climb to 500 meters"
        )
        assert result == "climb to 500 meters"

    def test_no_stopwords(self):
        assert stopwords.remove_stopwords("climb to 500 meters") == "climb to 500 meters"

    def test_empty_string(self):
        assert stopwords.remove_stopwords("") == ""

    def test_only_stopwords(self):
        result = stopwords.remove_stopwords("please could you a the")
        assert result == ""

    def test_okay(self):
        assert stopwords.remove_stopwords("okay go") == "go"

    def test_um_uh(self):
        assert stopwords.remove_stopwords("um go to uh alpha") == "go to alpha"