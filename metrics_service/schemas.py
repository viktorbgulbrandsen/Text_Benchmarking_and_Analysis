#File: text-analysis/schemas.py
# Part of: text-analysis project

from pydantic import BaseModel
from typing import List, Dict, Any


# --- Input schemas ---

class TextIn(BaseModel):
    text_id: str
    text: str


class StudentIn(BaseModel):
    student_id: str
    texts: List[TextIn]


class SubmissionIn(BaseModel):
    students: List[StudentIn]


# --- Output schemas ---

class TextOut(BaseModel):
    text_id: str
    text: str
    metrics: Dict[str, Any]
    scores: Dict[str, float]


class StudentOut(BaseModel):
    student_id: str
    texts: List[TextOut]


class MetricsResultOut(BaseModel):
    """
    Input: students (List[StudentOut]), message (str)  
    Output: BaseModel
    """
    students: List[StudentOut]
    message: str

class SubmissionOut(BaseModel):
    """
    Input: status (str), result (MetricsResultOut)
    Output: BaseModel  
    """
    status: str
    result: MetricsResultOut
