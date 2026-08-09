"""
agent_pyme_ingestor.py - Módulo de Ingesta Vectorial Semántica para el Asesor PYME
Este script lee el corpus_manifest.json, extrae el texto de los PDFs listados, 
realiza chunking semántico basado en jerarquías legales (Artículos, Capítulos),
convierte a vectores con Ollama (nomic-embed-text) y los inyecta en Qdrant.
"""
import os
import re
import json
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
MANIFEST_PATH = PDF_DIR / "corpus_manifest.json"

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
                json={"model": EMBED_MODEL, "prompt": text},
                timeout=120.0
            )
            return res.json().get("embedding", [])
    except Exception as e:
        print(f"[-] Error al vectorizar con Ollama: {e}")
        return []

def clean_extracted_text(text: str) -> str:
    """Limpia el texto base eliminando marcas de agua, índices y ruido excesivo."""
    # Remover múltiples saltos de línea y espacios
    text = re.sub(r'\n+', '\n', text)
    # Tratar de unir párrafos que fueron cortados por el PDF (saltos de línea en medio de la oración)
    text = re.sub(r'(?<!\.)\n(?=[a-z])', ' ', text)
    return text

def semantic_chunking(text: str) -> list[str]:
    """Divide el texto respetando Artículos y Capítulos legales."""
    # Dividir por "Artículo", "CAPÍTULO", "TÍTULO"
    # Usamos regex para encontrar los delimitadores. El lookahead mantiene el delimitador.
    pattern = r"(?=\nArtículo\s+\d+|\nCAPÍTULO\s+|\nTÍTULO\s+)"
    raw_chunks = re.split(pattern, text, flags=re.IGNORECASE)
    
    chunks = []
    # Usamos RecursiveCharacterTextSplitter como fallback si un artículo es demasiado largo
    fallback_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    
    for c in raw_chunks:
        c = c.strip()
        if not c:
            continue
        if len(c) > 2000:
            sub_chunks = fallback_splitter.split_text(c)
            chunks.extend(sub_chunks)
        else:
            chunks.append(c)
    return chunks

def extract_text_from_file(file_path: Path) -> str:
    """Extrae texto de un archivo PDF, MD o TXT."""
    text = ""
    try:
        if file_path.suffix.lower() == '.pdf':
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
        elif file_path.suffix.lower() in ['.md', '.txt']:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"[-] Error leyendo {file_path.name}: {e}")
    return text

async def ingest_document(file_path: Path, metadata: dict, point_id_start: int):
    """Procesa un documento con chunking semántico y lo sube a Qdrant."""
    print(f"[*] Ingestando: {file_path.name} ({metadata.get('entidad', 'General')})")
    raw_text = extract_text_from_file(file_path)
    if not raw_text.strip():
        print(f"   [!] Documento vacío o ilegible: {file_path.name}")
        return point_id_start

    clean_text = clean_extracted_text(raw_text)
    chunks = semantic_chunking(clean_text)
    print(f"   [+] Generados {len(chunks)} fragmentos semánticos. Vectorizando...")

    points = []
    current_id = point_id_start
    
    # Procesar secuencialmente
    for chunk in chunks:
        vector = await get_embedding(chunk)
        if vector:
            payload = {
                "text_content": chunk,
                "source": file_path.name,
                "entidad": metadata.get("entidad", ""),
                "dominio": metadata.get("dominio", ""),
                "vigencia": metadata.get("vigencia", ""),
                "tipo_documento": metadata.get("tipo_documento", "documento")
            }
            points.append(PointStruct(
                id=current_id,
                vector=vector,
                payload=payload
            ))
            current_id += 1
            
        if len(points) >= 50:
            await qclient.upsert(collection_name=KNOWLEDGE_VAULT, points=points)
            points = []

    if points:
        await qclient.upsert(collection_name=KNOWLEDGE_VAULT, points=points)
        
    print(f"   [+] {file_path.name} inyectado exitosamente en Qdrant.")
    return current_id

async def main():
    print("==================================================")
    print(" LIFEXTREME DATA INGESTOR - PYME ADVISOR (SEMANTIC)")
    print("==================================================")
    
    await initialize_qdrant()
    
    if not MANIFEST_PATH.exists():
        print(f"[-] No se encontró el manifiesto: {MANIFEST_PATH}")
        return
        
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    print(f"[*] Se encontraron {len(manifest)} documentos en el manifiesto. Iniciando ingesta...")
    
    try:
        info = await qclient.get_collection(KNOWLEDGE_VAULT)
        current_id = info.points_count + 1000  # Offset seguro
    except:
        current_id = 1000
    
    for item in manifest:
        file_path = PDF_DIR / item["filename"]
        if file_path.exists():
            current_id = await ingest_document(file_path, item, current_id)
        else:
            print(f"[-] Archivo no encontrado: {file_path}")
            
    print("\n[+] ¡INGESTA FINALIZADA! El Agente PYME ahora tiene estructura semántica.")

if __name__ == "__main__":
    asyncio.run(main())
