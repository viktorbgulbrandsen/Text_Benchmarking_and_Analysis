# basic text counts and averages

import re


def calculate_sentence_metrics(text: str, nlp=None) -> dict:
    # sentence metrics
    if not text or not text.strip():
        return {
            "avg_sentence_length": 0.0,
            "var_sentence_length": 0.0,
            "avg_word_length": 0.0
        }
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    sentences = list(doc.sents)

    sentence_lengths = []
    words = []

    for sent in sentences:
        sent_words = [token for token in sent if token.is_alpha]
        if sent_words:
            sentence_lengths.append(len(sent_words))
            words.extend(sent_words)

    if not sentence_lengths or not words:
        return {
            "avg_sentence_length": 0.0,
            "var_sentence_length": 0.0,
            "avg_word_length": 0.0
        }

    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    var_sentence_length = sum((l - avg_sentence_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
    avg_word_length = sum(len(token.text) for token in words) / len(words)

    return {
        "avg_sentence_length": avg_sentence_length,
        "var_sentence_length": var_sentence_length,
        "avg_word_length": avg_word_length
    }


def calculate_token_count(text: str, nlp=None) -> int:
    # token count
    if not text or not text.strip():
        return 0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    return len(doc)


def calculate_word_count(text: str, nlp=None) -> int:
    # word count
    if not text or not text.strip():
        return 0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    return len([token for token in doc if token.is_alpha])


def calculate_sentence_count(text: str, nlp=None) -> int:
    # sentence count
    if not text or not text.strip():
        return 0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    return len(list(doc.sents))


def calculate_avg_sentence_length(text: str, nlp=None) -> float:
    # avg sentence length
    if not text or not text.strip():
        return 0.0
    
    if nlp is None:
        raise ValueError("nlp parameter is required")

    doc = nlp(text)
    sentences = list(doc.sents)
    
    sentence_lengths = []
    for sent in sentences:
        sent_words = [token for token in sent if token.is_alpha]
        if sent_words:
            sentence_lengths.append(len(sent_words))

    if not sentence_lengths:
        return 0.0

    return sum(sentence_lengths) / len(sentence_lengths)