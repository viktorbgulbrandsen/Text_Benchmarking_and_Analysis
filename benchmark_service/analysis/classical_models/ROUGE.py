import time
from collections import Counter


def tokenize(text: str):
    # splits on whitespace
    return text.strip().split()


def ngrams(tokens, n: int):
    # n-grams from tokens
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


def rouge_n(candidate: str, reference: str, n: int = 1) -> float:
    cand_tokens = tokenize(candidate)
    ref_tokens = tokenize(reference)

    cand_ngrams = Counter(ngrams(cand_tokens, n))
    ref_ngrams = Counter(ngrams(ref_tokens, n))

    overlap = sum((cand_ngrams & ref_ngrams).values())
    total_ref = max(sum(ref_ngrams.values()), 1)

    return overlap / total_ref


def lcs_length(x, y):
    # lcs with dp
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if x[i] == y[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]


def rouge_l(candidate: str, reference: str) -> dict:
    cand_tokens = tokenize(candidate)
    ref_tokens = tokenize(reference)

    lcs = lcs_length(cand_tokens, ref_tokens)
    r_lcs = lcs / len(ref_tokens) if ref_tokens else 0.0
    p_lcs = lcs / len(cand_tokens) if cand_tokens else 0.0

    beta = 1.2  # recall-focused
    if r_lcs > 0 and p_lcs > 0:
        f_lcs = ((1 + beta**2) * r_lcs * p_lcs) / (r_lcs + beta**2 * p_lcs)
    else:
        f_lcs = 0.0

    return {"recall": r_lcs, "precision": p_lcs, "f1": f_lcs}


def get_rouge(candidate: str, reference: str) -> dict:
    # rouge scores
    start = time.time()

    r1 = rouge_n(candidate, reference, n=1)
    r2 = rouge_n(candidate, reference, n=2)
    rl = rouge_l(candidate, reference)

    elapsed = time.time() - start
    return {
        "ROUGE-1": r1,
        "ROUGE-2": r2,
        "ROUGE-L": rl,
        "elapsed_time_sec": elapsed,
    }
