import time
from bert_score import score


def get_bertscore(candidate: str, reference: str) -> dict:
    """calculate BERT scoree"""
    start = time.time()
    
    P, R, F1 = score([candidate], [reference], lang='en', verbose=False)
    
    elapsed = time.time() - start
    
    return {
        "bertscore_precision": P.item(),
        "bertscore_recall": R.item(), 
        "bertscore_f1": F1.item(),
        "elapsed_time_sec": elapsed,
    }