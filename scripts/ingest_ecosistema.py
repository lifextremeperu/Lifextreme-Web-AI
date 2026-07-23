import os
import asyncio
import httpx
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct
import uuid

load_dotenv()

QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"
REGION = "peru"
TIER = 1

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
        print(f"Error obteniendo embedding: {e}")
        return None

async def main():
    file_path = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\directorio_ingesta_turismo.md"
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split roughly by sections for better context mapping
    chunks = text.split("\n## ")
    # Re-add the "##" that was split out for chunks after the first one
    chunks = [chunks[0]] + ["## " + chunk for chunk in chunks[1:]]
    
    print(f"Documento dividido en {len(chunks)} secciones lógicas.")

    points = []
    async with httpx.AsyncClient() as http_client:
        for chunk in chunks:
            if not chunk.strip():
                continue
            
            vector = await get_embedding(chunk, http_client)
            if vector:
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "region": REGION,
                        "tier": TIER,
                        "modulo_nombre": "Ecosistema Institucional de Turismo",
                        "text_content": chunk.strip()
                    }
                )
                points.append(point)
    
    if points:
        await qdrant_client.upsert(
            collection_name=COLLECTION,
            points=points
        )
        print(f"¡Éxito! {len(points)} fragmentos del Ecosistema Institucional insertados en Qdrant.")

if __name__ == "__main__":
    asyncio.run(main())
