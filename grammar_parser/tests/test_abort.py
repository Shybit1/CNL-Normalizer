"""
Tests for abort commands (RTL, RETURN HOME, ABORT).
"""

from grammar_parser import parse, Intent


class TestAbortCommands:
    """Valid abort commands."""

    def test_rtl(self):
        r = parse("RTL")
        assert r.success is True
        assert r.intent == Intent.ABORT_RTL
        assert r.slots["action"] == "rtl"

    def test_return_home(self):
        r = parse("RETURN HOME")
        assert r.success is True
        assert r.intent == Intent.ABORT_RTL
        assert r.slots["action"] == "return_home"

    def test_abort(self):
        r = parse("ABORT")
        assert r.success is True
        assert r.intent == Intent.ABORT_RTL
        assert r.slots["action"] == "abort"


class TestAbortErrors:
    """Invalid abort commands."""

    def test_return_no_home(self):
        r = parse("RETURN")
        assert r.success is False

    def test_return_wrong_word(self):
        r = parse("RETURN BASE")
        assert r.success is False

    def test_rtl_with_extra(self):
        r = parse("RTL NOW")
        assert r.success is True  # Extra tokens allowed but flagged
        assert "extra" in r.slots