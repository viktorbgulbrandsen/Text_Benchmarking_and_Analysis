from fastapi import FastAPI, HTTPException
from schemas import OrchestratorRequestIn, OrchestratorResponse, OrchestratorResult, BenchmarkOut, TextOut
import httpx
import asyncio
import json

app = FastAPI()

async def call_metrics_service(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://metrics_service:8001/compute", json=data)
        response.raise_for_status()
        return response.json()

async def call_benchmark_service(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://benchmark_service:8002/compare", json=data)
        response.raise_for_status()
        return response.json()

@app.post("/orchestrate", response_model=OrchestratorResponse)
async def orchestrate(request: OrchestratorRequestIn):
    try:
        # Prepare metrics service input (include benchmark text as a "student")
        metrics_input = {
            "students": [
                {
                    "student_id": "benchmark",
                    "texts": [{"text_id": request.benchmark.benchmark_id, "text": request.benchmark.benchmark_text}]
                },
                {
                    "student_id": request.student_id,
                    "texts": [{"text_id": t.text_id, "text": t.text} for t in request.texts]
                }
            ]
        }
        
        # Prepare benchmark service input  
        benchmark_input = {
            "student_id": request.student_id,
            "benchmark": {
                "benchmark_id": request.benchmark.benchmark_id,
                "benchmark_text": request.benchmark.benchmark_text
            },
            "texts": [{"text_id": t.text_id, "text": t.text} for t in request.texts]
        }

        # Call both services
        metrics_result, benchmark_result = await asyncio.gather(
            call_metrics_service(metrics_input),
            call_benchmark_service(benchmark_input)
        )

        # Find benchmark metrics
        benchmark_metrics = None
        benchmark_scores = None
        for student in metrics_result["result"]["students"]:
            if student["student_id"] == "benchmark":
                benchmark_metrics = student["texts"][0]["metrics"]
                benchmark_scores = student["texts"][0]["scores"]
                break

        # Merge results
        texts_out = []
        student_texts_metrics = None
        for student in metrics_result["result"]["students"]:
            if student["student_id"] == request.student_id:
                student_texts_metrics = {t["text_id"]: t for t in student["texts"]}
                break

        for comparison in benchmark_result["result"]["comparisons"]:
            text_id = comparison["text_id"]
            text_metrics = student_texts_metrics[text_id]
            
            text_out = TextOut(
                text_id=text_id,
                text=comparison["text"],
                metrics=text_metrics["metrics"],
                scores=text_metrics["scores"],
                benchmark_metrics=comparison["benchmark_metrics"]
            )
            texts_out.append(text_out)

        # Create final result
        result = OrchestratorResult(
            student_id=request.student_id,
            benchmark=BenchmarkOut(
                benchmark_id=request.benchmark.benchmark_id,
                benchmark_text=request.benchmark.benchmark_text,
                metrics=benchmark_metrics,
                scores=benchmark_scores
            ),
            texts=texts_out
        )

        return OrchestratorResponse(status="ok", result=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "orchestrator_service"}

@app.get("/orchestrate-mock")
async def orchestrate_mock():
    with open("sample_exphilessays.json") as f:
        data = json.load(f)
    
    request = OrchestratorRequestIn(
        student_id=data["student_id"],
        benchmark=data["benchmark"], 
        texts=data["texts"]
    )
    
    return await orchestrate(request)

@app.get("/")
async def root():
    return {"service": "Orchestrator Service", "version": "1.0.0"}
