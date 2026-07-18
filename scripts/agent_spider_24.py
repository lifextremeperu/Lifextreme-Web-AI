import os
import sys
import time
import requests
import ssl
from pathlib import Path
import json
from bs4 import BeautifulSoup
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')
ssl._create_default_https_context = ssl._create_unverified_context

TARGET_DIR = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO\GOREs")
METADATA_FILE = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\gov_tupa_metadata.json")

DEPARTAMENTOS = [
    "Amazonas", "Ancash", "Apurimac", "Arequipa", "Ayacucho", "Cajamarca", 
    "Callao", "Cusco", "Huancavelica", "Huanuco", "Ica", "Junin", 
    "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", 
    "Moquegua", "Pasco", "Piura", "Puno", "San Martin", "Tacna", "Tumbes"
]

def search_ddg_lite(query):
    """Busca en DuckDuckGo HTML Lite (sin JS, puro HTML)."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    url = f"https://lite.duckduckgo.com/lite/"
    data = {'q': query}
    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        links = []
        for a in soup.find_all('a', class_='result-url'):
            href = a.get('href')
            if href:
                links.append(href)
        return links
    except Exception as e:
        print(f"    [-] Error en DDG Lite: {e}")
        return []

def search_tupa_pdf(departamento):
    """Busca el TUPA oficial del departamento."""
    print(f"\n[*] Buscando TUPA DIRCETUR/GERCETUR para: {departamento}...")
    
    # 1. Búsqueda estricta PDF + GOB.PE
    query1 = f"TUPA turismo gobierno regional {departamento} ext:pdf site:gob.pe"
    links = search_ddg_lite(query1)
    
    for link in links:
        if '.pdf' in link.lower() and '.gob.pe' in link.lower():
            print(f"    [+] Link oficial PDF encontrado: {link}")
            return link
            
    # 2. Búsqueda amplia
    query2 = f"TUPA turismo gobierno regional {departamento} pdf"
    links2 = search_ddg_lite(query2)
    
    for link in links2:
        if '.pdf' in link.lower():
            print(f"    [+] Link genérico PDF encontrado: {link}")
            return link
            
    print(f"    [-] No se encontró un PDF directo en buscadores.")
    return None

def download_pdf(url, filepath):
    """Descarga el PDF simulando un navegador humano."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=20, verify=False)
        if response.status_code != 200:
            print(f"    [-] Status {response.status_code} al descargar.")
            return False
            
        content_type = response.headers.get('Content-Type', '').lower()
        if 'html' in content_type:
            print(f"    [-] El servidor devolvió HTML en vez de PDF (Falsa redirección).")
            return False
            
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"    [ERROR] Fallo de conexión: {e}")
        return False

def main():
    print("===================================================================")
    print(" 🕷️ AGENTE ARAÑA TUPA (24 DEPARTAMENTOS - ESCALA NACIONAL) ")
    print("===================================================================")
    
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Cargar metadatos existentes para no re-descargar
    metadata = []
    if METADATA_FILE.exists():
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except:
            metadata = []
            
    descargados = [m['entidad_emisora'] for m in metadata]
    
    success_count = 0
    fail_count = 0
    
    for depto in DEPARTAMENTOS:
        entidad = f"GERCETUR_{depto.upper()}"
        filename = f"GERCETUR_TUPA_{depto}.pdf"
        filepath = TARGET_DIR / filename
        
        if filepath.exists() and filepath.stat().st_size > 10000:
            print(f"\n[*] {depto}: Ya existe un PDF válido en disco. [SKIP]")
            continue
            
        pdf_url = search_tupa_pdf(depto)
        if pdf_url:
            print(f"    -> Intentando descarga (simulando humano)...")
            if download_pdf(pdf_url, filepath):
                print(f"    [✅] ÉXITO: {filename} descargado ({(filepath.stat().st_size/1024):.1f} KB).")
                success_count += 1
                
                # Actualizar metadata si no existe
                if entidad not in descargados:
                    metadata.append({
                        "filename": filename,
                        "url": pdf_url,
                        "entidad_emisora": entidad,
                        "nivel_legal": "TUPA",
                        "jurisdiccion": f"Regional {depto}",
                        "titulo": f"TUPA Oficial del Gobierno Regional de {depto}"
                    })
            else:
                print(f"    [❌] FAIL: No se pudo descargar el archivo.")
                fail_count += 1
        else:
            print(f"    [❌] FAIL: Sin URL encontrada.")
            fail_count += 1
            
        time.sleep(3) # Pausa estratégica para evitar ban de DuckDuckGo
        
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    print("\n===================================================================")
    print(f" ✅ PROCESO NACIONAL COMPLETADO.")
    print(f"    - Éxitos (Nuevos): {success_count}")
    print(f"    - Fallidos / Ocultos por GORE: {fail_count}")
    print("===================================================================")

if __name__ == "__main__":
    main()
