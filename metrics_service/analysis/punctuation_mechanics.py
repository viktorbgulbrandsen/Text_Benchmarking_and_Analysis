# punctuation metrics

import re
from collections import Counter


def calculate_punctuation_density(text: str) -> float:
    # punctuation density
    if not text or not text.strip():
        return 0.0

    total_chars = len([c for c in text if not c.isspace()])
    if total_chars == 0:
        return 0.0

    punctuation_count = len(re.findall(r'[^\w\s]', text))
    return punctuation_count / total_chars


def calculate_comma_count(text: str) -> int:
    # comma count
    if not text:
        return 0
    return text.count(',')


def calculate_period_count(text: str) -> int:
    # period count
    if not text:
        return 0
    return text.count('.')


def calculate_question_mark_count(text: str) -> int:
    # question mark count
    if not text:
        return 0
    return text.count('?')


def calculate_exclamation_mark_count(text: str) -> int:
    # exclamation mark count
    if not text:
        return 0
    return text.count('!')


def calculate_punctuation_diversity(text: str) -> float:
    # unique punctuation types
    if not text or not text.strip():
        return 0.0

    punctuation_marks = re.findall(r'[^\w\s]', text)
    if not punctuation_marks:
        return 0.0

    unique_punctuation = set(punctuation_marks)
    return len(unique_punctuation)


def calculate_punctuation_counts(text: str) -> dict:
    # punctuation counts
    if not text:
        return {
            "comma_count": 0,
            "period_count": 0,
            "question_mark_count": 0,
            "exclamation_mark_count": 0,
            "semicolon_count": 0,
            "colon_count": 0
        }

    return {
        "comma_count": text.count(','),
        "period_count": text.count('.'),
        "question_mark_count": text.count('?'),
        "exclamation_mark_count": text.count('!'),
        "semicolon_count": text.count(';'),
        "colon_count": text.count(':')
    }