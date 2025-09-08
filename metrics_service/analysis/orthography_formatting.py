# orthography and formatting metrics

import re


def find_spelling_mistakes(text: str, wordbank=None) -> dict:
    """
    o(1) look up from globally stored set() of norwegian words.
    """
    if not text or not text.strip():
        return {"spelling_error_count": 0, "spelling_error_list": []}
    
    if wordbank is None:
        raise ValueError("wordbank parameter is required")

    mistakes = []
    word_pattern = re.compile(r'\b[a-zA-ZæøåÆØÅ]+\b')
    
    for match in word_pattern.finditer(text):
        word = match.group().lower()
        position = match.start()
        # skip one-letter words
        if len(word) <= 1:
            continue

        # check if word exists in dictionary
        if word not in wordbank:
            # crude filter: skip long inflected forms, can be fixed better later
            if len(word) > 10 and any(
                word.endswith(sfx) for sfx in ["en", "et", "a", "ene", "ern", "ane"]
            ):
                continue

            mistakes.append({"word": match.group(), "position": position})
    total_words = len(re.findall(r'\b[a-zA-ZæøåÆØÅ]+\b', text))
    return {
        "total_amount_of_words" : total_words, 
        "spelling_error_count": len(mistakes),
        "spelling_error_list": mistakes
    }


def calculate_capitalization_ratio(text: str) -> float:
    # ratio of capitalized words
    if not text or not text.strip():
        return 0.0

    words = re.findall(r'\b[a-zA-ZæøåÆØÅ]+\b', text)
    if not words:
        return 0.0

    capitalized_count = sum(1 for word in words if word[0].isupper())
    return capitalized_count / len(words)


def calculate_uppercase_letter_ratio(text: str) -> float:
    # ratio of uppercase letters
    if not text or not text.strip():
        return 0.0

    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0

    uppercase_count = sum(1 for c in letters if c.isupper())
    return uppercase_count / len(letters)


def calculate_lowercase_letter_ratio(text: str) -> float:
    # ratio of lowercase letters
    if not text or not text.strip():
        return 0.0

    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0

    lowercase_count = sum(1 for c in letters if c.islower())
    return lowercase_count / len(letters)


def calculate_digits_ratio(text: str) -> float:
    # ratio of digits to chars
    if not text or not text.strip():
        return 0.0

    total_chars = len([c for c in text if not c.isspace()])
    if total_chars == 0:
        return 0.0

    digit_count = sum(1 for c in text if c.isdigit())
    return digit_count / total_chars