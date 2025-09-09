
from .openai_embedding import get_cosine_similarity

def return_features(student_text: str, benchmark_text: str):
    cosine_sim = get_cosine_similarity(student_text, benchmark_text)
    
    return {
        "openai_cosine_similarity": cosine_sim
    }