import math
import time
from collections import Counter


def tokenize(text: str):
    # splits on whitespace
    return text.strip().split()


def ngrams(tokens, n: int):
    # n-grams from tokens
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def get_bleu(candidate: str, reference: str, max_n: int = 4) -> dict:
    # bleu score
    start = time.time()

    cand_tokens = tokenize(candidate)
    ref_tokens = tokenize(reference)

    precisions = []
    for n in range(1, max_n + 1):
        cand_ngrams = Counter(ngrams(cand_tokens, n))
        ref_ngrams = Counter(ngrams(ref_tokens, n))

        # Overlap = min counts
        overlap = sum((cand_ngrams & ref_ngrams).values())
        total = max(sum(cand_ngrams.values()), 1)  # avoid division by zero
        p_n = overlap / total
        precisions.append(p_n)

    # Geometric mean of precisions
    if min(precisions) > 0:
        geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)
    else:
        geo_mean = 0.0

    # Brevity penalty
    c = len(cand_tokens)
    r = len(ref_tokens)
    if c > r:
        bp = 1.0
    else:
        bp = math.exp(1 - r / c) if c > 0 else 0.0

    bleu = bp * geo_mean
    elapsed = time.time() - start

    return {
        "BLEU": bleu,
        "precisions": precisions,
        "brevity_penalty": bp,
        "candidate_length": c,
        "reference_length": r,
        "elapsed_time_sec": elapsed,
    }