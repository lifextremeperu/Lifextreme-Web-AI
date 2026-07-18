import sys
import os
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
TARGET_DIR = Path("data/tupas")

def get_embeddings(texts):
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
    print(" 🚀 INGESTA NACIONAL DE TUPAS REGIONALES (LIFEXTREME AI) ")
    print("===================================================================")
    
    if not TARGET_DIR.exists():
        print(f"[-] No se encontró el directorio {TARGET_DIR}. Ejecuta agent_tupa_downloader.py primero.")
        return
        
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

    # Buscar todos los PDFs recursivamente (incluye subcarpetas como Loreto)
    pdf_files = list(TARGET_DIR.rglob("*.pdf"))
    
    if not pdf_files:
        print("[-] No se encontraron PDFs en data/tupas")
        return
        
    print(f"[*] Encontrados {len(pdf_files)} PDFs TUPA para procesar.")

    for pdf_path in pdf_files:
        filename = pdf_path.name
        print(f"\n[*] Procesando documento: {filename}")
        
        # Extraer región del nombre
        region = filename.replace("TUPA_", "").replace(".pdf", "").replace("_", " ")
        
        try:
            print(f"    [+] Extrayendo texto y chunking...")
            text = extract_text_from_pdf(str(pdf_path))
            
            metadata = {
                "region": region,
                "tipo_documento": "TUPA Regional",
                "source": filename,
                "tier": 0,  # Máxima autoridad legal
                "estado": "Vigente"
            }
            
            chunks = chunk_legal_document(text, metadata)
            print(f"    [+] Generados {len(chunks)} fragmentos estructurados.")
            
            texts_batch = []
            payloads_batch = []
            success_count = 0
            batch_size = 50 
            
            for chunk in chunks:
                chunk_text = chunk["text"]
                vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_text + filename))
                
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
                    time.sleep(0.1)
                    
            # Remanentes
            if texts_batch:
                embs = get_embeddings(texts_batch)
                if embs and len(embs) == len(texts_batch):
                    points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                    if upsert_batch(qclient, points):
                        success_count += len(points)
                        print(f"    [+] Inyectados remanentes. Total: {success_count} vectores para {filename}.")
                        
        except Exception as e:
            print(f"    [ERROR] Fallo al procesar {filename}: {e}")
            
    print("\n===================================================================")
    print(" ✅ INGESTA DE TUPAS REGIONALES COMPLETADA ")
    print("===================================================================")

if __name__ == "__main__":
    main()
