import os
import sys
import time
import json
import hashlib
from pathlib import Path

DRIVES_TO_SCAN = ["C:\\", "D:\\"]

# Carpetas de sistema que vamos a ignorar por completo para acelerar
IGNORE_DIRS = {
    "Windows", "Program Files", "Program Files (x86)", "AppData", "ProgramData",
    "$Recycle.Bin", "System Volume Information", "node_modules", ".git", "venv",
    "__pycache__", "temp", "tmp", "Cache", "Logs", "Recovery", "Config.Msi", 
    "OneDriveTemp", "Packages"
}

VALID_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".md", ".csv", ".txt"}

CATEGORIES = {
    "Normativas": ["ley", "reglamento", "gercetur", "inacal", "sernanp", "resolucion", "ds", "norma"],
    "Estudios de Mercado": ["perfil", "promperu", "estadistica", "flujo", "demanda", "estudio"],
    "Planes Regionales": ["pertur", "pentur", "plan estrategico", "plan de desarrollo"],
    "Operativa y Tarifarios": ["cotizacion", "tarifario", "itinerario", "costos", "presupuesto", "precio", "pasajeros"],
    "Conocimiento Lifextreme": ["lifextreme", "cixtur", "expedicion", "trekking", "tour", "guia", "protocolo", "montaña", "selva"]
}

OUTPUT_JSON = Path("data/knowledge_inventory.json")

def generate_pseudo_hash(file_path, stat):
    """Genera un hash rápido basado en nombre, tamaño y fecha para no leer todo el archivo"""
    base_str = f"{file_path}_{stat.st_size}_{stat.st_mtime}"
    return hashlib.md5(base_str.encode('utf-8')).hexdigest()

def classify_file(path_str):
    path_lower = path_str.lower()
    for cat_name, keywords in CATEGORIES.items():
        if any(kw in path_lower for kw in keywords):
            return cat_name
    return "General"

def is_valuable(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in VALID_EXTENSIONS:
        return False
    # Verificamos si clasifica en alguna de las categorías
    cat = classify_file(file_path)
    if cat != "General":
        return True
    
    # Algunas palabras clave generales que igual queremos
    general_kws = ["turismo", "cusco", "arequipa", "lima", "agencia", "viaje"]
    if any(kw in file_path.lower() for kw in general_kws):
        return True
        
    return False

def main():
    print("===================================================================")
    print(" 🔎 LIFEXTREME BRAIN: ESCANER V2 (Categorizado y Optimizado) ")
    print("===================================================================")
    
    inventory = {
        "metadata": {
            "scanned_drives": DRIVES_TO_SCAN,
            "total_files": 0,
            "scan_date": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "categories": {cat: [] for cat in list(CATEGORIES.keys()) + ["General"]}
    }
    
    start_time = time.time()
    files_scanned_count = 0
    valuable_count = 0
    
    for drive in DRIVES_TO_SCAN:
        if not os.path.exists(drive):
            print(f"[-] El disco {drive} no existe o no está accesible. Saltando.")
            continue
            
        print(f"\n[*] INICIANDO ESCANEO EN DISCO {drive}")
        print("[*] Esto puede tomar varios minutos. Por favor, espera...\n")
        
        for root, dirs, files in os.walk(drive):
            # Ignorar carpetas ocultas y de sistema
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                files_scanned_count += 1
                
                # Imprimir avance para que el usuario no crea que se congeló
                if files_scanned_count % 10000 == 0:
                    print(f"   ... Analizados {files_scanned_count} archivos globales ...")
                
                full_path = os.path.join(root, file)
                
                # Excluir la carpeta temporal de Lifextreme-Web-AI/data si estamos guardando ahí
                if "knowledge_inventory.json" in full_path:
                    continue
                    
                if is_valuable(full_path):
                    try:
                        stat = os.stat(full_path)
                        # Omitir archivos extremadamente grandes (+50MB) para no atascar al RAG
                        if stat.st_size > 50 * 1024 * 1024:
                            continue
                            
                        cat = classify_file(full_path)
                        pseudo_hash = generate_pseudo_hash(full_path, stat)
                        
                        file_data = {
                            "path": full_path,
                            "filename": file,
                            "size_bytes": stat.st_size,
                            "hash": pseudo_hash,
                            "extension": os.path.splitext(file)[1].lower()
                        }
                        
                        inventory["categories"][cat].append(file_data)
                        inventory["metadata"]["total_files"] += 1
                        valuable_count += 1
                        
                        # Mostrar archivos clave en vivo
                        if valuable_count % 50 == 0:
                            print(f"[+] ¡Encontrado! [{cat}] -> {file}")
                            
                    except Exception:
                        # Archivos bloqueados por el sistema, saltar
                        continue
                        
    # Resumen final
    print("\n===================================================================")
    print(" 📂 ESCANEO COMPLETADO ")
    print("===================================================================")
    elapsed = time.time() - start_time
    print(f"Tiempo total: {elapsed:.2f} segundos")
    print(f"Archivos evaluados: {files_scanned_count}")
    print(f"Archivos VALIOSOS encontrados: {valuable_count}")
    
    print("\n--- Desglose por Categorías ---")
    for cat, files in inventory["categories"].items():
        print(f"- {cat}: {len(files)} archivos")
        
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)
        
    print(f"\n[+] Inventario guardado en: {OUTPUT_JSON.absolute()}")
    print("===================================================================")

if __name__ == "__main__":
    main()
