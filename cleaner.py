"""
cleaner.py — Stage 1 of the CNL Normalizer pipeline.

Performs normalization of raw input text:
- Converts to lowercase
- Removes punctuation (except hyphens within words and apostrophes within words)
- Collapses whitespace (tabs, newlines, multiple spaces)
- Trims leading/trailing whitespace
"""

import re


def clean(text: str) -> str:
    """
    Clean input text: lowercase, strip punctuation, collapse whitespace, trim.

    Args:
        text: Raw input string.

    Returns:
        Cleaned string ready for downstream pipeline stages.
    """
    if not text or not text.strip():
        return ""

    # Lowercase
    t = text.lower()

    # Remove punctuation — keep hyphens and apostrophes within words
    # Replace punctuation (not hyphens/apostrophes within words) with space
    t = re.sub(r"[^\w\s'-]", " ", t)

    # Replace standalone hyphens/dashes (not part of a word) with spaces
    # A hyphen is standalone if it's surrounded by spaces or at start/end
    t = re.sub(r"(?<!\w)-(?!\w)", " ", t)

    # Collapse whitespace (tabs, newlines, multiple spaces) to single space
    t = re.sub(r"\s+", " ", t)

    # Trim
    t = t.strip()

    return t