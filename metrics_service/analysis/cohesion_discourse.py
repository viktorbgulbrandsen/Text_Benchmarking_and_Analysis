# connectives and pronouns

import re


def calculate_connective_density(text: str, connectives=None) -> float:
    # connective density using o(1) lookup
    if not text or not text.strip():
        return 0.0
    
    if connectives is None:
        raise ValueError("connectives parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    connective_count = sum(1 for word in words if word in connectives["all_connectives"])
    return connective_count / len(words)


def calculate_pronoun_density(text: str, pronouns=None) -> float:
    """
    same
    """
    if not text or not text.strip():
        return 0.0
    
    if pronouns is None:
        raise ValueError("pronouns parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    pronoun_count = sum(1 for word in words if word in pronouns["all_pronouns"])
    return pronoun_count / len(words)


def calculate_first_person_pronoun_ratio(text: str, pronouns=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if pronouns is None:
        raise ValueError("pronouns parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    first_person_count = sum(1 for word in words if word in pronouns["first_person"])
    return first_person_count / len(words)


def calculate_second_person_pronoun_ratio(text: str, pronouns=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if pronouns is None:
        raise ValueError("pronouns parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    second_person_count = sum(1 for word in words if word in pronouns["second_person"])
    return second_person_count / len(words)


def calculate_third_person_pronoun_ratio(text: str, pronouns=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if pronouns is None:
        raise ValueError("pronouns parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    third_person_count = sum(1 for word in words if word in pronouns["third_person"])
    return third_person_count / len(words)


def calculate_causal_connective_ratio(text: str, connectives=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if connectives is None:
        raise ValueError("connectives parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    causal_count = sum(1 for word in words if word in connectives["causal"])
    return causal_count / len(words)


def calculate_connective_ratios(text: str, connectives=None) -> dict:
    if not text or not text.strip():
        return {
            "coordinating_connective_ratio": 0.0,
            "subordinating_connective_ratio": 0.0,
            "causal_connective_ratio": 0.0
        }
    
    if connectives is None:
        raise ValueError("connectives parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return {
            "coordinating_connective_ratio": 0.0,
            "subordinating_connective_ratio": 0.0,
            "causal_connective_ratio": 0.0
        }

    total_words = len(words)
    coordinating_count = sum(1 for word in words if word in connectives["coordinating"])
    subordinating_count = sum(1 for word in words if word in connectives["subordinating"])
    causal_count = sum(1 for word in words if word in connectives["causal"])

    return {
        "coordinating_connective_ratio": coordinating_count / total_words,
        "subordinating_connective_ratio": subordinating_count / total_words,
        "causal_connective_ratio": causal_count / total_words
    }