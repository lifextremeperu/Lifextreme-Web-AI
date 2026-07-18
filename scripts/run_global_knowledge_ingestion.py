import os
import sys
import uuid
import time
import httpx
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from pypdf import PdfReader
import docx

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://localhost:11434/api/embed"
COLLECTION = "Lifextreme_Knowledge"
TENANT_ID = "lifextreme"

KEYWORDS = [
    "turismo", "mincetur", "promperu", "viaje", "travel", "itinerario", 
    "tour", "hotel", "guia", "legal", "reglamento", "contrato", "cusco", 
    "peru", "sutran", "sernanp", "aventura", "glamping", "lifextreme",
    "paquete", "ruta", "montaña", "andes", "amazonas", "reserva", "ciclovia",
    "bot", "inteligencia"
]
VALID_EXTS = [".pdf", ".docx", ".md", ".xlsx", ".pptx", ".txt"]
IGNORE_DIRS = {
    "Windows", "Program Files", "Program Files (x86)", "AppData", "node_modules", 
    ".git", "dist", "build", "venv", "__pycache__", "$RECYCLE.BIN", "System Volume Information",
    ".vscode", "Cache", "Temp", "ProgramData"
}

def is_relevant(filepath):
    path_lower = filepath.lower()
    for kw in KEYWORDS:
        if kw in path_lower:
            return True
    return False

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
        qclient.upsert(collection_name=COLLECTION, points=points)
    except Exception as e:
        print(f"    [-] Error subiendo a Qdrant: {e}")

def get_existing_ids(qclient):
    print("[*] Descargando IDs actuales (Sistema Anti-Duplicados)...")
    existing_ids = set()
    offset = None
    while True:
        try:
            r = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll", json={
                "limit": 10000,
                "with_payload": False,
                "with_vector": False,
                "offset": offset
            }, timeout=60.0)
            if r.status_code != 200: break
            data = r.json().get("result", {})
            points = data.get("points", [])
            if not points: break
            for p in points:
                existing_ids.add(p["id"])
            offset = data.get("next_page_offset")
            if not offset: break
        except Exception as e:
            print(f"Error en scroll API: {e}")
            break
    print(f"    -> {len(existing_ids)} vectores en memoria. Serán omitidos.")
    return existing_ids

def extract_pdf_text(filepath):
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            t = page.extract_text()
            if t: text += t + "\n"
    except: pass
    return text

def extract_docx_text(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            if para.text.strip(): text += para.text + "\n"
    except: pass
    return text

def chunk_text(text, max_size=1000):
    paragraphs = text.split('\n')
    chunks = []
    current = ""
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        if len(current) + len(p) > max_size and current:
            chunks.append(current.strip())
            current = p + " "
        else:
            current += p + " "
    if current: chunks.append(current.strip())
    return chunks

def process_file(qclient, existing_ids, file_path, batch_size=50):
    path_obj = Path(file_path)
    if not path_obj.exists(): return 0
    
    content = ""
    ext = path_obj.suffix.lower()
    if ext == ".pdf": content = extract_pdf_text(file_path)
    elif ext == ".docx": content = extract_docx_text(file_path)
    elif ext in [".md", ".txt"]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except: return 0
    else: return 0
        
    if not content.strip(): return 0
    
    chunks = chunk_text(content)
    texts_batch = []
    payloads_batch = []
    total_new = 0
    
    for chunk in chunks:
        text = f"Archivo: {path_obj.name} | Ubicacion: {path_obj.parent.name} | Contenido: {chunk}"
        vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
        
        if vector_uuid in existing_ids:
            continue
            
        texts_batch.append(text)
        payloads_batch.append({
            "tenant_id": TENANT_ID,
            "vector_id": vector_uuid,
            "tier": 2,
            "region": "global",
            "modulo_nombre": "ConocimientoGlobal",
            "source": path_obj.name,
            "text_content": text
        })
        
        if len(texts_batch) >= batch_size:
            embs = get_embeddings(texts_batch)
            if embs and len(embs) == len(texts_batch):
                points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
                upsert_batch(qclient, points)
                total_new += len(points)
                for p in points: existing_ids.add(p.id)
                print(f"    [+] {total_new} nuevos inyectados de {path_obj.name}...")
            texts_batch = []
            payloads_batch = []
            
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total_new += len(points)
            for p in points: existing_ids.add(p.id)
            print(f"    [+] {total_new} nuevos inyectados de {path_obj.name} (Finalizado)")
            
    return total_new

def main():
    print("===================================================================")
    print(" 🌍 INYECCIÓN GLOBAL LIFEXTREME (3,138 ARCHIVOS POTENCIALES) ")
    print("===================================================================")
    
    qclient = QdrantClient(url=QDRANT_URL)
    existing_ids = get_existing_ids(qclient)
    
    search_paths = [r"C:\Users\ASUS", r"D:\\"]
    grand_total = 0
    files_processed = 0
    
    for sp in search_paths:
        if not os.path.exists(sp): continue
        print(f"\n[*] Escaneando Unidad: {sp}")
        
        for root, dirs, files in os.walk(sp):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in VALID_EXTS:
                    full_path = os.path.join(root, f)
                    if is_relevant(full_path):
                        # Evitar los que ya hicimos hoy (solo para no imprimir tanto)
                        if "Lifextreme-Web-AI\\data\\knowledge" in full_path or "Lifextreme-Web-AI\\data\\obsidian_vault" in full_path:
                            continue
                        
                        try:
                            new_vecs = process_file(qclient, existing_ids, full_path)
                            if new_vecs > 0:
                                grand_total += new_vecs
                                files_processed += 1
                        except Exception as e:
                            pass
                            
    print("\n===================================================================")
    print(f" ✅ INYECCIÓN GLOBAL FINALIZADA.")
    print(f" Archivos con vectores nuevos: {files_processed}")
    print(f" TOTAL NUEVOS VECTORES: {grand_total}")
    print("===================================================================")

if __name__ == "__main__":
    main()
