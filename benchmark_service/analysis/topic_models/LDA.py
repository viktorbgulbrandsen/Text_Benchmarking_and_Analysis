import time
from gensim import corpora, models
from gensim.matutils import sparse2full
from scipy.spatial.distance import cosine
from scipy.stats import entropy


def preprocess(text: str):
    # basic tokenizer
    return [w.lower() for w in text.split() if w.isalpha()]


def get_topic_distribution(lda_model, bow, num_topics: int):
    # bow to topic distribution
    dist_sparse = lda_model.get_document_topics(bow, minimum_probability=0)
    return sparse2full(dist_sparse, num_topics)


def get_lda_suite(benchmark: str, student: str, num_topics: int = 5) -> dict:
    # lda topic similarity
    start = time.time()

    # Preprocess texts
    texts = [preprocess(benchmark), preprocess(student)]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(t) for t in texts]

    # Train LDA (toy example: only benchmark + student doc)
    lda = models.LdaModel(
        corpus, num_topics=num_topics, id2word=dictionary, passes=10, random_state=42
    )

    # Topic distributions
    bench_dist = get_topic_distribution(lda, corpus[0], num_topics)
    stud_dist = get_topic_distribution(lda, corpus[1], num_topics)

    # Compare distributions
    cos_sim = 1 - cosine(bench_dist, stud_dist)
    kl_div = float(entropy(bench_dist + 1e-12, stud_dist + 1e-12))  # epsilon for stability

    elapsed = time.time() - start

    return {
        "num_topics": num_topics,
        "topic_dist_benchmark": bench_dist.tolist(),
        "topic_dist_student": stud_dist.tolist(),
        "cosine_similarity": float(cos_sim),
        "kl_divergence": kl_div,
        "elapsed_time_sec": elapsed,
    }
