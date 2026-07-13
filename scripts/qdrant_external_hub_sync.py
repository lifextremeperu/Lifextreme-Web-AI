import os
import uuid
import httpx
import argparse
import time
from pathlib import Path
import pandas as pd
from pypdf import PdfReader
import docx
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

# Configuraciones base
QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

def get_embeddings(texts):
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

# --- EXTRACTORES DE TEXTO ---

def extract_pdf_text(filepath):
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    except Exception as e:
        print(f"[-] Error leyendo PDF {filepath}: {e}")
    return text

def extract_docx_text(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
    except Exception as e:
        print(f"[-] Error leyendo DOCX {filepath}: {e}")
    return text

def chunk_text(text, max_size=1000):
    """Divide texto por párrafos para mantener sentido semántico."""
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        if len(current_chunk) + len(p) > max_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = p + " "
        else:
            current_chunk += p + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# --- BLOQUES DE PROCESAMIENTO ---

def process_file_generic(qclient, existing_ids, file_path, tier, modulo_nombre, visibility="public", batch_size=50):
    path_obj = Path(file_path)
    if not path_obj.exists(): return 0
    
    if path_obj.suffix.lower() == ".pdf":
        content = extract_pdf_text(file_path)
    elif path_obj.suffix.lower() == ".docx":
        content = extract_docx_text(file_path)
    elif path_obj.suffix.lower() == ".md":
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except: return 0
    else:
        return 0
        
    if not content.strip(): return 0
    
    chunks = chunk_text(content)
    texts_batch = []
    payloads_batch = []
    total = 0
    
    for i, chunk in enumerate(chunks):
        if visibility == "internal_b2b":
            text = f"CONFIDENCIAL B2B (Documento: {path_obj.name}): {chunk}"
        else:
            text = f"Narrativa/Contexto (Documento: {path_obj.name}): {chunk}"
            
        vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
        if vector_uuid in existing_ids: continue
        
        texts_batch.append(text)
        payloads_batch.append({
            "tenant_id": TENANT_ID,
            "vector_id": vector_uuid,
            "tier": tier,
            "region": "global",
            "modulo_nombre": modulo_nombre,
            "source": path_obj.name,
            "visibility": visibility,
            "text_content": text
        })
        
        if len(texts_batch) >= batch_size:
            embs = get_embeddings(texts_batch)
            if embs and len(embs) == len(texts_batch):
                points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                upsert_batch(qclient, points)
                total += len(points)
            texts_batch = []
            payloads_batch = []
            time.sleep(0.5)
            
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total += len(points)
            
    return total

def process_block_a(qclient, existing_ids, batch_size):
    print("\n=======================================================")
    print(" >>> BLOQUE A: DATA EXTERNA (PDFs, DOCX, Confidencial)")
    print("=======================================================")
    base_dir = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME")
    total_processed = 0
    
    # 1. PAQUETES (Tier 2.5 -> lo guardamos como Tier 2 para Qdrant)
    paquetes_dir = base_dir / "PAQUETES"
    if paquetes_dir.exists():
        print("[*] Procesando PAQUETES (Narrativa Itinerarios)...")
        for pdf in paquetes_dir.rglob("*.pdf"):
            total_processed += process_file_generic(qclient, existing_ids, pdf, 2, "ItinerariosNarrativa", "public", batch_size)
            
    # 2. USP (Glamping, Sonoterapia) (Tier 3)
    print("[*] Procesando Glamping y Sonoterapia (Proyectos USP)...")
    for subdir in ["GLAMPING TIPI COYA", "SONOTERAPIA"]:
        d = base_dir / subdir
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and f.suffix.lower() in [".pdf", ".docx"]:
                    total_processed += process_file_generic(qclient, existing_ids, f, 3, "ProyectosEspeciales", "public", batch_size)
                    
    # 3. CONFIDENCIAL B2B (Tier 3 pero con visibilidad interna)
    print("[*] Procesando Documentos Confidenciales B2B...")
    b2b_files = ["COSTOS OPERATIVOS LIFEXTREME.docx", "OBJETO SOCIAL LIFEXTREME.docx", "CARTERA CUSCO- AGENCIAS DE VIAJES.pdf"]
    for f_name in b2b_files:
        f = base_dir / f_name
        if f.exists():
            total_processed += process_file_generic(qclient, existing_ids, f, 3, "InteligenciaB2B", "internal_b2b", batch_size)
            
    print(f"[+] BLOQUE A FINALIZADO: {total_processed} chunks inyectados.")

def process_block_b(qclient, existing_ids, batch_size):
    print("\n=======================================================")
    print(" >>> BLOQUE B: HUB CUSCO 2026 (CIXTUR y Regulaciones)")
    print("=======================================================")
    base_dir = Path(r"D:\HUB-CUSCO-2026\apps\data\knowledge\lifextreme\sources")
    total_processed = 0
    
    # 1. EXCEL CIXTUR (Tier 1)
    excel_path = base_dir / "DATA SET" / "DATA SET CIXTUR 23_11_25 (1).xlsx"
    if excel_path.exists():
        print("[*] Procesando Excel Maestro CIXTUR (Esto puede tardar)...")
        try:
            df = pd.read_excel(excel_path)
            # Asumimos que las columnas relevantes son parecidas a pregunta/respuesta o descripción
            # Iteramos filas convirtiéndolas en texto denso
            texts_batch = []
            payloads_batch = []
            for index, row in df.iterrows():
                row_dict = row.dropna().to_dict()
                if not row_dict: continue
                # Construir string con las keys y values
                text = "Cusco Data (CIXTUR): " + " | ".join([f"{k}: {v}" for k, v in row_dict.items()])
                
                vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
                if vector_uuid in existing_ids: continue
                
                texts_batch.append(text)
                payloads_batch.append({
                    "tenant_id": TENANT_ID,
                    "vector_id": vector_uuid,
                    "tier": 1,
                    "region": "cusco",
                    "modulo_nombre": "DatasetCixtur",
                    "source": "DATA_SET_CIXTUR.xlsx",
                    "visibility": "public",
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
            # Restante
            if texts_batch:
                embs = get_embeddings(texts_batch)
                if embs and len(embs) == len(texts_batch):
                    points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                    upsert_batch(qclient, points)
                    total_processed += len(points)
        except Exception as e:
            print(f"[-] Error procesando Excel: {e}")
            
    # 2. INVESTIGACION AGENTE (Tier 3)
    inv_dir = base_dir / "INVESTIGACION AGENTE"
    if inv_dir.exists():
        print("[*] Procesando Investigaciones del Agente (.md)...")
        for md in inv_dir.rglob("*.md"):
            total_processed += process_file_generic(qclient, existing_ids, md, 3, "InvestigacionAgente", "public", batch_size)
            
    # 3. REGULACIONES Y LEYES (Tier 2)
    print("[*] Procesando Normativas y Leyes...")
    for subdir in ["MINCETUR", "REGLAMENTO", "LEGAL"]:
        d = base_dir / subdir
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and f.suffix.lower() in [".pdf", ".docx", ".md"]:
                    total_processed += process_file_generic(qclient, existing_ids, f, 2, "RegulacionTurismo", "public", batch_size)
                    
    print(f"[+] BLOQUE B FINALIZADO: {total_processed} chunks inyectados.")

def main():
    parser = argparse.ArgumentParser(description="Sincronizador Multiformato External & HUB CUSCO")
    parser.add_argument("--block", type=str, choices=["A", "B", "ALL"], default="ALL", help="Bloque a ejecutar")
    parser.add_argument("--batch-size", type=int, default=50, help="Tamaño del lote para Ollama")
    args = parser.parse_args()
    
    print("===================================================================")
    print(f" 🚀 INICIANDO SINCRONIZADOR MULTIFORMATO (Block: {args.block}) ")
    print("===================================================================")
    
    qclient = QdrantClient(url=QDRANT_URL)
    existing_ids = get_existing_ids(qclient)
    
    if args.block in ["A", "ALL"]:
        process_block_a(qclient, existing_ids, args.batch_size)
    if args.block in ["B", "ALL"]:
        process_block_b(qclient, existing_ids, args.batch_size)
        
    print("\n✅ SINCRONIZACIÓN MULTIFORMATO COMPLETADA.")

if __name__ == "__main__":
    main()
