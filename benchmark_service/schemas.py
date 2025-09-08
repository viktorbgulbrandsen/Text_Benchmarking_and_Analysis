from pydantic import BaseModel
from typing import List, Dict, Any

class BenchmarkIn(BaseModel):
    """
    Input: benchmark_id (str), benchmark_text (str)
    Output: BaseModel
    """
    benchmark_id: str
    benchmark_text: str

class TextIn(BaseModel):
    """
    Input: text_id (str), text (str)
    Output: BaseModel
    """
    text_id: str
    text: str

class BenchmarkRequestIn(BaseModel):
    """
    Input: student_id (str), benchmark (BenchmarkIn), texts (List[TextIn])
    Output: BaseModel
    """
    student_id: str
    benchmark: BenchmarkIn
    texts: List[TextIn]

class ComparisonOut(BaseModel):
    """
    Input: text_id (str), text (str), benchmark_metrics (dict)
    Output: BaseModel
    """
    text_id: str
    text: str
    benchmark_metrics: Dict[str, Any]

class ResultOut(BaseModel):
    """
    Input: student_id (str), benchmark_id (str), benchmark_text (str), comparisons (List), message (str)
    Output: BaseModel
    """
    student_id: str
    benchmark_id: str
    benchmark_text: str
    comparisons: List[ComparisonOut]
    message: str

class BenchmarkResultOut(BaseModel):
    """
    Input: status (str), result (ResultOut)
    Output: BaseModel
    """
    status: str
    result: ResultOut