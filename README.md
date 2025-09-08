
### Metrics Service
Runs text metric computations. The metrics are decently accurate, the scores are composite and need more thorough stastical analysis 
- **`http://localhost:8001/compute`**
- **`http://localhost:8001/compute-mock`** (mock data)

### Benchmark Service
Compares student texts with benchmark texts.
- **`http://localhost:8002/compare`**
- **`http://localhost:8002/compare-mock`** (mock data)

### Orchestrator Service
Calls both services.
- **`http://localhost:8003/orchestrate`**
- **`http://localhost:8003/orchestrate-mock`** (mockdata)

---
They have auto-generated documentation via Python FastAPI

- Metrics Service → [http://localhost:8001/docs](http://localhost:8001/docs)  
- Benchmark Service → [http://localhost:8002/docs](http://localhost:8002/docs)  
- Orchestrator Service → [http://localhost:8003/docs](http://localhost:8003/docs)  


## Structure:


From the project root (PowerShell):
- Both metrics_service and benchmark_service run as individual dockers (structure to be changed later to make more efficient and less orchestrator)
- Both have method post. 
- Both have data_format.md to see dataformat, the api mock calls serve to show nicely. 
- Most functionality is under the the analysis folders inside the individual service folders.

## Running with Docker
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up
