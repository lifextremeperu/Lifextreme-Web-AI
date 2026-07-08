import os
import gc
import json
import hashlib
import time
from pathlib import Path
import fitz  # PyMuPDF
from dotenv import load_dotenv
from supabase import create_client, Client
from ingestion_rules import ChunkMetadata, ProcessedChunk, CategoriaTuristica

import logging
logging.basicConfig(
    filename='logs_ingesta_chile.txt', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan credenciales de Supabase en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

STATE_FILE = "ingestion_state_chile.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"procesados": []}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def get_file_hash(filepath: str) -> str:
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Error leyendo {filepath} para hash: {e}")
        return None

def extract_and_chunk_pdf(filepath: str, max_chunk_len=1000):
    chunks = []
    try:
        doc = fitz.open(filepath)
        current_chunk = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("blocks")
            for b in blocks:
                text = b[4].strip()
                if len(text) < 20: 
                    continue
                if len(current_chunk) + len(text) > max_chunk_len and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = text
                else:
                    current_chunk += " " + text
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        doc.close()
    except Exception as e:
        logging.error(f"Error extrayendo {filepath}: {e}")
        
    return chunks

def process_chile_pdfs(base_dir: str):
    print("[+] Cargando modelo de Embedding bge-m3 para CHILE (Cuidando RAM...)")
    try:
        from sentence_transformers import SentenceTransformer
        embedder = SentenceTransformer('BAAI/bge-m3')
    except Exception as e:
        print(f"Error cargando el modelo de embeddings: {e}")
        return

    state = load_state()
    base_path = Path(base_dir)
    
    pdf_files = list(base_path.rglob("*.pdf"))
    
    print(f"[*] Encontrados {len(pdf_files)} PDFs de Chile listos para vectorizar.")
    
    for pdf_path in pdf_files:
        filepath = str(pdf_path)
        file_hash = get_file_hash(filepath)
        
        if not file_hash:
            continue
        
        if file_hash in state["procesados"]:
            print(f"[-] Saltando {pdf_path.name} (Ya vectorizado)")
            continue
            
        print(f"\n[>>>] Procesando Chile PDF: {pdf_path.name}")
        
        chunks = extract_and_chunk_pdf(filepath)
        print(f"    - Extraídos {len(chunks)} chunks semánticos.")
        
        if not chunks:
            state["procesados"].append(file_hash)
            save_state(state)
            continue
            
        try:
            print("    - Generando Embeddings (BGE-M3)...")
            embeddings = embedder.encode(chunks, batch_size=16, show_progress_bar=False)
            
            payload = []
            for i, (text_chunk, emb) in enumerate(zip(chunks, embeddings)):
                chunk_id = hashlib.md5(f"{file_hash}_{i}".encode()).hexdigest()
                
                # METADATOS CLAVE PARA CHILE
                meta = ChunkMetadata(
                    archivo_origen=pdf_path.name,
                    pais="Chile",
                    region="Macrozona_Chile" # Por defecto, si tuviéramos subcarpetas podríamos extraerlas
                ).model_dump()
                
                payload.append({
                    "id": chunk_id,
                    "content": text_chunk,
                    "metadata": meta,
                    "embedding": emb.tolist()
                })
            
            print(f"    - Subiendo a Supabase pgvector ({len(payload)} chunks)...")
            batch_size = 50
            for i in range(0, len(payload), batch_size):
                batch = payload[i:i+batch_size]
                supabase.table("knowledge_chunks").upsert(batch).execute()
                
            state["procesados"].append(file_hash)
            save_state(state)
            print(f"    - [OK] Completado y guardado de forma soberana!")
            
        except Exception as e:
            logging.error(f"Fallo en {filepath}: {str(e)}")
            print(f"    - ERROR: {e}")
            
        del chunks
        gc.collect()
        time.sleep(1)

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_pdfs', 'chile'))
    print("=====================================================")
    print("   LIFEXTREME INTELLIGENCE: INGESTA CHILE (DIVS-v1)  ")
    print("=====================================================")
    if not os.path.exists(BASE_DIR):
        print(f"La carpeta {BASE_DIR} no existe aún. Ejecuta el spider primero.")
    else:
        process_chile_pdfs(BASE_DIR)
