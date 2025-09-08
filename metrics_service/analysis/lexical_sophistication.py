# lexical sophistication metrics

import re


def calculate_long_word_ratio(text: str) -> float:
    # ratio of long words (>=7 chars)
    if not text or not text.strip():
        return 0.0

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text)
    if not words:
        return 0.0

    long_words = [w for w in words if len(w) >= 7]
    return len(long_words) / len(words)


def calculate_avg_word_length(text: str) -> float:
    if not text or not text.strip():
        return 0.0

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text)
    if not words:
        return 0.0

    total_length = sum(len(word) for word in words)
    return total_length / len(words)