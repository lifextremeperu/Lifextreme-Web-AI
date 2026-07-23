import os
import asyncio
import httpx
from qdrant_client import AsyncQdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"

qdrant_client = AsyncQdrantClient(url=QDRANT_URL)

async def get_embedding(text: str, client: httpx.AsyncClient) -> list[float]:
    try:
        response = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=120.0
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error obteniendo embedding para '{text}': {e}")
        return None

async def query_knowledge(query: str, client: httpx.AsyncClient, limit: int = 5):
    vector = await get_embedding(query, client)
    if not vector:
        return []
    
    search_result = await qdrant_client.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=limit
    )
    
    return [hit.payload['text_content'] for hit in search_result]

async def main():
    queries = [
        "Ciclovia del Maiz datos tecnicos ubicacion longitud Valle Sagrado",
        "Ciclovia del Maiz presupuesto comunidades campesinas",
        "Invierte.pe turismo MEF formulacion proyecto",
        "Capacidad de carga efectiva turismo riesgos"
    ]
    
    async with httpx.AsyncClient() as client:
        with open("data/contexto_extraido_ciclovia.txt", "w", encoding="utf-8") as f:
            for q in queries:
                print(f"Consultando: {q}")
                results = await query_knowledge(q, client, limit=5)
                f.write(f"\n\n--- Resultados para: {q} ---\n")
                for r in results:
                    f.write(f"- {r}\n")
    print("Contexto extraído y guardado en data/contexto_extraido_ciclovia.txt")

if __name__ == "__main__":
    asyncio.run(main())
