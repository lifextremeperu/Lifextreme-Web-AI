import os
import json
import urllib.request
import ssl
import time
import sys
from pathlib import Path
import random

sys.stdout.reconfigure(encoding='utf-8')
import random

# Deshabilitar verificación SSL
ssl._create_default_https_context = ssl._create_unverified_context

TARGET_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS FALTANTES"
TARGETS_FILE = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\oraculo_targets.json"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
]

def main():
    print("===================================================================")
    print(" 🕷️ AGENTE ARAÑA ORÁCULO (Extracción de Nivel 100) ")
    print("===================================================================")
    
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"[*] Creado directorio de caza: {TARGET_DIR}")
        
    if not os.path.exists(TARGETS_FILE):
        print(f"[-] No se encontró el archivo de objetivos: {TARGETS_FILE}")
        return
        
    with open(TARGETS_FILE, 'r', encoding='utf-8') as f:
        targets = json.load(f)
        
    print(f"[*] Iniciando cacería de {len(targets)} documentos de alta criticidad...\n")
    
    success_count = 0
    
    for doc in targets:
        file_path = os.path.join(TARGET_DIR, doc['filename'])
        url = doc['url']
        
        if os.path.exists(file_path):
            print(f"    [SKIP] Ya existe en caché: {doc['filename']}")
            continue
            
        print(f"    -> [CAZANDO] {doc['filename']} ({doc['entidad_emisora']})")
        
        # Pausa aleatoria antibot
        time.sleep(random.uniform(1.5, 3.5))
        
        try:
            req = urllib.request.Request(
                url, 
                headers={
                    'User-Agent': random.choice(USER_AGENTS),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'
                }
            )
            
            with urllib.request.urlopen(req, timeout=40) as response:
                content_type = response.headers.get('Content-Type', '')
                
                # Check si nos bloquearon devolviendo un HTML de Captcha en vez de PDF
                if 'text/html' in content_type and not url.endswith('.html'):
                    print(f"    [WARNING] Posible bloqueo por Captcha en {doc['entidad_emisora']}. Descargando fallback txt.")
                    fallback_path = file_path.replace(".pdf", ".txt")
                    with open(fallback_path, "w", encoding="utf-8") as f:
                        f.write(f"DOCUMENTO BLOQUEADO POR CAPTCHA/FIREWALL DE {doc['entidad_emisora']}\n")
                        f.write(f"Enlace original: {url}\n")
                        f.write(f"Por favor descargue manualmente este documento para su ingesta.\n")
                    continue

                data = response.read()
                
            with open(file_path, 'wb') as out_file:
                out_file.write(data)
                
            print(f"    [+] ÉXITO: {doc['filename']} descargado ({len(data)/1024/1024:.2f} MB)")
            success_count += 1
            
        except urllib.error.HTTPError as e:
             # Manejar 404s y 403s con un fallback para que la pipeline RAG no se caiga
             print(f"    [-] ERROR HTTP {e.code}: {doc['filename']}. Generando fallback.")
             fallback_path = file_path.replace(".pdf", ".txt")
             with open(fallback_path, "w", encoding="utf-8") as f:
                 f.write(f"ERROR DE DESCARGA (HTTP {e.code}) - {doc['entidad_emisora']}\n")
                 f.write(f"Enlace roto o protegido: {url}\n")
                 f.write(f"Descargar manualmente.\n")
                 
        except Exception as e:
            print(f"    [-] ERROR GENERAL en {doc['filename']}: {e}")
            
    print("\n===================================================================")
    print(f" ✅ CACERÍA COMPLETADA. Archivos obtenidos: {success_count}/{len(targets)}")
    print(rf" 📁 Revisa los archivos en: {TARGET_DIR}")
    print("===================================================================")

if __name__ == "__main__":
    main()
