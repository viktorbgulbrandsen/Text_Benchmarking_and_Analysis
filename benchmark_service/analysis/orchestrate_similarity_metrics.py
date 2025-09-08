
# Classical models
from .classical_models.BLEU import get_bleu
from .classical_models.ROUGE import get_rouge
from .classical_models.ChrF import get_chrf
from .classical_models.tfidf import get_tfidf_cosine

# Embedding models  

""" These take insane load time and are slow in executing for me
from .embedding_models.sbert import get_sbert_suite
from .embedding_models.cross_encoder import get_crossencoder_score
from .embedding_models.norbert import get_norbert_suite
from .embedding_models.bertscore import get_bertscore
"""

# Topic models
from .topic_models.LDA import get_lda_suite


def return_similarity_matrix(student_text: str, benchmark_text: str) -> dict:
    # similarity metrics suite
    
    
    # Classical models (fast)
    bleu_results = get_bleu(student_text, benchmark_text)
    rouge_results = get_rouge(student_text, benchmark_text) 
    chrf_results = get_chrf(student_text, benchmark_text)
    tfidf_results = get_tfidf_cosine(benchmark_text, student_text)
    
    # Embedding models (very slow, dont use )
    """
    sbert_results = get_sbert_suite(benchmark_text, student_text)
    crossencoder_results = get_crossencoder_score(benchmark_text, student_text)
    norbert_results = get_norbert_suite(benchmark_text, student_text)
    bertscore_results = get_bertscore(student_text, benchmark_text)
    """

    # Topic models (medium speed)
    lda_results = get_lda_suite(benchmark_text, student_text)
    
    return {
        # Classical models
        "bleu": bleu_results,
        "rouge": rouge_results,
        "chrf": chrf_results,
        "tfidf": tfidf_results,
        
        # Embedding models
        # "sbert": sbert_results,
        # "crossencoder": crossencoder_results,
        # "norbert": norbert_results,
        # "bertscore": bertscore_results,
        
        # Topic models
        "lda": lda_results,
    }