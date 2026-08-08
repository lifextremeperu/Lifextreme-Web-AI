"""
agent_pyme_ingestor.py - Módulo de Ingesta Vectorial para el Asesor PYME
Este script lee todos los PDFs de la carpeta 'data/documentos/pymes', los divide en chunks,
los convierte a vectores usando Ollama (nomic-embed-text) y los inyecta en Qdrant.

Dependencias requeridas si no las tienes:
pip install PyMuPDF langchain langchain-text-splitters
"""
import os
import fitz  # PyMuPDF
import httpx
import asyncio
from pathlib import Path
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================
# CONFIGURACIÓN
# ==========================================
OLLAMA_URL = "http://localhost:11434"
QDRANT_URL = "http://localhost:6333"
KNOWLEDGE_VAULT = "Lifextreme_Knowledge"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIMENSION = 768

PDF_DIR = Path("data/documentos/pymes")

qclient = AsyncQdrantClient(url=QDRANT_URL)

async def initialize_qdrant():
    """Asegura que la colección existe con las dimensiones correctas."""
    try:
        exists = await qclient.collection_exists(KNOWLEDGE_VAULT)
        if not exists:
            await qclient.create_collection(
                collection_name=KNOWLEDGE_VAULT,
                vectors_config=VectorParams(size=EMBED_DIMENSION, distance=Distance.COSINE)
            )
            print(f"[+] Colección {KNOWLEDGE_VAULT} creada.")
    except Exception as e:
        print(f"[!] Error inicializando Qdrant: {e}")

async def get_embedding(text: str) -> list[float]:
    """Obtiene el embedding de Ollama."""
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/embeddings", 
                json={"model": EMBED_MODEL, "prompt": text}
            )
            return res.json().get("embedding", [])
    except Exception as e:
        print(f"[-] Error al vectorizar con Ollama: {e}")
        return []

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrae todo el texto de un PDF usando PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"[-] Error leyendo {pdf_path.name}: {e}")
    return text

async def ingest_document(pdf_path: Path, point_id_start: int):
    """Procesa un PDF y lo sube a Qdrant."""
    print(f"[*] Ingestando: {pdf_path.name}")
    raw_text = extract_text_from_pdf(pdf_path)
    if not raw_text.strip():
        print(f"   [!] Documento vacío o ilegible: {pdf_path.name}")
        return point_id_start

    # Dividir el documento en chunks lógicos (1000 caracteres con 200 de solapamiento)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    print(f"   [+] Generados {len(chunks)} fragmentos. Vectorizando...")

    points = []
    current_id = point_id_start
    
    # Procesar secuencialmente para no saturar a Ollama
    for chunk in chunks:
        vector = await get_embedding(chunk)
        if vector:
            points.append(PointStruct(
                id=current_id,
                vector=vector,
                payload={
                    "text_content": chunk,
                    "source": pdf_path.name,
                    "type": "pyme_manual"
                }
            ))
            current_id += 1
            
        if len(points) >= 50:
            # Subir por lotes
            await qclient.upsert(collection_name=KNOWLEDGE_VAULT, points=points)
            points = []

    if points:
        await qclient.upsert(collection_name=KNOWLEDGE_VAULT, points=points)
        
    print(f"   [+] {pdf_path.name} inyectado exitosamente en Qdrant.")
    return current_id

async def main():
    print("==================================================")
    print(" LIFEXTREME DATA INGESTOR - PYME ADVISOR")
    print("==================================================")
    
    await initialize_qdrant()
    
    if not PDF_DIR.exists():
        print(f"[-] La ruta {PDF_DIR} no existe. No hay PDFs para ingestar.")
        return
        
    pdfs = list(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"[-] No se encontraron archivos PDF en {PDF_DIR}.")
        return
        
    print(f"[*] Se encontraron {len(pdfs)} manuales. Iniciando ingesta masiva...")
    
    # Conseguir un ID base seguro leyendo la cantidad actual en Qdrant
    try:
        info = await qclient.get_collection(KNOWLEDGE_VAULT)
        current_id = info.points_count + 1000  # Offset seguro
    except:
        current_id = 1000
    
    for pdf in pdfs:
        current_id = await ingest_document(pdf, current_id)
        
    print("\n[+] ¡INGESTA FINALIZADA! El Agente PYME ahora es un experto técnico.")

if __name__ == "__main__":
    asyncio.run(main())
