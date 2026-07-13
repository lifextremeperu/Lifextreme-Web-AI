import sys
import os
import json
import uuid
import httpx
import time
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

QUEUE_DIR = Path("data/knowledge/queue")

def get_embeddings(texts):
    """Obtiene embeddings de Ollama (nomic-embed-text)."""
    try:
        response = httpx.post(OLLAMA_URL, json={
            "model": "nomic-embed-text",
            "input": texts
        }, timeout=120.0)
        response.raise_for_status()
        return response.json().get('embeddings', [])
    except Exception as e:
        print(f"[-] Error obteniendo embeddings de Ollama: {e}")
        return []

def upsert_batch(qclient, points):
    if not points: return False
    try:
        qclient.upsert(
            collection_name=COLLECTION,
            points=points
        )
        return True
    except Exception as e:
        print(f"[-] Error subiendo a Qdrant: {e}")
        return False

def process_queue_file(qclient, jsonl_path):
    print(f"\n[*] Procesando archivo de cola: {jsonl_path.name}")
    
    texts_batch = []
    payloads_batch = []
    success_count = 0
    batch_size = 50  # Lote seguro para Ollama
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            data = json.loads(line)
            
            text = data["text"]
            vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text + data["metadata"].get("source", "")))
            
            texts_batch.append(text)
            payloads_batch.append({
                "tenant_id": TENANT_ID,
                "vector_id": vector_uuid,
                "tier": 4,  # Auto-scanned docs
                "region": "global",
                "modulo_nombre": data["metadata"].get("category", "General"),
                "source": data["metadata"].get("filename", "unknown"),
                "text_content": text
            })
            
            if len(texts_batch) >= batch_size:
                embs = get_embeddings(texts_batch)
                if embs and len(embs) == len(texts_batch):
                    points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                    if upsert_batch(qclient, points):
                        success_count += len(points)
                        print(f"    [+] Subidos {success_count} vectores a Qdrant...")
                
                texts_batch = []
                payloads_batch = []
                time.sleep(0.5)
                
    # Remanentes
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            if upsert_batch(qclient, points):
                success_count += len(points)
                print(f"    [+] Subidos remanentes. Total: {success_count} vectores.")
                
    return success_count > 0

def main():
    print("===================================================================")
    print(" 🚀 INYECTOR FINAL: DE COLA A QDRANT ")
    print("===================================================================")
    
    if not QUEUE_DIR.exists():
        print("[-] No hay carpeta de cola. Ejecuta run_smart_ingestion.py primero.")
        return
        
    jsonl_files = list(QUEUE_DIR.glob("*.jsonl"))
    if not jsonl_files:
        print("[-] La cola está vacía. No hay archivos para inyectar.")
        return
        
    print(f"[*] Archivos en cola detectados: {len(jsonl_files)}")
    
    qclient = QdrantClient(url=QDRANT_URL)
    
    if not qclient.collection_exists(COLLECTION):
        print(f"[*] Colección {COLLECTION} no existe, creándola...")
        qclient.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        
    for jsonl_file in jsonl_files:
        success = process_queue_file(qclient, jsonl_file)
        if success:
            # Eliminar para liberar la cola
            os.remove(jsonl_file)
            print(f"    [✓] Archivo de cola {jsonl_file.name} inyectado y eliminado.")
        else:
            print(f"    [!] Hubo un problema inyectando {jsonl_file.name}. Se mantiene en cola.")
            
    print("\n===================================================================")
    print(" ✅ INYECCIÓN A QDRANT FINALIZADA ")
    print("===================================================================")

if __name__ == "__main__":
    main()
