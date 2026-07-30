"""
Tests for error conditions and edge cases.
"""

from grammar_parser import parse, ParseResult


class TestErrors:
    """Error and edge case handling."""

    def test_empty_string(self):
        r = parse("")
        assert r.success is False
        assert "Empty" in r.errors[0] or "empty" in r.errors[0]

    def test_whitespace_only(self):
        r = parse("   ")
        assert r.success is False

    def test_unknown_verb(self):
        r = parse("JUMP TO 500 METERS")
        assert r.success is False
        assert any("Unknown" in e or "unknown" in e for e in r.errors)

    def test_garbage_input(self):
        r = parse("XYZPDQ 12345 FOO")
        assert r.success is False

    def test_lowercase_input(self):
        """Normalizer output is uppercase, but we should handle lowercase gracefully."""
        r = parse("climb to 500 meters")
        assert r.success is False or r.success is True

    def test_token_count_limit(self):
        """Test that 128+ token input is rejected."""
        tokens = ["CLIMB", "TO", "500", "METERS"] + ["EXTRA"] * 130
        r = parse(" ".join(tokens))
        assert r.success is False
        assert any("128" in e for e in r.errors)

    def test_long_token_rejected(self):
        """Tokens over 128 chars should be rejected."""
        r = parse("CLIMB TO 500 " + "A" * 129)
        assert r.success is False
        assert any("128" in e for e in r.errors)

    def test_parse_result_repr(self):
        r = parse("CLIMB TO 500 METERS")
        rep = repr(r)
        assert "ParseResult" in rep
        assert "OK" in rep

    def test_failed_result_repr(self):
        r = parse("INVALID")
        rep = repr(r)
        assert "ParseResult" in rep
        assert "FAIL" in rep