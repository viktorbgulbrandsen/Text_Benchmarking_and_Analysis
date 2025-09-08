from pydantic import BaseModel
from typing import List, Dict, Any

class BenchmarkIn(BaseModel):
    benchmark_id: str
    benchmark_text: str

class TextIn(BaseModel):
    text_id: str
    text: str

class OrchestratorRequestIn(BaseModel):
    student_id: str
    benchmark: BenchmarkIn
    texts: List[TextIn]

class BenchmarkOut(BaseModel):
    benchmark_id: str
    benchmark_text: str
    metrics: Dict[str, Any]
    scores: Dict[str, float]

class TextOut(BaseModel):
    text_id: str
    text: str
    metrics: Dict[str, Any]
    scores: Dict[str, float]
    benchmark_metrics: Dict[str, Any]

class OrchestratorResult(BaseModel):
    student_id: str
    benchmark: BenchmarkOut
    texts: List[TextOut]

class OrchestratorResponse(BaseModel):
    status: str
    result: OrchestratorResult