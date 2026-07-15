"""
entities.py — Stage 6 of the CNL Normalizer pipeline.

Normalizes named entities: waypoint names, formation names, and
other predefined proper nouns to uppercase canonical form.
"""

# Waypoint/zone names → canonical uppercase
WAYPOINTS = {
    "alpha": "ALPHA",
    "bravo": "BRAVO",
    "charlie": "CHARLIE",
    "delta": "DELTA",
    "echo": "ECHO",
    "foxtrot": "FOXTROT",
    "golf": "GOLF",
    "hotel": "HOTEL",
    "india": "INDIA",
    "juliett": "JULIETT",
    "kilo": "KILO",
    "lima": "LIMA",
    "mike": "MIKE",
    "november": "NOVEMBER",
    "oscar": "OSCAR",
    "papa": "PAPA",
    "quebec": "QUEBEC",
    "romeo": "ROMEO",
    "sierra": "SIERRA",
    "tango": "TANGO",
    "uniform": "UNIFORM",
    "victor": "VICTOR",
    "whiskey": "WHISKEY",
    "xray": "XRAY",
    "yankee": "YANKEE",
    "zulu": "ZULU",
    "sector": "SECTOR",
    "zone": "ZONE",
    "point": "POINT",
    "waypoint": "WAYPOINT",
    "home": "HOME",
    "base": "BASE",
    "rally": "RALLY",
    "landing": "LANDING",
}

# Formation names
# "avoiding sector alpha" → "AVOIDING SECTOR ALPHA" but we process entities after stopwords,
# so "sector alpha" remains. These get normalized to uppercase.
# But "sector" is also a waypoint-related word, so it gets uppercased.
# Multi-word formation names
FORMATION_WORDS = {
    "wedge": "WEDGE",
    "diamond": "DIAMOND",
    "line": "LINE",
    "echelon": "ECHELON",
    "staggered": "STAGGERED",
    "trail": "TRAIL",
    "column": "COLUMN",
    "arrowhead": "ARROWHEAD",
    "box": "BOX",
    "v": "V",
    "vic": "VIC",
    "finger": "FINGER",
    "four": "FOUR",
}

# Combine all entity mappings
ENTITY_WORDS = {}
ENTITY_WORDS.update(WAYPOINTS)
ENTITY_WORDS.update(FORMATION_WORDS)


def normalize_entities(text: str) -> str:
    """
    Normalize named entities (waypoints, formations) to canonical uppercase.

    Args:
        text: Text string with potential entity names.

    Returns:
        Text with entity names uppercased.
    """
    if not text:
        return ""

    tokens = text.split()
    result = []

    for token in tokens:
        if token in ENTITY_WORDS:
            result.append(ENTITY_WORDS[token])
        else:
            result.append(token)

    return " ".join(result)