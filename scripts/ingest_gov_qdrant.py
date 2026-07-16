import sys
import os
import json
import uuid
import httpx
import time
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from legal_chunker import extract_text_from_pdf, chunk_legal_document

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

TARGET_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO"
METADATA_FILE = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\gov_metadata.json"

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

def main():
    print("===================================================================")
    print(" 🚀 ORQUESTADOR DE INGESTA GUBERNAMENTAL (LIFEXTREME AI) ")
    print("===================================================================")
    
    if not os.path.exists(METADATA_FILE):
        print(f"[-] No se encontró {METADATA_FILE}. Ejecuta download_gov_docs.py primero.")
        return
        
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        documents = json.load(f)
        
    try:
        qclient = QdrantClient(url=QDRANT_URL)
        if not qclient.collection_exists(COLLECTION):
            print(f"[*] Colección {COLLECTION} no existe, creándola...")
            qclient.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
    except Exception as e:
        print(f"[-] Error conectando a Qdrant. ¿Está encendido? Error: {e}")
        return

    for doc in documents:
        pdf_path = os.path.join(TARGET_DIR, doc['filename'])
        if not os.path.exists(pdf_path):
            print(f"    [SKIP] Archivo no encontrado en disco: {doc['filename']}")
            continue
            
        print(f"\n[*] Procesando documento: {doc['filename']}")
        
        try:
            text = extract_text_from_pdf(pdf_path)
            # Agregar source a la metadata base
            base_meta = doc.copy()
            base_meta["source"] = doc['filename']
            base_meta["tier"] = 0 # Tier 0 para info gubernamental crítica
            
            chunks = chunk_legal_document(text, base_meta)
            print(f"    [+] Generados {len(chunks)} fragmentos estructurados.")
            
            texts_batch = []
            payloads_batch = []
            success_count = 0
            batch_size = 50 
            
            for chunk in chunks:
                chunk_text = chunk["text"]
                vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_text + doc["filename"]))
                
                texts_batch.append(chunk_text)
                
                payload = {
                    "tenant_id": TENANT_ID,
                    "vector_id": vector_uuid,
                    "text_content": chunk_text,
                    **chunk["metadata"]
                }
                payloads_batch.append(payload)
                
                if len(texts_batch) >= batch_size:
                    embs = get_embeddings(texts_batch)
                    if embs and len(embs) == len(texts_batch):
                        points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                        if upsert_batch(qclient, points):
                            success_count += len(points)
                            print(f"    [+] Inyectados {success_count} vectores a Qdrant...")
                    
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
                        print(f"    [+] Inyectados remanentes. Total: {success_count} vectores para {doc['filename']}.")
                        
        except Exception as e:
            print(f"    [ERROR] Fallo al procesar {doc['filename']}: {e}")
            
    print("\n===================================================================")
    print(" ✅ INGESTA GUBERNAMENTAL COMPLETADA ")
    print("===================================================================")

if __name__ == "__main__":
    main()
