Simple code which uses openai embed and scikit-learn compute cosine similarity. 

Test run: 
{
    "status": "ok",
    "result": {
        "student_id": "101",
        "benchmark_id": "bmk_101",
        "benchmark_text": "Klimaforandringer representerer en av de største utfordringene i vår tid og påvirker økosystemer globalt. Smeltende is ved polene fører til stigende havnivå, som truer kystområder. ",
        "comparisons": [
            {
                "text_id": "essay_001",
                "text": "Klimaendringer er et stort problem som påvirker hele verden. Isen på Nordpolen og Antarktis smelter mye raskere enn før, og dette fører til at havnivået stiger. ",
                "benchmark_metrics": {
                    "openai_cosine_similarity": 0.8122691106467537
                }
            }
        ],
        "message": "Embedding comparisons computed successfully"
    }
}
