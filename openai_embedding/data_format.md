INPUT
{
  "student_id": "101",
  "benchmark": {
    "benchmark_id": "bmk_101",
    "benchmark_text": "This is the benchmark written by student 101."
  },
  "texts": [
    {
      "text_id": "essay_001",
      "text": "Some later writing by the same student."
    }
  ]
}

OUTPUT
{
  "status": "ok",
  "result": {
    "student_id": "101",
    "benchmark_id": "bmk_101",
    "benchmark_text": "This is the benchmark written by student 101.",
    "comparisons": [
      {
        "text_id": "essay_001",
        "text": "Some later writing by the same student.",
        "benchmark_metrics": {
          "embedding_similarity": 0.82,
          "lexical_overlap": 0.41,
          "syntax_divergence": 0.17
        }
      }
    ],
    "message": "Benchmark comparisons computed successfully"
  }
}