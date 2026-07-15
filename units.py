"""
units.py — Stage 4 of the CNL Normalizer pipeline.

Normalizes unit variants to canonical uppercase unit names.
"""

# Unit synonyms → canonical form
UNIT_MAP = {
    # Meters
    "meter": "METERS",
    "meters": "METERS",
    "m": "METERS",
    "metre": "METERS",
    "metres": "METERS",

    # Kilometers
    "kilometer": "KILOMETERS",
    "kilometers": "KILOMETERS",
    "km": "KILOMETERS",
    "kilometre": "KILOMETERS",
    "kilometres": "KILOMETERS",
    "klick": "KILOMETERS",
    "klicks": "KILOMETERS",

    # Feet
    "foot": "FEET",
    "feet": "FEET",
    "ft": "FEET",

    # Seconds
    "second": "SECONDS",
    "seconds": "SECONDS",
    "sec": "SECONDS",
    "secs": "SECONDS",
    "s": "SECONDS",

    # Minutes
    "minute": "MINUTES",
    "minutes": "MINUTES",
    "min": "MINUTES",
    "mins": "MINUTES",

    # Hours
    "hour": "HOURS",
    "hours": "HOURS",
    "hr": "HOURS",
    "hrs": "HOURS",

    # Kilometers per hour
    "kilometers per hour": "KMH",
    "kilometres per hour": "KMH",
    "km/h": "KMH",
    "kmh": "KMH",
    "kph": "KMH",
    "klicks per hour": "KMH",

    # Miles per hour
    "miles per hour": "MPH",
    "mile per hour": "MPH",
    "mph": "MPH",
    "mi/h": "MPH",

    # Meters per second
    "meters per second": "MPS",
    "metres per second": "MPS",
    "m/s": "MPS",
    "mps": "MPS",

    # Knots
    "knot": "KNOTS",
    "knots": "KNOTS",
    "kt": "KNOTS",
    "kts": "KNOTS",

    # Degrees
    "degree": "DEGREES",
    "degrees": "DEGREES",
    "deg": "DEGREES",
    "degs": "DEGREES",

    # Percentage
    "percent": "PERCENT",
    "per cent": "PERCENT",
    "%": "PERCENT",
    "percentage": "PERCENT",
}

# Multi-word units must be matched before single-word units
MULTI_WORD_UNITS = {
    phrase: canonical
    for phrase, canonical in sorted(UNIT_MAP.items(), key=lambda x: -len(x[0].split()))
    if " " in phrase
}

# Slash-notation units: after the cleaner removes "/", "m/s" becomes "m s".
# We need to match these multi-token patterns as compound units.
# These are ordered longest-first to avoid partial matches.
COMPOUND_UNITS = {
    "m s": "MPS",
    "m sec": "MPS",
    "m seconds": "MPS",
    "km h": "KMH",
    "km hour": "KMH",
    "km hours": "KMH",
    "mi h": "MPH",
    "mi hour": "MPH",
    "mi hours": "MPH",
    "knots h": "KNOTS",
    "kt h": "KNOTS",
    "kts h": "KNOTS",
}

# Sort compound units by length (longest first)
COMPOUND_UNITS_SORTED = sorted(COMPOUND_UNITS.items(), key=lambda x: -len(x[0].split()))


def normalize_units(text: str) -> str:
    """
    Replace unit variants with canonical uppercase unit names.

    Multi-word units (e.g., "kilometers per hour") are matched first
    to avoid partial matches (e.g., "kilometers" matched before
    "kilometers per hour").

    Args:
        text: Text string with potential unit names.

    Returns:
        Text with units normalized to canonical form.
    """
    if not text:
        return ""

    tokens = text.split()
    output = []
    i = 0

    while i < len(tokens):
        matched = False

        # Multi-word units (longest first)
        for phrase, canonical in MULTI_WORD_UNITS.items():
            phrase_tokens = phrase.split()
            if i + len(phrase_tokens) <= len(tokens):
                candidate = " ".join(tokens[i:i + len(phrase_tokens)])
                if candidate == phrase:
                    output.append(canonical)
                    i += len(phrase_tokens)
                    matched = True
                    break

        if matched:
            continue

        # Compound units from slash notation (e.g., "m s" from "m/s")
        for phrase, canonical in COMPOUND_UNITS_SORTED:
            phrase_tokens = phrase.split()
            if i + len(phrase_tokens) <= len(tokens):
                candidate = " ".join(tokens[i:i + len(phrase_tokens)])
                if candidate == phrase:
                    output.append(canonical)
                    i += len(phrase_tokens)
                    matched = True
                    break

        if matched:
            continue

        # Single word unit
        word = tokens[i]
        if word in UNIT_MAP:
            output.append(UNIT_MAP[word])
        else:
            output.append(word)

        i += 1

    return " ".join(output)