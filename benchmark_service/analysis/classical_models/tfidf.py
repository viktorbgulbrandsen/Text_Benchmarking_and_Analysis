import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_tfidf_cosine(benchmark: str, student: str) -> dict:
    # tfidf cosine similarity
    start = time.time()

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([benchmark, student])  # 2 x |V| matrix

    # Compute cosine similarity between the two rows
    sim = cosine_similarity(tfidf[0], tfidf[1])[0, 0]

    elapsed = time.time() - start
    return {
        "tfidf_cosine_similarity": float(sim),
        "vocab_size": len(vectorizer.get_feature_names_out()),
        "elapsed_time_sec": elapsed,
    }

