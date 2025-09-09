from fastapi import FastAPI, HTTPException
from schemas import BenchmarkRequestIn, BenchmarkResultOut, ResultOut, ComparisonOut
from analysis.orchestrate_features import return_features
import json
import time
from starlette.concurrency import run_in_threadpool

app = FastAPI()


def process_embedding_request(request: BenchmarkRequestIn) -> BenchmarkResultOut:
    request_dict = request.dict()
    
    student_id = request_dict["student_id"]
    benchmark_id = request_dict["benchmark"]["benchmark_id"]
    benchmark_text = request_dict["benchmark"]["benchmark_text"]
    texts = request_dict["texts"]
    
    comparisons = []
    
    for text_item in texts:
        text_id = text_item["text_id"]
        text_content = text_item["text"]
        
        benchmark_metrics = return_features(text_content, benchmark_text)
        
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
        message="Embedding comparisons computed successfully"
    )
    
    return BenchmarkResultOut(
        status="ok",
        result=result
    )

@app.post("/embed", response_model=BenchmarkResultOut)
async def embed_texts(request: BenchmarkRequestIn):
    start_time = time.perf_counter()
    
    try:
        result = await run_in_threadpool(process_embedding_request, request)
        elapsed_time = time.perf_counter() - start_time
        print(f"Processed {len(request.texts)} embeddings in {elapsed_time:.4f} seconds")
        return result
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/embed-mock", response_model=BenchmarkResultOut)
async def embed_mock():
    try:
        with open("data/mock_data.json", "r", encoding="utf-8") as f:
            mock_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Mock data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in mock data file")
    
    try:
        request = BenchmarkRequestIn(**mock_data)
        result = await run_in_threadpool(process_embedding_request, request)
        print(f"Processed mock data with {len(request.texts)} embeddings")
        return result
    except Exception as e:
        print(f"Error processing mock request: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing mock data")