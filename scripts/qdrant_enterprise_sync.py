import os
import re
import csv
import json
import uuid
import httpx
import argparse
import time
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# Configuraciones base
QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

def get_embeddings(texts):
    """Obtiene embeddings de Ollama en lote."""
    try:
        response = httpx.post(OLLAMA_URL, json={
            "model": "nomic-embed-text",
            "input": texts
        }, timeout=120.0)
        response.raise_for_status()
        return response.json().get('embeddings', [])
    except Exception as e:
        print(f"[-] Error con Ollama: {e}")
        return []

def upsert_batch(qclient, points):
    if not points: return
    try:
        qclient.upsert(
            collection_name=COLLECTION,
            points=points
        )
        print(f"    [+] Subidos {len(points)} vectores a Qdrant.")
    except Exception as e:
        print(f"    [-] Error subiendo a Qdrant: {e}")

def get_existing_ids(qclient):
    """Descarga todos los IDs existentes en Qdrant para evitar duplicados."""
    print("[*] Descargando hashes existentes para reanudación segura...")
    existing_ids = set()
    offset = None
    while True:
        try:
            r = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll", json={
                "limit": 5000,
                "with_payload": False,
                "with_vector": False,
                "offset": offset
            })
            if r.status_code != 200: break
            data = r.json().get("result", {})
            points = data.get("points", [])
            if not points: break
            
            for p in points:
                existing_ids.add(p["id"])
                
            offset = data.get("next_page_offset")
            if not offset: break
        except:
            break
    print(f"    -> Encontrados {len(existing_ids)} vectores en DB.")
    return existing_ids

def process_tier_1_fqsas(qclient, existing_ids, batch_size):
    print("\n=======================================================")
    print(" >>> TIER 1: SINCRONIZANDO FQSAs REGIONALES (JSON)")
    print("=======================================================")
    base_dir = Path("data/knowledge")
    
    texts_batch = []
    payloads_batch = []
    total_processed = 0
    
    for json_file in base_dir.rglob("*.json"):
        if "max_" in json_file.name or "seed" in json_file.name: continue
        
        region = json_file.parent.name
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                qa_pairs = []
                modulo = "General"
                
                if isinstance(data, list):
                    modulo = json_file.stem.split("-")[0] # ej. ALOJA
                    for qa in data:
                        q = qa.get("q") or qa.get("pregunta", "")
                        a = qa.get("a") or qa.get("respuesta", "")
                        if q and a: qa_pairs.append((q, a))
                else:
                    modulo = data.get("modulo_nombre", "General")
                    fqsas_dict = data.get("fqsas", {})
                    for angle, qa_list in fqsas_dict.items():
                        if not isinstance(qa_list, list): continue
                        for qa in qa_list:
                            q = qa.get("q", "")
                            a = qa.get("a", "")
                            if q and a: qa_pairs.append((q, a))
                            
                for q, a in qa_pairs:
                    text = f"Región: {region.capitalize()}. Módulo: {modulo}. Pregunta: {q} Respuesta: {a}"
                    vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
                    
                    if vector_uuid in existing_ids:
                        continue
                        
                    texts_batch.append(text)
                    payloads_batch.append({
                        "tenant_id": TENANT_ID,
                        "vector_id": vector_uuid,
                        "tier": 1,
                        "region": region,
                        "modulo_nombre": modulo,
                        "source": json_file.name,
                        "text_content": text
                    })
                    
                    if len(texts_batch) >= batch_size:
                        embs = get_embeddings(texts_batch)
                        if embs and len(embs) == len(texts_batch):
                            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                            upsert_batch(qclient, points)
                            total_processed += len(points)
                        texts_batch = []
                        payloads_batch = []
                        time.sleep(0.5) # Pausa técnica para enfriar Ollama
        except Exception as e:
            print(f"[-] Error en {json_file.name}: {e}")
            
    # Remanente
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total_processed += len(points)
            
    print(f"\n[+] TIER 1 FINALIZADO: {total_processed} FQSAs inyectados.")

def process_tier_2_csv(qclient, existing_ids, batch_size):
    print("\n=======================================================")
    print(" >>> TIER 2: SINCRONIZANDO CATÁLOGO OPERATIVO (CSV)")
    print("=======================================================")
    csv_path = "tours_faq.csv"
    if not os.path.exists(csv_path):
        print("[-] Archivo tours_faq.csv no encontrado.")
        return
        
    texts_batch = []
    payloads_batch = []
    total_processed = 0
    
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        header = next(reader, None) # Saltar header si existe
        
        for row in reader:
            if not row or len(row) < 2: continue
            q = row[0].strip()
            a = row[1].strip()
            if not q or not a: continue
            
            text = f"Catálogo Operativo Lifextreme. Pregunta: {q} Respuesta: {a}"
            vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
            
            if vector_uuid in existing_ids:
                continue
                
            texts_batch.append(text)
            payloads_batch.append({
                "tenant_id": TENANT_ID,
                "vector_id": vector_uuid,
                "tier": 2,
                "region": "global",
                "modulo_nombre": "CatalogoTours",
                "source": "tours_faq.csv",
                "text_content": text
            })
            
            if len(texts_batch) >= batch_size:
                embs = get_embeddings(texts_batch)
                if embs and len(embs) == len(texts_batch):
                    points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                    upsert_batch(qclient, points)
                    total_processed += len(points)
                texts_batch = []
                payloads_batch = []
                time.sleep(0.5)
                
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total_processed += len(points)
            
    print(f"\n[+] TIER 2 FINALIZADO: {total_processed} filas CSV inyectadas.")

def chunk_markdown_by_headers(text):
    """Chunking semántico avanzado usando encabezados ##"""
    chunks = []
    parts = re.split(r'(^##\s+.*$)', text, flags=re.MULTILINE)
    
    current_chunk = ""
    for part in parts:
        if part.startswith("## "):
            if len(current_chunk) > 100:
                chunks.append(current_chunk.strip())
            current_chunk = part + "\n"
        else:
            current_chunk += part
            if len(current_chunk) > 1500: # Max tamaño forzado si el ## es muy largo
                chunks.append(current_chunk[:1500].strip())
                current_chunk = current_chunk[1500:] # Sin solapamiento complejo para mantenerlo rapido
                
    if len(current_chunk) > 50:
        chunks.append(current_chunk.strip())
        
    # Eliminar vacios
    return [c for c in chunks if c.strip()]

def process_tier_3_markdown(qclient, existing_ids, batch_size):
    print("\n=======================================================")
    print(" >>> TIER 3: SINCRONIZANDO CONOCIMIENTO NO ESTRUCTURADO")
    print("=======================================================")
    
    files_to_process = []
    # Obsidian Vault
    obsidian_path = Path("data/obsidian_vault")
    if obsidian_path.exists():
        files_to_process.extend(list(obsidian_path.rglob("*.md")))
        
    # Raíz MDs
    root_mds = ["AI_PERSONALIZATION_DOCS.md", "boletin_inteligencia_cusco.md", "expediente_montana_colores.md"]
    for md in root_mds:
        if os.path.exists(md): files_to_process.append(Path(md))
        
    texts_batch = []
    payloads_batch = []
    total_processed = 0
    
    for md_file in files_to_process:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            chunks = chunk_markdown_by_headers(content)
            for chunk in chunks:
                text = f"Documento: {md_file.name}. Contenido: {chunk}"
                vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
                
                if vector_uuid in existing_ids:
                    continue
                    
                texts_batch.append(text)
                payloads_batch.append({
                    "tenant_id": TENANT_ID,
                    "vector_id": vector_uuid,
                    "tier": 3,
                    "region": "global",
                    "modulo_nombre": "NarrativaMD",
                    "source": md_file.name,
                    "text_content": text
                })
                
                if len(texts_batch) >= batch_size:
                    embs = get_embeddings(texts_batch)
                    if embs and len(embs) == len(texts_batch):
                        points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                        upsert_batch(qclient, points)
                        total_processed += len(points)
                    texts_batch = []
                    payloads_batch = []
                    time.sleep(0.5)
        except Exception as e:
            print(f"[-] Error en {md_file.name}: {e}")
            
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total_processed += len(points)
            
    print(f"\n[+] TIER 3 FINALIZADO: {total_processed} chunks inyectados.")

def main():
    parser = argparse.ArgumentParser(description="Lifextreme Enterprise RAG Sincronizador")
    parser.add_argument("--tier", type=int, action='append', help="Tiers a ejecutar (1, 2, 3)")
    parser.add_argument("--batch-size", type=int, default=100, help="Tamaño del lote para Ollama")
    args = parser.parse_args()
    
    tiers_to_run = args.tier if args.tier else [1, 2, 3]
    
    print("===================================================================")
    print(f" 🚀 INICIANDO SINCRONIZACIÓN ENTERPRISE RAG (Tiers: {tiers_to_run}) ")
    print("===================================================================")
    
    qclient = QdrantClient(url=QDRANT_URL)
    
    if not qclient.collection_exists(COLLECTION):
        qclient.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"[*] Colección {COLLECTION} creada.")
        
    existing_ids = get_existing_ids(qclient)
    
    if 1 in tiers_to_run:
        process_tier_1_fqsas(qclient, existing_ids, args.batch_size)
    if 2 in tiers_to_run:
        process_tier_2_csv(qclient, existing_ids, args.batch_size)
    if 3 in tiers_to_run:
        process_tier_3_markdown(qclient, existing_ids, args.batch_size)
        
    print("\n✅ SINCRONIZACIÓN MAESTRA COMPLETADA.")

if __name__ == "__main__":
    main()
