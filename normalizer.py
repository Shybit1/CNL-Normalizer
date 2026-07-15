"""
normalizer.py — Orchestrator for the CNL Normalizer pipeline.

Runs all 6 stages in sequence to convert raw natural-language
drone commands into canonical form.
"""

import cleaner
import synonyms
import numwords
import units
import stopwords
import entities


def normalize(text: str) -> str:
    """
    Normalize a natural-language drone command to canonical form.

    Pipeline stages:
    1. cleaner  — lowercase, strip punctuation, collapse whitespace
    2. synonyms — verb/phrase synonyms → canonical verbs
    3. numbers  — word numbers → digit strings
    4. units    — unit variants → canonical units
    5. stopwords — remove filler words
    6. entities — waypoint/formation names → uppercase
    7. cleaner  — final cleanup pass (spacing)
    8. upper    — final canonical uppercase

    Args:
        text: Raw natural-language command.

    Returns:
        Canonicalized command string.
    """
    if not text or not text.strip():
        return ""

    t = cleaner.clean(text)
    t = synonyms.replace_synonyms(t)
    t = numwords.normalize_numbers(t)
    t = units.normalize_units(t)
    t = stopwords.remove_stopwords(t)
    t = entities.normalize_entities(t)
    t = cleaner.clean(t)  # final pass for spacing
    return t.upper()  # final canonical form