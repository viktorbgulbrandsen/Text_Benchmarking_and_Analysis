from fastapi import FastAPI, HTTPException
from schemas import BenchmarkRequestIn, BenchmarkResultOut, ResultOut, ComparisonOut
from analysis.orchestrate_similarity_metrics import return_similarity_matrix
import json
import time
from starlette.concurrency import run_in_threadpool

app = FastAPI()


def process_benchmark_request(request: BenchmarkRequestIn) -> BenchmarkResultOut:
    """
    Input: request (BenchmarkRequestIn)
    Output: BenchmarkResultOut
    """
    request_dict = request.dict()
    
    student_id = request_dict["student_id"]
    benchmark_id = request_dict["benchmark"]["benchmark_id"]
    benchmark_text = request_dict["benchmark"]["benchmark_text"]
    texts = request_dict["texts"]
    
    comparisons = []
    
    for text_item in texts:
        text_id = text_item["text_id"]
        text_content = text_item["text"]
        
        benchmark_metrics = return_similarity_matrix(text_content, benchmark_text)
        
        comparison = {
            "text_id": text_id,
            "text": text_content,
            "benchmark_metrics": benchmark_metrics
        }
        comparisons.append(comparison)
    
    result = ResultOut(
        student_id=student_id,
        benchmark_id=benchmark_id,
        benchmark_text=benchmark_text,
        comparisons=[ComparisonOut(**comp) for comp in comparisons],
        message="Benchmark comparisons computed successfully"
    )
    
    return BenchmarkResultOut(
        status="ok",
        result=result
    )

@app.post("/compare", response_model=BenchmarkResultOut)
async def compare_texts(request: BenchmarkRequestIn):
    """
    Input: request (BenchmarkRequestIn)
    Output: BenchmarkResultOut
    """
    start_time = time.perf_counter()
    
    try:
        result = await run_in_threadpool(process_benchmark_request, request)
        elapsed_time = time.perf_counter() - start_time
        print(f"Processed {len(request.texts)} comparisons in {elapsed_time:.4f} seconds")
        return result
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/compare-mock", response_model=BenchmarkResultOut)
async def compare_mock():
    """
    Input: None
    Output: BenchmarkResultOut
    """
    try:
        with open("data/mock_eutanasi_data.json", "r", encoding="utf-8") as f:
            mock_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Mock data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in mock data file")
    
    try:
        request = BenchmarkRequestIn(**mock_data)
        result = await run_in_threadpool(process_benchmark_request, request)
        print(f"Processed mock data with {len(request.texts)} comparisons")
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
        "service": "benchmark_service"
    }

@app.get("/")
async def root():
    """
    Input: None  
    Output: dict
    """
    return {
        "service": "Benchmark Service",
        "version": "1.0.0",
        "endpoints": {
            "POST /compare": "Compare texts",
            "POST /compare-mock": "Compare using mock data", 
            "GET /health": "Health check",
            "GET /": "Service info"
        }
    }