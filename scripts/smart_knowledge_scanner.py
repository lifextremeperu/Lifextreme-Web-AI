import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Palabras clave relacionadas a Lifextreme y Turismo
KEYWORDS = [
    "turismo", "mincetur", "promperu", "viaje", "travel", "itinerario", 
    "tour", "hotel", "guia", "legal", "reglamento", "contrato", "cusco", 
    "peru", "sutran", "sernanp", "aventura", "glamping", "lifextreme",
    "paquete", "ruta", "montaña", "andes", "amazonas", "reserva"
]

# Extensiones de documentos útiles para la IA
VALID_EXTS = [".pdf", ".docx", ".md", ".xlsx", ".pptx", ".txt"]

# Carpetas a ignorar para no perder tiempo ni leer archivos de sistema/código
IGNORE_DIRS = {
    "Windows", "Program Files", "Program Files (x86)", "AppData", "node_modules", 
    ".git", "dist", "build", "venv", "__pycache__", "$RECYCLE.BIN", "System Volume Information",
    ".vscode", "Cache", "Temp", "ProgramData"
}

def is_relevant(filepath):
    path_lower = filepath.lower()
    # Verifica si tiene alguna palabra clave en la ruta o nombre de archivo
    for kw in KEYWORDS:
        if kw in path_lower:
            return True
    return False

def scan_directory(base_dir):
    print(f"[*] Iniciando escaneo en: {base_dir}")
    found_files = []
    
    try:
        for root, dirs, files in os.walk(base_dir):
            # Filtrar directorios a ignorar
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in VALID_EXTS:
                    full_path = os.path.join(root, f)
                    if is_relevant(full_path):
                        # Evitar los que ya procesamos recientemente en Lifextreme-Web-AI
                        if "Lifextreme-Web-AI\\data\\knowledge" in full_path or "Lifextreme-Web-AI\\data\\obsidian_vault" in full_path:
                            continue
                            
                        # Obtener tamaño
                        try:
                            size_mb = os.path.getsize(full_path) / (1024 * 1024)
                            found_files.append({
                                "path": full_path,
                                "size_mb": round(size_mb, 2),
                                "ext": ext
                            })
                        except:
                            pass
    except Exception as e:
        print(f"[-] Error accediendo a {base_dir}: {e}")
        
    return found_files

def main():
    # Solo buscar en la carpeta de usuario en C: para evitar archivos de Windows, y todo D:
    search_paths = [
        r"C:\Users\ASUS",
        r"D:\\"
    ]
    
    all_results = []
    for sp in search_paths:
        if os.path.exists(sp):
            all_results.extend(scan_directory(sp))
            
    # Ordenar por tamaño descendente
    all_results.sort(key=lambda x: x["size_mb"], reverse=True)
    
    # Agrupar por categoría basada en la ruta
    report = "# 🗺️ Radar de Conocimiento: Archivos Potenciales para Lifextreme AI\n\n"
    report += "Se escanearon los discos C: y D: buscando documentos con palabras clave estratégicas (Turismo, Mincetur, Contratos, etc.) que no estén actualmente en la base de datos de Qdrant.\n\n"
    
    # Top 50 archivos más grandes/importantes
    report += "## 📑 Top 50 Archivos Más Relevantes Encontrados\n"
    report += "| Archivo | Tamaño (MB) | Ruta Completa |\n"
    report += "|---|---|---|\n"
    
    for item in all_results[:50]:
        filename = os.path.basename(item["path"])
        report += f"| **{filename}** | {item['size_mb']} MB | `{item['path']}` |\n"
        
    report += f"\n**Total de archivos relevantes encontrados en toda la PC:** {len(all_results)}\n"
    
    with open(r"C:\Users\ASUS\.gemini\antigravity\brain\53a890c3-72f0-4498-92dd-9eec52613903\artifacts\radar_conocimiento.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\n[+] Escaneo finalizado. Se encontraron {len(all_results)} archivos.")
    print("Reporte generado en artifacts/radar_conocimiento.md")

if __name__ == "__main__":
    main()
