import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def create_embedding(text: str) -> list:
    response = client.embeddings.create(
        model=deployment,
        input=text
    )
    return response.data[0].embedding

def get_cosine_similarity(student_text: str, benchmark_text: str) -> float:
    student_embedding = create_embedding(student_text)
    benchmark_embedding = create_embedding(benchmark_text)
    
    similarity = cosine_similarity([student_embedding], [benchmark_embedding])[0][0]
    return float(similarity)

"""
def main():
    test_student = "Klimaforandringer representerer en av de største utfordringene i vår tid og påvirker økosystemer globalt. Smeltende is ved polene fører til stigende havnivå, som truer kystområder."
    test_benchmark = "Klimaendringer er et stort problem som påvirker hele verden. Isen på Nordpolen og Antarktis smelter mye raskere enn før, og dette fører til at havnivået stiger."


    similarity = get_cosine_similarity(test_student, test_benchmark)
    print(f"Cosine similarity: {similarity}")

if __name__ == "__main__":
    main()
"""