# Data Format Documentation

This Python script processes student text data and returns analysis metrics.

## Input Format
```json
{
  "students": [
    {
      "student_id": "101",
      "texts": [
        {
          "text_id": "essay_001",
          "text": "The student's essay text..."
        },
        {
          "text_id": "essay_002", 
          "text": "Another essay from the same student..."
        }
      ]
    },
    {
      "student_id": "102",
      "texts": [
        {
          "text_id": "essay_003",
          "text": "Single essay from another student..."
        }
      ]
    }
  ]
}
```

## Output Format
```json
{
  "status": "ok",
  "result": {
    "fetched_data": {
      "students": [
        {
          "student_id": "101",
          "texts": [
            {
              "text_id": "essay_001",
              "text": "The student's essay text...",
              "metrics": {
                "word_count": 25,
                "sentence_count": 3,
                "avg_word_length": 4.2
              }
            }
          ]
        }
      ]
    },
    "message": "Data processed successfully"
  }
}
```


