import os
import sys
import uuid
import time
import hashlib
from pathlib import Path
import httpx

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from langchain_text_splitters import MarkdownHeaderTextSplitter

sys.stdout.reconfigure(encoding='utf-8')

# Variables Globales
QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
OLLAMA_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"
BATCH_SIZE = 50

# Configuración del Splitter de Markdown
headers_to_split_on = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3"),
    ("####", "H4"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

def init_qdrant():
    qclient = QdrantClient(url=QDRANT_URL)
    if not qclient.collection_exists(collection_name=COLLECTION):
        print(f"[*] Creando colección {COLLECTION} en Qdrant...")
        qclient.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    return qclient

def get_embeddings_batch(texts):
    try:
        response = httpx.post(OLLAMA_EMBED_URL, json={
            "model": OLLAMA_MODEL,
            "input": texts
        }, timeout=120.0)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("embeddings", [])
        else:
            print(f"[-] Error de Ollama: {response.text}")
            return []
    except Exception as e:
        print(f"[-] Error de conexión con Ollama: {e}")
        return []

def generate_stable_id(text):
    hash_obj = hashlib.md5(text.encode('utf-8'))
    return str(uuid.UUID(hash_obj.hexdigest()))

def upload_to_qdrant(qclient, points_batch):
    if not points_batch: return
    try:
        qclient.upsert(
            collection_name=COLLECTION,
            points=points_batch
        )
        print(f"    [+] Subidos {len(points_batch)} chunks de Obsidian a Qdrant.")
    except Exception as e:
        print(f"    [-] Error subiendo batch a Qdrant: {e}")

def process_batch(qclient, current_batch):
    if not current_batch: return
    texts_to_embed = [item["text"] for item in current_batch]
    embeddings = get_embeddings_batch(texts_to_embed)
    
    if len(embeddings) == len(texts_to_embed):
        points = []
        for i, item in enumerate(current_batch):
            points.append(
                PointStruct(
                    id=item["id"],
                    vector=embeddings[i],
                    payload=item["payload"]
                )
            )
        upload_to_qdrant(qclient, points)
        time.sleep(0.5)
    else:
        print("    [-] El tamaño de embeddings no coincide con el batch.")

def run_ingestion():
    qclient = init_qdrant()
    obsidian_dir = Path("data/obsidian_vault")
    
    if not obsidian_dir.is_dir():
        print(f"[-] No se encontró el directorio de Obsidian en: {obsidian_dir}")
        return
        
    print("=========================================================")
    print(" 💎 INYECTOR DE BÓVEDA OBSIDIAN (MARKDOWN CHUNKING) ")
    print("=========================================================")
    
    current_batch = []
    total_injected = 0
    
    # Recorrer todos los .md recursivamente (excluyendo carpetas ocultas de obsidian)
    for md_file in obsidian_dir.rglob("*.md"):
        if ".obsidian" in str(md_file):
            continue
            
        print(f"\n[*] Analizando nota: {md_file.name} ...")
        try:
            with open(md_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                
            if not content.strip():
                continue
                
            # Trocear por encabezados
            md_header_splits = markdown_splitter.split_text(content)
            
            for split in md_header_splits:
                chunk_text = split.page_content.strip()
                if not chunk_text:
                    continue
                
                # Construir el texto final con el contexto de los títulos
                headers_context = " | ".join([f"{k}: {v}" for k, v in split.metadata.items()])
                if headers_context:
                    full_text = f"[{md_file.name}] {headers_context}\n{chunk_text}"
                else:
                    full_text = f"[{md_file.name}]\n{chunk_text}"
                    
                stable_id = generate_stable_id(full_text)
                
                payload = {
                    "text_content": full_text,
                    "agencia_id": "lifextreme",
                    "tier": "tier_1", # Obsidian es inteligencia de negocio (Tier 1)
                    "source": "obsidian_vault",
                    "document_name": md_file.name,
                    "headers": split.metadata
                }
                
                current_batch.append({"id": stable_id, "text": full_text, "payload": payload})
                
                if len(current_batch) >= BATCH_SIZE:
                    process_batch(qclient, current_batch)
                    total_injected += len(current_batch)
                    current_batch = []
                    
        except Exception as e:
            print(f"[-] Error procesando {md_file.name}: {e}")
            
    # Flush final
    if current_batch:
        process_batch(qclient, current_batch)
        total_injected += len(current_batch)
        
    print(f"\n=========================================================")
    print(f" 🎉 ¡BÓVEDA OBSIDIAN ASIMILADA! Total Chunks: {total_injected}")
    print("=========================================================")

if __name__ == "__main__":
    run_ingestion()
