from pydantic import BaseModel
from typing import List, Dict, Any

class BenchmarkIn(BaseModel):
    benchmark_id: str
    benchmark_text: str

class TextIn(BaseModel):
    text_id: str
    text: str

class BenchmarkRequestIn(BaseModel):
    student_id: str
    benchmark: BenchmarkIn
    texts: List[TextIn]

class ComparisonOut(BaseModel):
    text_id: str
    text: str
    benchmark_metrics: Dict[str, Any]

class ResultOut(BaseModel):
    student_id: str
    benchmark_id: str
    benchmark_text: str
    comparisons: List[ComparisonOut]
    message: str

class BenchmarkResultOut(BaseModel):
    status: str
    result: ResultOut