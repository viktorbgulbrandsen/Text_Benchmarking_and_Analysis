# File: text-analysis/resources.py
# Part of: text-analysis project

import os
import time
import pickle
import spacy
from spacy.language import Language
from typing import Any, Tuple


WORDBANK_PKL = "data/norsk_ordbank/wordbank.pkl"
LEMMA_PKL    = "data/norsk_ordbank/lemma_data.pkl"
PRONOUNS_PKL = "data/norsk_ordbank/pronouns.pkl"
CONNECTIVES_PKL = "data/norsk_ordbank/connectives.pkl"
POS_CATEGORIES_PKL = "data/norsk_ordbank/pos_categories.pkl"
SPACY_MODEL  = "nb_core_news_md"


def load_spacy_model() -> Language:
    """
    Load the configured spaCy model, or raise with clear instructions.
    """
    t0 = time.perf_counter()
    try:
        nlp = spacy.load(SPACY_MODEL)
    except OSError as e:
        raise OSError(
            f"Failed to load spaCy model '{SPACY_MODEL}'. "
            f"spaCy version: {spacy.__version__}. "
            f"Install with: python -m spacy download {SPACY_MODEL}"
        ) from e
    t1 = time.perf_counter()
    meta = getattr(nlp, "meta", {})
    print(
        f"Loaded spaCy model '{SPACY_MODEL}' "
        f"(spaCy {spacy.__version__}, model {meta.get('version','?')}) "
        f"in {t1 - t0:.4f} seconds"
    )
    return nlp


def load_pickle(path: str) -> Any:
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Required pickle not found: {path}. "
            f"Run pickle_parse_ordbank.py to generate it."
        )
    with open(path, "rb") as f:
        return pickle.load(f)


def init_resources() -> Tuple[Language, Any, dict, dict, dict, dict, dict, dict]:
    """
    Initialize all heavy resources:
      - spaCy model
      - wordbank.pkl
      - lemma_data.pkl
      - pronouns.pkl
      - connectives.pkl
      - pos_categories.pkl

    Returns:
        (nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta)
    Where `meta` contains info like:
        {"spacy_version": "3.x.x", "model_name": "nb_core_news_md", "model_version": "..."}
    """
    nlp = load_spacy_model()
    meta = {
        "spacy_version": spacy.__version__,
        "model_name": SPACY_MODEL,
        "model_version": getattr(nlp, "meta", {}).get("version", "?"),
    }

    # wordbank
    t0 = time.perf_counter()
    wordbank = load_pickle(WORDBANK_PKL)
    t1 = time.perf_counter()
    print(f"Loaded wordbank.pkl with {len(wordbank)} entries in {t1 - t0:.4f} seconds")

    # lemma data
    t0 = time.perf_counter()
    lemma_tuple = load_pickle(LEMMA_PKL)
    if not (isinstance(lemma_tuple, tuple) and len(lemma_tuple) == 2):
        raise ValueError("lemma_data.pkl must be a (lemma_forms, form_to_lemma) tuple")
    lemma_forms, form_to_lemma = lemma_tuple
    t1 = time.perf_counter()
    print(
        f"Loaded lemma_data.pkl with {len(lemma_forms)} lemmas "
        f"and {len(form_to_lemma)} forms in {t1 - t0:.4f} seconds"
    )

    # pronouns
    t0 = time.perf_counter()
    pronouns = load_pickle(PRONOUNS_PKL)
    t1 = time.perf_counter()
    print(f"Loaded pronouns.pkl with {len(pronouns['all_pronouns'])} pronouns in {t1 - t0:.4f} seconds")

    # connectives
    t0 = time.perf_counter()
    connectives = load_pickle(CONNECTIVES_PKL)
    t1 = time.perf_counter()
    print(f"Loaded connectives.pkl with {len(connectives['all_connectives'])} connectives in {t1 - t0:.4f} seconds")

    # pos categories
    t0 = time.perf_counter()
    pos_categories = load_pickle(POS_CATEGORIES_PKL)
    t1 = time.perf_counter()
    print(f"Loaded pos_categories.pkl with {len(pos_categories['content_words'])} content words in {t1 - t0:.4f} seconds")

    return nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta
