I have thrown in a bunch of methods to demonstrate.

BLEU is used to assess machine-translated language to another. Maybe not relevant, unless one wants to look at plagirsm. 
https://en.wikipedia.org/wiki/BLEU#

ChrF has a nltk module:  https://www.nltk.org/_modules/nltk/translate/chrf_score.html, I've tried to recreate, but must look closer at algorthim if it is to be used. 

ROUGE is a similar model for comparing natural language  : https://en.wikipedia.org/wiki/ROUGE_(metric). Tentative simplified algorithm. 


BERTScore: semantic similarity with transformers. Slower, may need batching or GPU.

Cross-encoders: accurate, but expensive. Usually not practical without strong hardware.

SBERT / NorBERT: sentence embeddings. Can be precomputed and stored in a vector DB. Might need larger infrastructure if used at scale. But  valuable if semantic similarity is required across many texts

LDA. Latent Dirichlet Allocation. https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation . Cheap to run, decent for coarse topical similarity, but limited compared to embeddings for semantic detail
