"""
numbers.py — Stage 3 of the CNL Normalizer pipeline.

Converts number words (e.g., "five hundred") to digits (e.g., "500").
Uses the word2number library for robust conversion.

Only attempts conversion on phrases composed of known number-related
words to avoid false positives (e.g., "a" → "1", "alpha" matched as a number).
"""

from word2number import w2n

# Words that indicate the start or presence of a number phrase.
# These are the only words that will trigger a number conversion attempt.
NUMBER_WORDS = {
    # Digits
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
    "20", "30", "40", "50", "60", "70", "80", "90",
    "100", "200", "300", "400", "500", "600", "700", "800", "900",
    "1000", "million", "billion",
    # Number words
    "zero", "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen",
    "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
    "eighty", "ninety",
    "hundred", "thousand",
    # Hyphenated forms
    "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five",
    "twenty-six", "twenty-seven", "twenty-eight", "twenty-nine",
    "thirty-one", "thirty-two", "thirty-three", "thirty-four", "thirty-five",
    "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine",
    "forty-one", "forty-two", "forty-three", "forty-four", "forty-five",
    "forty-six", "forty-seven", "forty-eight", "forty-nine",
    "fifty-one", "fifty-two", "fifty-three", "fifty-four", "fifty-five",
    "fifty-six", "fifty-seven", "fifty-eight", "fifty-nine",
    "sixty-one", "sixty-two", "sixty-three", "sixty-four", "sixty-five",
    "sixty-six", "sixty-seven", "sixty-eight", "sixty-nine",
    "seventy-one", "seventy-two", "seventy-three", "seventy-four",
    "seventy-five", "seventy-six", "seventy-seven", "seventy-eight",
    "seventy-nine",
    "eighty-one", "eighty-two", "eighty-three", "eighty-four",
    "eighty-five", "eighty-six", "eighty-seven", "eighty-eight",
    "eighty-nine",
    "ninety-one", "ninety-two", "ninety-three", "ninety-four",
    "ninety-five", "ninety-six", "ninety-seven", "ninety-eight",
    "ninety-nine",
    # Conjunctions that appear inside number phrases
    "and",
}

# We explicitly do NOT include "a" or "an" as number words.


def normalize_numbers(text: str) -> str:
    """
    Convert word-based numbers to digit strings.

    Only attempts conversion on phrases where at least the first word
    is a known number-related word, to avoid false positives.

    Args:
        text: Text string with potential number words.

    Returns:
        Text with number words replaced by digit strings.
    """
    if not text:
        return ""

    tokens = text.split()
    result = []
    i = 0

    while i < len(tokens):
        # Check if current token could start a number phrase
        if tokens[i] in NUMBER_WORDS:
            number_found = False

            for end in range(min(i + 12, len(tokens)), i, -1):
                phrase = " ".join(tokens[i:end])
                # Quick check: do all tokens look number-ish?
                all_numberish = all(
                    t in NUMBER_WORDS or t.replace("-", "").isdigit()
                    for t in tokens[i:end]
                )
                if not all_numberish:
                    continue

                try:
                    num_val = w2n.word_to_num(phrase)
                    result.append(str(num_val))
                    i = end
                    number_found = True
                    break
                except (ValueError, IndexError):
                    continue

            if not number_found:
                result.append(tokens[i])
                i += 1
        else:
            result.append(tokens[i])
            i += 1

    return " ".join(result)