# app.py (strict payload acceptance + optional mock)

from fastapi import FastAPI, HTTPException
from schemas import SubmissionIn, SubmissionOut, MetricsResultOut, StudentOut, TextOut
from resources import init_resources
from analysis.orchestrate_text_metrics import return_text_metrics
import json
import time
from starlette.concurrency import run_in_threadpool

app = FastAPI()

# Initialize resources once at startup
nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta = init_resources()

def process_metrics_request(submission: SubmissionIn, resources=None) -> SubmissionOut:
    """
    Input: submission (SubmissionIn)
    Output: SubmissionOut
    """
    
    submission_dict = submission.dict()
    students_out = []
    
    for student in submission_dict["students"]:
        student_id = student["student_id"]
        texts_out = []
        
        for text_obj in student["texts"]:
            text_id = text_obj["text_id"]
            text_content = text_obj["text"]
            
            # get all metrics for this text using the orchestrate function
            text_metrics = return_text_metrics(text_content, resources)
            
            text_out = {
                "text_id": text_id,
                "text": text_content,
                "metrics": text_metrics["metrics"],
                "scores": text_metrics["scores"]
            }
            texts_out.append(text_out)
        
        student_out = {
            "student_id": student_id,
            "texts": [TextOut(**text) for text in texts_out]
        }
        students_out.append(StudentOut(**student_out))
    
    result = MetricsResultOut(
        students=students_out,
        message="Text metrics computed successfully"
    )
    
    return SubmissionOut(
        status="ok",
        result=result
    )

# main endpoint: accepts JSON payload
@app.post("/compute", response_model=SubmissionOut)
async def compute(submission: SubmissionIn):
    """
    Input: submission (SubmissionIn)
    Output: SubmissionOut
    """
    start_time = time.perf_counter()
    
    try:
        result = await run_in_threadpool(process_metrics_request, submission, (nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta))
        elapsed_time = time.perf_counter() - start_time
        print(f"Processed {len(submission.students)} students with {sum(len(s.texts) for s in submission.students)} texts in {elapsed_time:.4f} seconds")
        return result
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# optional: mock endpoint (reads from local file)
@app.post("/compute-mock", response_model=SubmissionOut)
async def compute_mock():
    """
    Input: None
    Output: SubmissionOut
    """
    try:
        with open("data/mock_data.json", "r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Mock data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in mock data file")
    
    try:
        submission = SubmissionIn(**payload)
        result = await run_in_threadpool(process_metrics_request, submission, (nlp, wordbank, lemma_forms, form_to_lemma, pronouns, connectives, pos_categories, meta))
        print(f"Processed mock data with {len(submission.students)} students")
        return result
    except Exception as e:
        print(f"Error processing mock request: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing mock data")

@app.get("/health")
async def health_check():
    """
    Input: None
    Output: dict
    """
    return {
        "status": "healthy",
        "service": "metrics_service"
    }

@app.get("/")
async def root():
    """
    Input: None  
    Output: dict
    """
    return {
        "service": "Metrics Service",
        "version": "1.0.0",
        "endpoints": {
            "POST /compute": "Compute text metrics",
            "POST /compute-mock": "Compute using mock data", 
            "GET /health": "Health check",
            "GET /": "Service info"
        }
    }
