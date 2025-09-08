


APIS
http://localhost:8001/compute
http://localhost:8002/compare  
http://localhost:8003/orchestrate


also 
http://localhost:8002/compare-mock
http://localhost:8001/compute-mock

rebuild (for my powershell)
docker-compose down; docker-compose build --no-cache; docker-compose up


Sample JSON for localhost:8003/orchestrate:
{
  "student_id": "101",
  "benchmark": {
    "benchmark_id": "bmk_101", 
    "benchmark_text": "Klimaforandringer representerer en av de største utfordringene i vår tid og påvirker økosystemer globalt. Smeltende is ved polene fører til stigende havnivå, som truer kystområder."
  },
  "texts": [
    {
      "text_id": "essay_001",
      "text": "Klimaendringer er et stort problem som påvirker hele verden. Isen på Nordpolen og Antarktis smelter mye raskere enn før, og dette fører til at havnivået stiger."
    }
  ]
}
Or you can send sample_exphilessays.json

You can use mock_eutanasi_data.json to test out 8002/compare