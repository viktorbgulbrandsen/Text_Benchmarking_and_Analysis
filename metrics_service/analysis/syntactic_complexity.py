# pos ratios and content words

import re


def calculate_pos_ratios(text: str, nlp=None) -> dict:
    # returns dict of all pos ratios
    if not text or not text.strip():
        return {}
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    tokens = [token for token in doc if token.is_alpha]
    total_tokens = len(tokens)
    if total_tokens == 0:
        return {}

    pos_counts = {}
    for token in tokens:
        pos = token.pos_
        pos_counts[pos] = pos_counts.get(pos, 0) + 1

    # Convert counts to ratios
    return {f"pos_ratio_{pos.lower()}": count / total_tokens 
            for pos, count in pos_counts.items()}


def calculate_noun_ratio(text: str, nlp=None) -> float:
    # noun ratio
    if not text or not text.strip():
        return 0.0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    tokens = [token for token in doc if token.is_alpha]
    total_tokens = len(tokens)
    if total_tokens == 0:
        return 0.0

    noun_count = sum(1 for token in tokens if token.pos_ == "NOUN")
    return noun_count / total_tokens


def calculate_adjective_ratio(text: str, nlp=None) -> float:
    # adjective ratio
    if not text or not text.strip():
        return 0.0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    tokens = [token for token in doc if token.is_alpha]
    total_tokens = len(tokens)
    if total_tokens == 0:
        return 0.0

    adj_count = sum(1 for token in tokens if token.pos_ == "ADJ")
    return adj_count / total_tokens


def calculate_content_word_ratio(text: str, pos_categories=None) -> float:
    # content words (nouns/verbs/adj/adv) ratio
    if not text or not text.strip():
        return 0.0
    
    if pos_categories is None:
        raise ValueError("pos_categories parameter is required")

    words = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower())
    if not words:
        return 0.0

    content_count = sum(1 for word in words if word in pos_categories["content_words"])
    return content_count / len(words)