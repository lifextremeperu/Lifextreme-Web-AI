import os
import glob
import fitz  # PyMuPDF
import asyncio
import httpx
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct
import uuid

load_dotenv()

# Configuraciones
PDF_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\CICLOVIA DEL MAIZ"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"
REGION = "cusco"
TIER = 2

# Clientes
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

async def process_pdf(pdf_path: str, splitter: RecursiveCharacterTextSplitter, http_client: httpx.AsyncClient, sem: asyncio.Semaphore):
    file_name = os.path.basename(pdf_path)
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"Advertencia: PDF vacío o no se pudo extraer texto -> {file_name}")
        return

    chunks = splitter.split_text(text)
    print(f"PDF {file_name} dividido en {len(chunks)} fragmentos.")

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
                        "modulo_nombre": f"Ciclovía del Maíz - {file_name}",
                        "text_content": chunk
                    }
                )
                return point
            return None

    tasks = [process_chunk(i, chunk) for i, chunk in enumerate(chunks)]
    results = await asyncio.gather(*tasks)
    points = [p for p in results if p is not None]

    # Batch insert into Qdrant
    if points:
        batch_size = 50
        for i in range(0, len(points), batch_size):
            batch = points[i:i+batch_size]
            try:
                await qdrant_client.upsert(
                    collection_name=COLLECTION,
                    points=batch
                )
                print(f"Insertados {len(batch)} vectores de {file_name} en Qdrant.")
            except Exception as e:
                print(f"Error insertando en Qdrant: {e}")

async def main():
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    if not pdf_files:
        print(f"No se encontraron archivos PDF en {PDF_DIR}")
        return

    print(f"Encontrados {len(pdf_files)} archivos PDF para procesar.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    sem = asyncio.Semaphore(5)  # Limitar concurrencia a Ollama

    async with httpx.AsyncClient() as http_client:
        for pdf in pdf_files:
            await process_pdf(pdf, splitter, http_client, sem)
            
    print("\n¡Proceso de ingesta finalizado con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
