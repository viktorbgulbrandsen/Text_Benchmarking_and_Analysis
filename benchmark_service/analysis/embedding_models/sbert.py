import time
import re
from sentence_transformers import SentenceTransformer, util


model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
_sbert_model = None


def get_sbert_model():
    """get model and reuse it."""
    global _sbert_model
    if _sbert_model is None:
        _sbert_model = SentenceTransformer(model_name)
    return _sbert_model


def simple_sent_split(text: str):
    """split sentences using regex."""
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]


def get_sbert_suite(benchmark: str, text: str) -> dict:
    # sbert similarity metrics
    start = time.time()
    sbert = get_sbert_model()

    # embedding on document
    emb_bench = sbert.encode(benchmark, convert_to_tensor=True)
    emb_student = sbert.encode(text, convert_to_tensor=True)
    cosine_doc = util.cos_sim(emb_bench, emb_student).item()

    # embedding on sents
    bench_sents = simple_sent_split(benchmark)
    stud_sents = simple_sent_split(text)

    bench_embs = sbert.encode(bench_sents, convert_to_tensor=True) if bench_sents else None
    stud_embs = sbert.encode(stud_sents, convert_to_tensor=True) if stud_sents else None

    # calculate coherence and simple if test 
    coherence = None
    if stud_embs is not None and len(stud_embs) > 1:
        coherence = float(util.cos_sim(stud_embs[:-1], stud_embs[1:]).mean())

    # calculate coverage and simple if test
    coverage = None
    if bench_embs is not None and stud_embs is not None:
        coverage = float(util.cos_sim(bench_embs, stud_embs).max(dim=1).values.mean())

    elapsed = time.time() - start

    return {
        "cosine_similarity_doc": cosine_doc,
        "coherence_student": coherence,
        "coverage_benchmark": coverage,
        "embedding_dim": emb_bench.shape[-1],
        "n_benchmark_sentences": len(bench_sents),
        "n_student_sentences": len(stud_sents),
        "elapsed_time_sec": elapsed,
    }
