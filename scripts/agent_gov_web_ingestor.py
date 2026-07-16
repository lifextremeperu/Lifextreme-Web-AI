import os
import json
import hashlib
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOWNLOAD_DIR = Path("data/institucional_descargas")
QUEUE_DIR = Path("data/knowledge/queue")

def generate_pseudo_hash(file_path):
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()

def extract_and_queue(file_path, filename):
    print(f"   [+] Extrayendo Conocimiento Web -> {filename}")
    ext = os.path.splitext(file_path)[1].lower()
    file_hash = generate_pseudo_hash(file_path)
    
    # Derivar categoría del nombre
    category = "General"
    if "SUTRAN" in filename: category = "SUTRAN"
    elif "MININTER" in filename: category = "MININTER"
    elif "SERFOR" in filename: category = "SERFOR"
    elif "OSINERGMIN" in filename: category = "OSINERGMIN"
    
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
    print(" 🏛️ AGENTE DE INGESTA GUBERNAMENTAL WEB (Fase 2) ")
    print("===================================================================")
    
    if not DOWNLOAD_DIR.exists():
        print("[-] Directorio de descargas web no encontrado.")
        return
        
    files = list(DOWNLOAD_DIR.glob("*.*"))
    if not files:
        print("[-] No hay archivos descargados en la carpeta.")
        return
        
    processed = 0
    for f in files:
        success = extract_and_queue(str(f), f.name)
        if success:
            processed += 1
            
    print("\n===================================================================")
    print(f" ✅ EXTRACCIÓN A COLA FINALIZADA ({processed} archivos) ")
    print("===================================================================")

if __name__ == "__main__":
    main()
