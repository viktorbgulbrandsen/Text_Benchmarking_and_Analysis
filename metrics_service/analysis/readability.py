# readability calculations

import re
import math


def calculate_lix(text: str) -> float:
    # lix readability score
    if not text or not text.strip():
        return 0.0

    sentences = re.split(r'[.!?]+', text.strip())
    sentence_count = len([s for s in sentences if s.strip()])
    if sentence_count == 0:
        return 0.0

    words = re.findall(r'[a-zA-ZæøåÆØÅ]+', text)
    word_count = len(words)
    if word_count == 0:
        return 0.0

    long_word_count = len([word for word in words if len(word) >= 7])
    lix_score = (word_count / sentence_count) + (100 * long_word_count / word_count)

    return lix_score


def calculate_sentence_length_std_dev(text: str, nlp=None) -> float:
    # sentence length standard deviation
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

    if len(sentence_lengths) < 2:
        return 0.0

    avg_length = sum(sentence_lengths) / len(sentence_lengths)
    variance = sum((l - avg_length) ** 2 for l in sentence_lengths) / len(sentence_lengths)
    
    return math.sqrt(variance)