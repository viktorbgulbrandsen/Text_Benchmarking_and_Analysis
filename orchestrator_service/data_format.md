# Data Format for Orchestrator Service

## Input Format
```json
{
  "student_id": "101",
  "benchmark": {
    "benchmark_id": "bmk_101", 
    "benchmark_text": "Klimaforandringer representerer en av de største utfordringene i vår tid..."
  },
  "texts": [
    {
      "text_id": "essay_001",
      "text": "Klimaendringer er et stort problem som påvirker hele verden..."
    }
  ]
}
```

## Output Format
```json
{
  "status": "ok",
  "result": {
    "student_id": "101",
    "benchmark": {
      "benchmark_id": "bmk_101",
      "benchmark_text": "Klimaforandringer representerer...",
      "metrics": {...},
      "scores": {...}
    },
    "texts": [
      {
        "text_id": "essay_001", 
        "text": "Klimaendringer er et stort problem...",
        "metrics": {...},
        "scores": {...},
        "benchmark_metrics": {...}
      }
    ]
  }
}
```

## Flow
1. Input → metrics_service for all texts + benchmark
2. Input → benchmark_service for similarity comparison  
3. Merge results into combined output