import os
import time

# Configuraciones del escáner
DRIVES_TO_SCAN = ["C:\\Users\\ASUS\\OneDrive\\VARIOS\\Documentos", "D:\\"] # Rutas base a escanear
# Extensiones valiosas para la IA
VALID_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".md", ".csv"}
# Palabras clave en el nombre del archivo o carpeta que indican valor para Lifextreme
KEYWORDS = [
    "turismo", "tour", "expedicion", "trekking", "itinerario", "cotizacion", 
    "costos", "marketing", "agencia", "pasajeros", "mincetur", "reglamento", 
    "guia", "protocolo", "lifextreme", "cixtur", "cusco", "arequipa", "lima"
]
# Carpetas a ignorar (sistemas, basura, etc.)
IGNORE_DIRS = [
    "AppData", "Windows", "Program Files", "Program Files (x86)", 
    "node_modules", ".git", "venv", "__pycache__", "temp", "tmp"
]

OUTPUT_FILE = "reporte_archivos_valiosos.txt"

def is_valuable(file_path):
    """Determina si un archivo es valioso basado en su extensión y palabras clave."""
    path_lower = file_path.lower()
    
    # 1. Verificar extensión
    ext = os.path.splitext(path_lower)[1]
    if ext not in VALID_EXTENSIONS:
        return False
        
    # 2. Verificar palabras clave en el path o nombre
    for keyword in KEYWORDS:
        if keyword in path_lower:
            return True
            
    return False

def scan_drives():
    print("===================================================================")
    print(" 🔎 INICIANDO ESCÁNER INTELIGENTE DE ARCHIVOS LIFEXTREME ")
    print("===================================================================")
    
    valuable_files = []
    start_time = time.time()
    
    for drive in DRIVES_TO_SCAN:
        if not os.path.exists(drive):
            print(f"[-] La ruta {drive} no existe o no es accesible.")
            continue
            
        print(f"[*] Escaneando ruta: {drive} (Esto tomará unos minutos)...")
        
        for root, dirs, files in os.walk(drive):
            # Ignorar carpetas de sistema o pesadas
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
            
            for file in files:
                full_path = os.path.join(root, file)
                if is_valuable(full_path):
                    valuable_files.append(full_path)
                    
    # Guardar reporte
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("=== REPORTE DE ARCHIVOS POTENCIALES PARA LA IA ===\n")
            f.write(f"Total encontrados: {len(valuable_files)}\n\n")
            for vf in valuable_files:
                f.write(f"{vf}\n")
    except Exception as e:
        print(f"[-] Error guardando reporte: {e}")
        
    elapsed = round(time.time() - start_time, 2)
    print("===================================================================")
    print(f" ✅ ESCANEO COMPLETADO EN {elapsed} SEGUNDOS.")
    print(f" 📂 Se encontraron {len(valuable_files)} archivos de alto valor comercial.")
    print(f" 📄 Revisa el archivo: {OUTPUT_FILE} en esta misma carpeta.")
    print("===================================================================")

if __name__ == "__main__":
    scan_drives()
