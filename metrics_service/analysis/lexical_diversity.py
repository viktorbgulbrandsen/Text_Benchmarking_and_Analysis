"""
contains code for 
lexical density
inflectional diversity
hapax legomena
TTR
moving average TTR
"""

import re
from typing import Dict, Set


def calculate_lexical_density(text: str, doc=None, nlp=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if doc is None:
        if nlp is None:
            raise ValueError("Either doc or nlp parameter is required")
        doc = nlp(text)
    words = [token.text for token in doc if token.is_alpha]
    if not words:
        return 0.0

    unique_words = set(word.lower() for word in words)
    lexical_density = len(unique_words) / len(words)

    return lexical_density


def calculate_inflectional_diversity(text: str, form_to_lemma=None) -> float:
    if not text or not text.strip():
        return 0.0
    
    if form_to_lemma is None:
        raise ValueError("form_to_lemma parameter is required")

    words = [w.lower() for w in re.findall(r"\b[a-zA-ZæøåÆØÅ]+\b", text)]
    lemma_usage: Dict[str, Set[str]] = {}

    for word in words:
        lemma = form_to_lemma.get(word)
        if lemma:
            lemma_usage.setdefault(lemma, set()).add(word)

    if not lemma_usage:
        return 0.0

    total_forms = sum(len(forms) for forms in lemma_usage.values())
    return total_forms / len(lemma_usage)


def calculate_hapax_legomena_ratio(text: str) -> float:
    # words appearing exactly once
    if not text or not text.strip():
        return 0.0

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    hapax_count = sum(1 for count in freq.values() if count == 1)
    return hapax_count / len(words)


def calculate_ttr(text: str) -> float:
    # type-token ratio
    if not text or not text.strip():
        return 0.0

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    unique_words = set(words)
    return len(unique_words) / len(words)


def calculate_moving_average_ttr(text: str, window_size: int = 100) -> float:
    # moving average TTR
    if not text or not text.strip():
        return 0.0

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if len(words) < window_size:
        return calculate_ttr(text)

    ttrs = []
    for i in range(len(words) - window_size + 1):
        window_words = words[i:i + window_size]
        unique_words = set(window_words)
        ttr = len(unique_words) / len(window_words)
        ttrs.append(ttr)

    return sum(ttrs) / len(ttrs) if ttrs else 0.0