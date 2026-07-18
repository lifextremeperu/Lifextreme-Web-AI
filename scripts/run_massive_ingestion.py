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

# Configuración
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
    except Exception as e:
        print(f"    [-] Error subiendo a Qdrant: {e}")

def get_existing_ids(qclient):
    print("[*] Descargando IDs existentes para evitar duplicados y ahorrar tiempo de IA...")
    existing_ids = set()
    offset = None
    while True:
        try:
            r = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll", json={
                "limit": 5000,
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
            print(f"Error en scroll: {e}")
            break
    print(f"    -> {len(existing_ids)} vectores ya existen en Qdrant. Serán omitidos inteligentemente.")
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

def process_file(qclient, existing_ids, file_path, source_name, batch_size=50):
    path_obj = Path(file_path)
    if not path_obj.exists(): return 0
    
    content = ""
    ext = path_obj.suffix.lower()
    if ext == ".pdf":
        content = extract_pdf_text(file_path)
    elif ext == ".docx":
        content = extract_docx_text(file_path)
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
        text = f"Contexto: {source_name} | Archivo: {path_obj.name} | Contenido: {chunk}"
        vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, text))
        
        # FILTRO ANTIDUPLICADOS: Evita gastar tokens en IA si ya existe
        if vector_uuid in existing_ids:
            continue
            
        texts_batch.append(text)
        payloads_batch.append({
            "tenant_id": TENANT_ID,
            "vector_id": vector_uuid,
            "tier": 2,
            "region": "global",
            "modulo_nombre": source_name,
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
                print(f"    [+] {total_new} vectores nuevos inyectados de {path_obj.name}")
            texts_batch = []
            payloads_batch = []
            
    if texts_batch:
        embs = get_embeddings(texts_batch)
        if embs and len(embs) == len(texts_batch):
            points = [PointStruct(id=p["vector_id"], vector=emb, payload=p) for p, emb in zip(payloads_batch, embs)]
            upsert_batch(qclient, points)
            total_new += len(points)
            for p in points: existing_ids.add(p.id)
            print(f"    [+] {total_new} vectores nuevos inyectados de {path_obj.name}")
            
    return total_new

def main():
    print("===================================================================")
    print(" 🚀 INYECCIÓN MASIVA LIFEXTREME (Filtro Antiduplicados Activado) ")
    print("===================================================================")
    
    qclient = QdrantClient(url=QDRANT_URL)
    existing_ids = get_existing_ids(qclient)
    
    directories = [
        (r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\obsidian_vault", "ObsidianVault"),
        (r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge", "FQSAs_Knowledge"),
        (r"D:\HUB-CUSCO-2026\apps\data\knowledge\lifextreme\sources", "HubCuscoSources"),
        (r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME", "LifextremeDocs"),
        (r"D:\HUB-CUSCO-2026\apps\hub-cusco-2026", "HubCuscoProject")
    ]
    
    # Filtro super estricto para obviar carpetas de programacion
    ignore_dirs = ["node_modules", ".git", "dist", "build", "venv", "__pycache__", ".next", ".vscode", "components", "pages", "styles"]
    valid_exts = [".md", ".pdf", ".docx", ".txt"]
    
    grand_total = 0
    
    for dir_path, source_name in directories:
        print(f"\n[*] Escaneando Bóveda: {source_name}")
        base_path = Path(dir_path)
        if not base_path.exists():
            print(f"    [-] Directorio no encontrado: {dir_path}")
            continue
            
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in valid_exts:
                    file_path = os.path.join(root, f)
                    try:
                        new_vecs = process_file(qclient, existing_ids, file_path, source_name)
                        grand_total += new_vecs
                    except Exception as e:
                        pass
                        
    print("\n===================================================================")
    print(f" ✅ INYECCIÓN MASIVA FINALIZADA. TOTAL NUEVOS VECTORES: {grand_total}")
    print("===================================================================")

if __name__ == "__main__":
    main()
