"""
Integration tests for the full grammar parser pipeline.
"""

from grammar_parser import parse, ParseResult, Intent


class TestParser:
    """End-to-end pipeline tests."""

    def test_normalizer_to_parser_chain(self):
        """Simulate a full command flowing from normalizer → parser."""
        from normalizer import normalize

        # Normalize raw commands
        raw_commands = [
            ("Go up to 500 meters.", "CLIMB TO 500 METERS"),
            ("Descend to 300 feet.", "DESCEND TO 300 FEET"),
            ("go to waypoint alpha", "GO TO WAYPOINT ALPHA"),
            ("formation wedge", "FORMATION WEDGE"),
            ("loiter for 30 seconds", "LOITER FOR 30 SECONDS"),
            ("rtl", "RTL"),
            ("return to launch", "RTL"),
            ("abort", "ABORT"),
        ]

        for raw, expected_canonical in raw_commands:
            canonical = normalize(raw)
            assert canonical == expected_canonical, f"Normalizer mismatch: {raw!r} → {canonical!r} != {expected_canonical!r}"
            r = parse(canonical)
            assert r.success is True, f"Parser failed for {canonical!r}: {r.errors}"

    def test_altitude_full_pipeline(self):
        """Normalizer → Parser chain for altitude commands."""
        from normalizer import normalize

        r = parse(normalize("ascend to 500 metres"))
        assert r.success is True
        assert r.intent == Intent.ALTITUDE_CHANGE
        assert r.slots["direction"] == "up"
        assert r.slots["target_altitude"] == 500
        assert r.slots["unit"] == "meters"

    def test_navigation_full_pipeline(self):
        """Normalizer → Parser chain for navigation."""
        from normalizer import normalize

        r = parse(normalize("Go to sector bravo"))
        assert r.success is True
        assert r.intent == Intent.WAYPOINT_NAVIGATION
        assert r.slots["target"] == "bravo"
        assert r.slots["waypoint_type"] == "sector"

    def test_formation_full_pipeline(self):
        """Normalizer → Parser chain for formation."""
        from normalizer import normalize

        r = parse(normalize("form up in wedge formation"))
        assert r.success is True
        assert r.intent == Intent.FORMATION_CHANGE
        assert r.slots["formation"] == "wedge"

    def test_loiter_full_pipeline(self):
        """Normalizer → Parser chain for loiter."""
        from normalizer import normalize

        r = parse(normalize("hover at 100 meters for 30 seconds"))
        assert r.success is True
        assert r.intent == Intent.HOLD_LOITER
        assert r.slots["target_altitude"] == 100
        assert r.slots["duration"] == 30

    def test_abort_full_pipeline(self):
        """Normalizer → Parser chain for abort."""
        from normalizer import normalize

        r = parse(normalize("return to base"))
        assert r.success is True
        assert r.intent == Intent.ABORT_RTL

    def test_deterministic(self):
        """Same input always produces same output."""
        r1 = parse("CLIMB TO 500 METERS")
        r2 = parse("CLIMB TO 500 METERS")
        assert r1 == r2
        assert r1.slots == r2.slots

    def test_thread_safe(self):
        """Multiple calls do not interfere."""
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(parse, "CLIMB TO 500 METERS")
                for _ in range(20)
            ]
            results = [f.result() for f in futures]

        for r in results:
            assert r.success is True
            assert r.slots["target_altitude"] == 500

    def test_intent_enum_string(self):
        """Intent enum should work as a string."""
        assert str(Intent.ALTITUDE_CHANGE) == "ALTITUDE_CHANGE"
        assert str(Intent.WAYPOINT_NAVIGATION) == "WAYPOINT_NAVIGATION"