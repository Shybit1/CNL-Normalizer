"""
stopwords.py — Stage 5 of the CNL Normalizer pipeline.

Removes filler words that carry no command meaning.
"""
# Filler words to remove (case-insensitive, but input is already lowercase)
STOPWORDS = frozenset({
    "please",
    "could",
    "would",
    "kindly",
    "can",
    "you",
    "the",
    "a",
    "an",
    "just",
    "maybe",
    "perhaps",
    "like",
    "um",
    "uh",
    "well",
    "so",
    "okay",
    "alright",
    "while",
    "whilst",
})


def remove_stopwords(text: str) -> str:
    """
    Remove filler/stopwords from text.

    Args:
        text: Text string with possible filler words.

    Returns:
        Text with filler words removed (whitespace re-collapsed).
    """
    if not text:
        return ""

    tokens = text.split()
    filtered = [t for t in tokens if t not in STOPWORDS]

    return " ".join(filtered)