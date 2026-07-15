"""
synonyms.py — Stage 2 of the CNL Normalizer pipeline.

Maps verb and phrase variants to canonical command verbs.
All canonical verbs are UPPERCASE to make them distinguishable
in the final output.
"""

CANONICAL_VERBS = {
    # CLIMB variants
    "climb": "CLIMB",
    "ascend": "CLIMB",
    "rise": "CLIMB",
    "go up": "CLIMB",
    "go upward": "CLIMB",
    "take us up": "CLIMB",
    "increase altitude": "CLIMB",
    "gain altitude": "CLIMB",

    # DESCEND variants
    "descend": "DESCEND",
    "go down": "DESCEND",
    "go downward": "DESCEND",
    "drop": "DESCEND",
    "decrease altitude": "DESCEND",
    "lose altitude": "DESCEND",
    "sink": "DESCEND",

    # GO variants
    "go": "GO",
    "move": "GO",
    "proceed": "GO",
    "travel": "GO",
    "fly": "GO",
    "head": "GO",
    "navigate": "GO",
    "advance": "GO",

    # RTL (Return To Launch) variants
    "return to launch": "RTL",
    "return to base": "RTL",
    "go home": "RTL",
    "rtl": "RTL",
    "come back": "RTL",
    "return": "RTL",

    # LOITER variants
    "loiter": "LOITER",
    "hover": "LOITER",
    "hold position": "LOITER",
    "stay": "LOITER",
    "remain": "LOITER",
    "circle": "LOITER",
    "orbit": "LOITER",

    # FORMATION variants
    "formation": "FORMATION",
    "form up": "FORMATION",
    "get into formation": "FORMATION",
    "assume formation": "FORMATION",

    # LAND variants
    "land": "LAND",
    "touch down": "LAND",
    "set down": "LAND",

    # TAKEOFF variants
    "take off": "TAKEOFF",
    "launch": "TAKEOFF",
    "lift off": "TAKEOFF",

    # AVOID variants
    "avoid": "AVOID",
    "stay clear of": "AVOID",
    "keep away from": "AVOID",

    # SCAN variants
    "scan": "SCAN",
    "survey": "SCAN",
    "search": "SCAN",
    "recon": "SCAN",
    "reconnoiter": "SCAN",

    # FOLLOW variants
    "follow": "FOLLOW",
    "track": "FOLLOW",
    "pursue": "FOLLOW",

    # REPORT variants
    "report": "REPORT",
    "declare": "REPORT",
    "announce": "REPORT",
    "transmit": "REPORT",

    # SET variants
    "set": "SET",
    "configure": "SET",
    "adjust": "SET",
}

# Multi-word synonyms must be sorted by length (descending) so longer
# phrases match before substrings of them (e.g., "go up" before "go").
MULTI_WORD_SYNONYMS = {
    phrase: canonical
    for phrase, canonical in sorted(CANONICAL_VERBS.items(), key=lambda x: -len(x[0].split()))
    if " " in phrase
}


def replace_synonyms(text: str) -> str:
    """
    Replace verb and phrase synonyms with canonical command verbs.

    Multi-word phrases are matched first (longest-first) to avoid
    partial matches. Single-word synonyms are then replaced.

    Args:
        text: Cleaned text string (lowercase, without punctuation).

    Returns:
        Text with synonyms replaced by canonical UPPERCASE verbs.
    """
    if not text:
        return ""

    tokens = text.split()
    output = []
    i = 0

    while i < len(tokens):
        matched = False

        # Try multi-word synonyms first (longest first)
        for phrase, canonical in MULTI_WORD_SYNONYMS.items():
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

        # Single word lookup
        word = tokens[i]
        if word in CANONICAL_VERBS:
            output.append(CANONICAL_VERBS[word])
        else:
            output.append(word)

        i += 1

    return " ".join(output)