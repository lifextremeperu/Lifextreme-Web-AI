import os
import fitz
import asyncio
import httpx
from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct
import uuid
from legal_chunker import chunk_legal_document

load_dotenv()

# Configuraciones
PDF_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"
REGION = "peru"
TIER = 0 # Nivel Experto / Estrategia Maestra

# Lista estricta de PDFs nuevos a procesar
NUEVOS_PDFS = [
    "7645565-pei-2026-2030-del-cenfotur.pdf",
    "7826147-programacion-marzo-2026-plan-para-el-fortalecimiento-de-competencias.pdf",
    "7574779-plan-operativo-institucional-poi-mincetur-2026.pdf",
    "Capacidad de carga Machupicchu.pdf",
    "resolucion-ministerial-ndeg-000075-2026-mc-anexo-plan-maestro-mcch.pdf",
    "Leyde parovechamiento RRNN -N°-26821.pdf",
    "Legislacion Forestal.pdf",
    "FEDETUR.pdf",
    "2092332-9.pdf",
    "2125062-3.pdf"
]

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

def extract_text_from_pdf(pdf_path: str) -> str:
    print(f"Extrayendo texto de: {os.path.basename(pdf_path)}")
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error leyendo {pdf_path}: {e}")
    return text

def process_pdf_sync(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"Advertencia: PDF vacío o escaneado -> {pdf_path}")
        return []
        
    meta = {"entidad_emisora": "Estado Peruano - Estrategia Maestra"}
    chunks = chunk_legal_document(text, meta)
    return chunks

async def process_pdf(pdf_path: str, http_client: httpx.AsyncClient, sem: asyncio.Semaphore):
    file_name = os.path.basename(pdf_path)
    chunks_dict = process_pdf_sync(pdf_path)
    
    if not chunks_dict:
        return

    # Inyectar el prefijo de contexto maestro a cada fragmento
    chunks = []
    for c in chunks_dict:
        prefix = "[Contexto Experto - Estrategia Maestra Nacional] "
        chunks.append(prefix + c["text"])
        
    print(f"PDF {file_name} dividido en {len(chunks)} fragmentos maestros.")

    points = []
    
    async def process_chunk(i, chunk):
        async with sem:
            vector = await get_embedding(chunk, http_client)
            if vector:
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "region": REGION,
                        "tier": TIER,
                        "modulo_nombre": "Estrategia Maestra Turismo - Nivel Experto",
                        "fuente": file_name,
                        "text_content": chunk
                    }
                )
                return point
            return None

    tasks = [process_chunk(i, chunk) for i, chunk in enumerate(chunks)]
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
                print(f"Error insertando en Qdrant: {e}")
        print(f"Insertados {len(points)} vectores estrategicos de {file_name} en Qdrant.")

async def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    pdf_files = [os.path.join(PDF_DIR, f) for f in NUEVOS_PDFS if os.path.exists(os.path.join(PDF_DIR, f))]
    
    if not pdf_files:
        print(f"No se encontraron los PDFs maestros en {PDF_DIR}")
        return

    print(f"Encontrados {len(pdf_files)} archivos PDF estrategicos para procesar.")

    sem = asyncio.Semaphore(1) # Reduced to 1 to avoid overwhelming Ollama

    async with httpx.AsyncClient() as http_client:
        for pdf in pdf_files:
            await process_pdf(pdf, http_client, sem)
            
    print("\n¡Proceso de ingesta de la Estrategia Maestra finalizado con exito!")

if __name__ == "__main__":
    asyncio.run(main())
