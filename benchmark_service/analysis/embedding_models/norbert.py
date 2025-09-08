import time
import torch
from torch.nn.functional import cosine_similarity, pairwise_distance
from transformers import AutoTokenizer, AutoModel


# global model, runtime high
model_name = "ltg/norbert3-base"
_norbert_tokenizer = None
_norbert_model = None


def get_norbert_models():
    """load once and reuse."""
    global _norbert_tokenizer, _norbert_model
    if _norbert_tokenizer is None or _norbert_model is None:
        _norbert_tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        _norbert_model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    return _norbert_tokenizer, _norbert_model


def embed(text: str):
    """get  mean pooled NorBERT embedding."""
    tokenizer, model = get_norbert_models()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)


def get_norbert_suite(benchmark: str, text: str) -> dict:
    # norbert similarity metrics
    start = time.time()

    vec_b = embed(benchmark)
    vec_s = embed(text)

    cos_sim = cosine_similarity(vec_b, vec_s).item()
    euclidean = pairwise_distance(vec_b, vec_s, p=2).item()
    manhattan = pairwise_distance(vec_b, vec_s, p=1).item()

    elapsed = time.time() - start

    return {
        "cosine_similarity": cos_sim,
        "euclidean_distance": euclidean,
        "manhattan_distance": manhattan,
        "embedding_dim": vec_b.shape[-1],
        "elapsed_time_sec": elapsed,
    }