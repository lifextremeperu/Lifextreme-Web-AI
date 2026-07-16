import os
import json
import time
import hashlib
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

SCAN_RESULTS = Path(r"C:\Users\ASUS\.gemini\antigravity\brain\bd6aa194-c871-4493-8419-804ced4eb3ac\scratch\scan_results.json")
QUEUE_DIR = Path("data/knowledge/queue")

def generate_pseudo_hash(file_path):
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()

def is_valid_ana(path_str):
    path_lower = path_str.lower()
    if "agua" in path_lower or "hidrico" in path_lower or "\\ana\\" in path_lower or "autoridad nacional" in path_lower:
        return True
    return False

def extract_and_queue(file_path, category, filename):
    print(f"   [+] Extrayendo Conocimiento -> {filename} ({category})")
    ext = os.path.splitext(file_path)[1].lower()
    file_hash = generate_pseudo_hash(file_path)
    
    try:
        docs = []
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
            docs = loader.load()
        elif ext in [".md", ".txt"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                class Doc: pass
                d = Doc()
                d.page_content = content
                d.metadata = {"source": file_path}
                docs = [d]
        else:
            return False
            
        if not docs:
            return False
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        splits = text_splitter.split_documents(docs)
        
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        queue_file = QUEUE_DIR / f"{file_hash}.jsonl"
        
        with open(queue_file, "w", encoding="utf-8") as f:
            for i, split in enumerate(splits):
                chunk_data = {
                    "id": f"{file_hash}_{i}",
                    "text": split.page_content,
                    "metadata": {
                        "source": file_path,
                        "filename": filename,
                        "category": category
                    }
                }
                f.write(json.dumps(chunk_data, ensure_ascii=False) + "\n")
                
        print(f"       ✅ Extraídos {len(splits)} fragmentos.")
        return True
        
    except Exception as e:
        print(f"       [-] Error leyendo {filename}: {e}")
        return False

def main():
    print("===================================================================")
    print(" 🏛️ AGENTE DE INGESTA LOCAL GUBERNAMENTAL (Fase 1) ")
    print("===================================================================")
    
    if not SCAN_RESULTS.exists():
        print("[-] scan_results.json no encontrado.")
        return
        
    with open(SCAN_RESULTS, "r", encoding="utf-8") as f:
        inventory = json.load(f)
        
    for cat, files in inventory.items():
        if not files: continue
        
        # Saltamos SUTRAN, OSINERGMIN, MININTER, SERFOR, MINAM, MUNICIPIOS, INDECOPI (serán por web o son muy pocos)
        # Solo inyectamos los que tienen buena data local
        if cat not in ["MEF", "MINCU", "MINSA", "SUNAT", "MINTRA", "POLTUR", "ANA"]:
            continue
            
        print(f"\n[*] PROCESANDO: {cat} ({len(files)} archivos potenciales)")
        processed = 0
        for f_data in files:
            path = f_data["path"]
            filename = f_data["filename"]
            
            if cat == "ANA" and not is_valid_ana(path):
                continue
                
            success = extract_and_queue(path, cat, filename)
            if success:
                processed += 1
                
            # Limite seguro para evitar demoras extremas
            if processed >= 20: 
                print("[!] Límite de 20 documentos por categoría alcanzado.")
                break
                
    print("\n===================================================================")
    print(" ✅ EXTRACCIÓN A COLA FINALIZADA ")
    print("===================================================================")

if __name__ == "__main__":
    main()
