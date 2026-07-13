import sys
import os
import json
import time
from pathlib import Path

# Forzar salida en UTF-8 para evitar errores con emojis en Windows CMD
sys.stdout.reconfigure(encoding='utf-8')

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

INVENTORY_FILE = Path("data/knowledge_inventory.json")
STATE_FILE = Path("data/ingestion_state_v2.json")
QUEUE_DIR = Path("data/knowledge/queue")

def load_inventory():
    if not INVENTORY_FILE.exists():
        return None
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_state():
    if not STATE_FILE.exists():
        return {"procesados": []}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def extract_and_queue_file(file_data):
    """
    Lee el archivo (PDF/MD/TXT), lo fragmenta inteligentemente y lo guarda
    en una cola local para ser inyectado por lotes a Qdrant sin colapsar el sistema.
    """
    path = file_data["path"]
    filename = file_data["filename"]
    ext = file_data["extension"]
    
    print(f"   [+] Extrayendo Conocimiento -> {filename}")
    
    try:
        docs = []
        if ext == ".pdf":
            loader = PyPDFLoader(path)
            docs = loader.load()
        elif ext in [".md", ".txt"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                # Fake a Document object structure
                class Doc: pass
                d = Doc()
                d.page_content = content
                d.metadata = {"source": path}
                docs = [d]
        else:
            # Skip for now
            return True
            
        if not docs:
            return True
            
        # Splitter semántico
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        splits = text_splitter.split_documents(docs)
        
        # Guardar en la cola
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        queue_file = QUEUE_DIR / f"{file_data['hash']}.jsonl"
        
        with open(queue_file, "w", encoding="utf-8") as f:
            for i, split in enumerate(splits):
                chunk_data = {
                    "id": f"{file_data['hash']}_{i}",
                    "text": split.page_content,
                    "metadata": {
                        "source": path,
                        "filename": filename,
                        "category": file_data.get("category", "General")
                    }
                }
                f.write(json.dumps(chunk_data, ensure_ascii=False) + "\n")
                
        print(f"       ✅ Extraídos {len(splits)} fragmentos listos para vectorización.")
        return True
        
    except Exception as e:
        print(f"       [-] Error leyendo {filename}: {e}")
        return False

def main():
    print("===================================================================")
    print(" 🧠 LIFEXTREME BRAIN: ORQUESTADOR DE EXTRACCIÓN Y COLA ")
    print("===================================================================")
    
    inventory = load_inventory()
    if not inventory:
        print("No se encontró el inventario.")
        return
        
    state = load_state()
    procesados = set(state["procesados"])
    
    total_processed = 0
    total_skipped = 0
    
    # Prioridad
    priority_order = ["Planes Regionales", "Normativas", "Estudios de Mercado", "Operativa y Tarifarios", "Conocimiento Lifextreme"]
    
    for category in priority_order:
        if category not in inventory["categories"]: continue
        
        files = inventory["categories"][category]
        if not files: continue
        
        print(f"\n[*] PROCESANDO CATEGORÍA: {category.upper()} ({len(files)} archivos)")
        
        for file_data in files:
            file_data["category"] = category
            file_hash = file_data["hash"]
            
            if file_hash in procesados:
                total_skipped += 1
                continue
                
            success = extract_and_queue_file(file_data)
            if success:
                procesados.add(file_hash)
                state["procesados"] = list(procesados)
                save_state(state)
                total_processed += 1
                
            # LIMITE DE SEGURIDAD PARA MODO NOCTURNO (Procesar 100 por lote para no colapsar memoria)
            if total_processed >= 100:
                print("\n[!] Límite de lote nocturno alcanzado (100 documentos).")
                print("[!] El script maestro tomará el control para vaciar la cola.")
                break
        if total_processed >= 100:
            break

    print("\n===================================================================")
    print(" ✅ FASE DE EXTRACCIÓN FINALIZADA ")
    print("===================================================================")
    print(f"Archivos procesados y encolados: {total_processed}")
    print(f"Archivos saltados (ya procesados): {total_skipped}")
    print("Los fragmentos están en data/knowledge/queue/ listos para Qdrant.")
    print("===================================================================")

if __name__ == "__main__":
    main()
