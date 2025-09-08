import time
from sentence_transformers import CrossEncoder


# Global model - will be loaded once when module is imported
model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_cross_encoder_model = None


def get_crossencoder_model():
    """reuse cross encoder model."""
    global _cross_encoder_model
    if _cross_encoder_model is None:
        _cross_encoder_model = CrossEncoder(model_name)
    return _cross_encoder_model


def get_crossencoder_score(benchmark: str, text: str) -> dict:
    """calculate cross encoder score benchmark and text."""
    start = time.time()
    cross_encoder = get_crossencoder_model()

    # Model expects list of pairs
    score = cross_encoder.predict([(benchmark, text)]).item()

    elapsed = time.time() - start

    return {
        "crossencoder_score": score,
        "elapsed_time_sec": elapsed,
    }
