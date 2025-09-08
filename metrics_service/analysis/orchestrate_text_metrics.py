# File: analysis/orchestrate_text_metrics.py
# Part of: text-analysis project

import re
import math

# Lexical diversity functions
from .lexical_diversity import (
    calculate_lexical_density,
    calculate_inflectional_diversity,
    calculate_hapax_legomena_ratio,
    calculate_ttr,
    calculate_moving_average_ttr
)

# Lexical sophistication functions
from .lexical_sophistication import (
    calculate_long_word_ratio,
    calculate_avg_word_length
)

# Readability functions
from .readability import (
    calculate_lix,
    calculate_sentence_length_std_dev
)

# Syntactic complexity functions
from .syntactic_complexity import (
    calculate_pos_ratios,
    calculate_noun_ratio,
    calculate_adjective_ratio,
    calculate_content_word_ratio
)

# Text productivity functions
from .text_productivity import (
    calculate_sentence_metrics,
    calculate_token_count,
    calculate_word_count,
    calculate_sentence_count,
    calculate_avg_sentence_length
)

# Orthography and formatting functions
from .orthography_formatting import (
    find_spelling_mistakes,
    calculate_capitalization_ratio,
    calculate_uppercase_letter_ratio,
    calculate_lowercase_letter_ratio,
    calculate_digits_ratio
)

# Punctuation mechanics functions
from .punctuation_mechanics import (
    calculate_punctuation_density,
    calculate_punctuation_counts,
    calculate_punctuation_diversity
)

# Cohesion and discourse functions
from .cohesion_discourse import (
    calculate_connective_density,
    calculate_pronoun_density,
    calculate_first_person_pronoun_ratio,
    calculate_second_person_pronoun_ratio,
    calculate_third_person_pronoun_ratio,
    calculate_causal_connective_ratio,
    calculate_connective_ratios
)

# Score calculation functions (keeping these for now as requested)


def normalize_score(values):
    # sigmoid normalization
    if not values:
        return 0.0
    avg = sum(values) / len(values)
    return 1 / (1 + math.exp(-avg))


def return_text_metrics(text: str, resources=None) -> dict:
    # text metrics suite
    
    if resources is None:
        raise ValueError("resources parameter is required")
    
    nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta = resources
    
    # SINGLE spaCy processing - do this ONCE and reuse everywhere
    doc = nlp(text) if text and text.strip() else None
    
    # Pre-compute common data structures for reuse
    words_lower = re.findall(r"[a-zA-ZæøåÆØÅ]+", text.lower()) if text else []
    tokens = [token for token in doc if token.is_alpha] if doc else []
    sentences = list(doc.sents) if doc else []
    
    # Lexical diversity metrics - using doc where possible, otherwise text
    lexical_density = calculate_lexical_density(text, doc=doc) if doc else 0.0
    inflectional_diversity = calculate_inflectional_diversity(text, form_to_lemma)
    hapax_legomena_ratio = calculate_hapax_legomena_ratio(text)
    ttr = calculate_ttr(text)
    moving_average_ttr = calculate_moving_average_ttr(text)
    
    # Lexical sophistication metrics - pure regex, no spaCy needed
    long_word_ratio = calculate_long_word_ratio(text)
    avg_word_length = calculate_avg_word_length(text)
    
    # Readability metrics - mix of regex and spaCy
    lix = calculate_lix(text)
    sentence_length_std_dev = calculate_sentence_length_std_dev(text, nlp) if doc else 0.0
    
    # Syntactic complexity metrics - mix of spaCy and O(1) lookups
    pos_ratios = calculate_pos_ratios(text, nlp) if doc else {}
    noun_ratio = calculate_noun_ratio(text, nlp) if doc else 0.0
    adjective_ratio = calculate_adjective_ratio(text, nlp) if doc else 0.0
    content_word_ratio = calculate_content_word_ratio(text, pos_categories)
    
    # Text productivity metrics - using doc
    sentence_metrics = calculate_sentence_metrics(text, nlp) if doc else {"avg_sentence_length": 0.0, "var_sentence_length": 0.0, "avg_word_length": 0.0}
    token_count = len(doc) if doc else 0
    word_count = len(tokens)
    sentence_count = len(sentences)
    avg_sentence_length = sentence_metrics["avg_sentence_length"]
    
    # Orthography and formatting metrics - no spaCy needed
    spelling_mistakes = find_spelling_mistakes(text, wordbank)
    capitalization_ratio = calculate_capitalization_ratio(text)
    uppercase_letter_ratio = calculate_uppercase_letter_ratio(text)
    lowercase_letter_ratio = calculate_lowercase_letter_ratio(text)
    digits_ratio = calculate_digits_ratio(text)
    
    # Punctuation mechanics metrics - no spaCy needed
    punctuation_density = calculate_punctuation_density(text)
    punctuation_counts = calculate_punctuation_counts(text)
    punctuation_diversity = calculate_punctuation_diversity(text)
    
    # Cohesion and discourse metrics - using O(1) lookups instead of spaCy!
    connective_density = calculate_connective_density(text, connectives)
    pronoun_density = calculate_pronoun_density(text, pronouns)
    first_person_pronoun_ratio = calculate_first_person_pronoun_ratio(text, pronouns)
    second_person_pronoun_ratio = calculate_second_person_pronoun_ratio(text, pronouns)
    third_person_pronoun_ratio = calculate_third_person_pronoun_ratio(text, pronouns)
    causal_connective_ratio = calculate_causal_connective_ratio(text, connectives)
    connective_ratios = calculate_connective_ratios(text, connectives)
    
    # Category scores - normalized with sigmoid to 0-1 range
    cohesion_discourse_score = normalize_score([
        connective_density, pronoun_density, first_person_pronoun_ratio,
        second_person_pronoun_ratio, third_person_pronoun_ratio,
        causal_connective_ratio
    ] + list(connective_ratios.values()))
    
    lexical_diversity_score = normalize_score([
        lexical_density, inflectional_diversity, hapax_legomena_ratio,
        ttr, moving_average_ttr
    ])
    
    lexical_sophistication_score = normalize_score([
        long_word_ratio, avg_word_length
    ])
    
    readability_score = normalize_score([
        lix, sentence_length_std_dev
    ])
    
    syntactic_complexity_score = normalize_score([
        noun_ratio, adjective_ratio, content_word_ratio
    ] + list(pos_ratios.values()))
    
    text_productivity_score = normalize_score([
        token_count, word_count, sentence_count, avg_sentence_length
    ] + list(sentence_metrics.values()))
    
    # For orthography - invert spelling error rate (higher errors = lower score)
    spelling_error_rate = spelling_mistakes["spelling_error_count"] / max(1, spelling_mistakes["total_amount_of_words"])
    orthography_formatting_score = normalize_score([
        capitalization_ratio, uppercase_letter_ratio, lowercase_letter_ratio,
        digits_ratio, 1 - spelling_error_rate
    ])
    
    punctuation_mechanics_score = normalize_score([
        punctuation_density, punctuation_diversity
    ] + list(punctuation_counts.values()))
    return {
        "metrics": {
            # Lexical diversity
            "lexical_density": lexical_density,
            "inflectional_diversity": inflectional_diversity,
            "hapax_legomena_ratio": hapax_legomena_ratio,
            "ttr": ttr,
            "moving_average_ttr": moving_average_ttr,
            
            # Lexical sophistication
            "long_word_ratio": long_word_ratio,
            "avg_word_length": avg_word_length,
            
            # Readability
            "lix": lix,
            "sentence_length_std_dev": sentence_length_std_dev,
            
            # Syntactic complexity
            **pos_ratios,
            "noun_ratio": noun_ratio,
            "adjective_ratio": adjective_ratio,
            "content_word_ratio": content_word_ratio,
            
            # Text productivity
            **sentence_metrics,
            "token_count": token_count,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            
            # Orthography and formatting
            "spelling_error_count": spelling_mistakes["spelling_error_count"],
            "capitalization_ratio": capitalization_ratio,
            "uppercase_letter_ratio": uppercase_letter_ratio,
            "lowercase_letter_ratio": lowercase_letter_ratio,
            "digits_ratio": digits_ratio,
            
            # Punctuation mechanics
            "punctuation_density": punctuation_density,
            **punctuation_counts,
            "punctuation_diversity": punctuation_diversity,
            
            # Cohesion and discourse
            "connective_density": connective_density,
            "pronoun_density": pronoun_density,
            "first_person_pronoun_ratio": first_person_pronoun_ratio,
            "second_person_pronoun_ratio": second_person_pronoun_ratio,
            "third_person_pronoun_ratio": third_person_pronoun_ratio,
            "causal_connective_ratio": causal_connective_ratio,
            **connective_ratios,
        },
        "scores": {
            "cohesion_discourse_score": cohesion_discourse_score,
            "lexical_diversity_score": lexical_diversity_score,
            "lexical_sophistication_score": lexical_sophistication_score,
            "readability_score": readability_score,
            "syntactic_complexity_score": syntactic_complexity_score,
            "text_productivity_score": text_productivity_score,
            "orthography_formatting_score": orthography_formatting_score,
            "punctuation_mechanics_score": punctuation_mechanics_score,
        },
    }