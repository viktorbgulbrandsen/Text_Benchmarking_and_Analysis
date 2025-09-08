import time
from collections import Counter


def char_ngrams(text: str, n: int):
    # character n-grams
    text = text.replace(" ", "_")  # preserve word boundaries
    return [text[i:i+n] for i in range(len(text)-n+1)]


def chrf_score(candidate: str, reference: str, n_max: int = 6, beta: float = 2.0) -> float:
    # chrf score
    cand_ngrams = []
    ref_ngrams = []
    for n in range(1, n_max+1):
        cand_ngrams.extend(char_ngrams(candidate, n))
        ref_ngrams.extend(char_ngrams(reference, n))

    cand_counts = Counter(cand_ngrams)
    ref_counts = Counter(ref_ngrams)

    overlap = sum((cand_counts & ref_counts).values())
    total_cand = sum(cand_counts.values())
    total_ref = sum(ref_counts.values())

    # Precision and recall
    p = overlap / total_cand if total_cand > 0 else 0.0
    r = overlap / total_ref if total_ref > 0 else 0.0

    if p > 0 and r > 0:
        f_beta = (1 + beta**2) * p * r / (beta**2 * p + r)
    else:
        f_beta = 0.0

    return f_beta


def get_chrf(candidate: str, reference: str) -> dict:
    # character f-score
    start = time.time()
    score = chrf_score(candidate, reference)
    elapsed = time.time() - start
    return {"ChrF": score, "elapsed_time_sec": elapsed}
