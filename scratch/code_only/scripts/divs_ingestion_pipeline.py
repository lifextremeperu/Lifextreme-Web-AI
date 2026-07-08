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

# Configuración de Logging simple
import logging
logging.basicConfig(
    filename='logs_ingesta.txt', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cargar variables de entorno
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan credenciales de Supabase en el archivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Estado de la ingesta (Checkpoints)
STATE_FILE = "ingestion_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"procesados": []}

def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4)

def extract_region_from_path(filepath: str) -> str:
    """Extrae la región de la carpeta padre."""
    path_parts = Path(filepath).parts
    # Asume estructura: .../LIFEXTREME/[REGION]/archivo.pdf
    if len(path_parts) >= 2:
        return path_parts[-2].lower()
    return "desconocido"

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
    """Extrae texto usando PyMuPDF y hace un chunking básico semántico (por párrafos)."""
    chunks = []
    try:
        doc = fitz.open(filepath)
        current_chunk = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Extraer bloques de texto (mantiene mejor el flujo que extract_text)
            blocks = page.get_text("blocks")
            
            for b in blocks:
                text = b[4].strip()
                # Ignorar basurilla, números de página cortos
                if len(text) < 20: 
                    continue
                
                # Acumular hasta llegar al max_chunk_len
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

def process_pdfs_batch(base_dir: str):
    # Inicializar modelo local SÓLO cuando sea necesario, para ahorrar RAM.
    # Usaremos sentence-transformers para embedding directo.
    print("[+] Cargando modelo de Embedding bge-m3 (Cuidando RAM...)")
    try:
        from sentence_transformers import SentenceTransformer
        # Puedes forzar device='cpu' si la GPU se queda sin memoria
        embedder = SentenceTransformer('BAAI/bge-m3')
    except Exception as e:
        print(f"Error cargando el modelo de embeddings: {e}")
        print("Instala: pip install sentence-transformers")
        return

    state = load_state()
    base_path = Path(base_dir)
    
    subdirs = [d for d in base_path.iterdir() if d.is_dir()]
    total_pdfs = sum(1 for _ in base_path.rglob("*.pdf"))
    
    print(f"[*] Encontrados {total_pdfs} PDFs repartidos en {len(subdirs)} carpetas principales.")
    
    for subdir in subdirs:
        pdf_files = list(subdir.rglob("*.pdf"))
        if not pdf_files:
            continue
            
        print(f"\n=====================================================")
        print(f"📁 PROCESANDO CARPETA: {subdir.name.upper()} ({len(pdf_files)} PDFs)")
        print(f"=====================================================")
        
        for pdf_path in pdf_files:
            filepath = str(pdf_path)
            file_hash = get_file_hash(filepath)
            
            if not file_hash:
                print(f"[-] Saltando {pdf_path.name} (No se puede leer. ¿Está solo en la nube de OneDrive?)")
                continue
            
            if file_hash in state["procesados"]:
                print(f"[-] Saltando {pdf_path.name} (Ya procesado)")
                continue
                
            print(f"\n[>>>] Procesando: {pdf_path.name}")
            region = extract_region_from_path(filepath)
            
            chunks = extract_and_chunk_pdf(filepath)
            print(f"    - Extraídos {len(chunks)} chunks.")
            
            if not chunks:
                print("    - PDF vacío o es solo imágenes (Escaneado). Ignorando.")
                state["procesados"].append(file_hash)
                save_state(state)
                continue
                
            # Generar embeddings en LOTE para optimizar
            try:
                print("    - Generando Embeddings...")
                embeddings = embedder.encode(chunks, batch_size=16, show_progress_bar=False)
                
                # Preparar payload para Supabase
                payload = []
                for i, (text_chunk, emb) in enumerate(zip(chunks, embeddings)):
                    chunk_id = hashlib.md5(f"{file_hash}_{i}".encode()).hexdigest()
                    
                    meta = ChunkMetadata(
                        archivo_origen=pdf_path.name,
                        region=region
                    ).model_dump()
                    
                    payload.append({
                        "id": chunk_id,
                        "content": text_chunk,
                        "metadata": meta,
                        "embedding": emb.tolist()
                    })
                
                # Subir a Supabase en bloques de 50 para no saturar la red/DB
                print(f"    - Subiendo a Supabase ({len(payload)} registros)...")
                batch_size = 50
                for i in range(0, len(payload), batch_size):
                    batch = payload[i:i+batch_size]
                    supabase.table("knowledge_chunks").upsert(batch).execute()
                    
                # Marcar como procesado solo si todo fue exitoso
                state["procesados"].append(file_hash)
                save_state(state)
                print(f"    - [OK] Completado y guardado!")
                
            except Exception as e:
                logging.error(f"Fallo en {filepath}: {str(e)}")
                print(f"    - ERROR: {e}")
                
            # Garbage collection agresivo para mantener los 8GB a salvo
            del chunks
            gc.collect()
            time.sleep(1) # Pequeña pausa térmica

if __name__ == "__main__":
    BASE_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME"
    print("=====================================================")
    print("   INICIANDO INGESTA Y VECTORIZACIÓN (DIVS-v1)       ")
    print("=====================================================")
    process_pdfs_batch(BASE_DIR)
