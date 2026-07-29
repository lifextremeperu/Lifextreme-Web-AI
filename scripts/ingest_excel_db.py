import os
import glob
import pandas as pd
import asyncio
import httpx
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct
import uuid

load_dotenv()

EXCEL_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\institucional_descargas"
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

def process_row_to_text(row, filename):
    """Convierte una fila de Excel en una oración semántica descriptiva"""
    cols = row.index
    text_parts = [f"Base de datos MINCETUR ({filename}):"]
    for col in cols:
        val = str(row[col]).strip()
        if val and val.lower() != 'nan' and val.lower() != 'nat':
            text_parts.append(f"{col}: {val}")
    return " | ".join(text_parts)

async def process_excel(excel_path: str, http_client: httpx.AsyncClient, sem: asyncio.Semaphore):
    file_name = os.path.basename(excel_path)
    print(f"Procesando Excel: {file_name}")
    
    try:
        df = pd.read_excel(excel_path, engine='calamine')
    except Exception as e:
        print(f"Error leyendo el Excel {file_name}: {e}")
        return
        
    print(f"Encontrados {len(df)} registros en {file_name}.")
    
    # Tomar las filas como diccionarios
    records = df.to_dict('records')
    points = []
    
    async def process_chunk(record):
        # Convertimos a Pandas Series momentáneamente para usar nuestra función
        row_series = pd.Series(record)
        chunk = process_row_to_text(row_series, file_name)
        
        async with sem:
            vector = await get_embedding(chunk, http_client)
            if vector:
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "region": REGION,
                        "tier": TIER,
                        "modulo_nombre": f"Base MINCETUR - {file_name}",
                        "text_content": chunk
                    }
                )
                return point
            return None

    tasks = [process_chunk(rec) for rec in records]
    
    # Procesar en lotes grandes (gather)
    print(f"Generando embeddings para {len(tasks)} registros...")
    results = await asyncio.gather(*tasks)
    points = [p for p in results if p is not None]

    if points:
        batch_size = 50
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            try:
                await qdrant_client.upsert(
                    collection_name=COLLECTION,
                    points=batch
                )
            except Exception as e:
                print(f"Error insertando lote en Qdrant: {e}")
        print(f"Insertados {len(points)} vectores de {file_name} en Qdrant.")

async def main():
    excel_files = glob.glob(os.path.join(EXCEL_DIR, "*.xlsx"))
    if not excel_files:
        print(f"No se encontraron archivos Excel en {EXCEL_DIR}")
        return

    print(f"Encontrados {len(excel_files)} archivos Excel institucionales para procesar.")

    # Semáforo para controlar carga en Ollama
    sem = asyncio.Semaphore(5)

    async with httpx.AsyncClient() as http_client:
        for excel_file in excel_files:
            await process_excel(excel_file, http_client, sem)
            
    print("\n¡Proceso de ingesta de Bases de Datos Excel finalizado con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
