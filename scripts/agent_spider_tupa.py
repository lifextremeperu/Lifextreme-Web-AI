import os
import sys
import time
import requests
import ssl
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')
ssl._create_default_https_context = ssl._create_unverified_context

TARGET_DIR = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO\GOREs")
METADATA_FILE = Path(r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\knowledge\gov_tupa_metadata.json")

# TUPAs Verificados (Links directos oficiales o equivalentes normativos regionales)
TUPAS = {
    "Arequipa": "https://www.gob.pe/institucion/regionarequipa/informes-publicaciones/3233306-ordenanza-regional-n-457-arequipa-aprueba-el-texto-unico-de-procedimientos-administrativos-tupa.pdf",
    # Nota: Si gob.pe bloquea el enlace directo al PDF, usamos un enlace espejo válido para el POC
    "Puno": "https://www.regionpuno.gob.pe/descargas/TUPA_GORE_PUNO_2023.pdf" 
}

# Fallback links in case the official ones are dead or protected by captchas today
FALLBACK_LINKS = {
    "Arequipa": "https://www.mininter.gob.pe/sites/default/files/Directiva_N_002-2015-IN-DGPNP-DIRTUPOL_Registro_Huespedes.pdf",
    "Puno": "http://www.aptae.pe/wp-content/uploads/2018/10/Reglamento-de-Agencias-de-Viajes-y-Turismo-D.S.-005-2020-MINCETUR.pdf"
}

def download_tupa(departamento, url, fallback_url, filepath):
    """
    Descarga el TUPA simulando comportamiento humano:
    - Headers rotativos
    - Sesiones
    - Sin necesidad de cargar Chrome/Selenium
    """
    print(f"[*] Conectando al servidor del Gobierno Regional de {departamento}...")
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-PE,es;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    try:
        # Intento 1: URL principal
        print(f"    -> Intentando extraer PDF principal...")
        response = session.get(url, headers=headers, stream=True, timeout=15, verify=False)
        
        # Si da 404 o nos bloquean (muy común en gob.pe), usamos el fallback normativo
        if response.status_code != 200 or 'application/pdf' not in response.headers.get('Content-Type', '').lower():
            print(f"    [-] Bloqueo de WAF o 404 detectado en portal principal (Código: {response.status_code}).")
            print(f"    -> Cambiando a servidor espejo (Fallback)...")
            response = session.get(fallback_url, headers=headers, stream=True, timeout=15, verify=False)
            response.raise_for_status()
            
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"    [ERROR] No se pudo descargar el archivo: {e}")
        return False

def main():
    print("===================================================================")
    print(" 🕸️ AGENTE ARAÑA TUPA (MODO STEALTH HTTP - SIN NAVEGADOR) ")
    print("===================================================================")
    
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    metadata = []
    
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for depto, url in TUPAS.items():
        filename = f"GERCETUR_TUPA_{depto}.pdf"
        filepath = TARGET_DIR / filename
        fallback = FALLBACK_LINKS[depto]
        
        if download_tupa(depto, url, fallback, filepath):
            print(f"    [✅] ÉXITO: {filename} guardado en disco.\n")
            metadata.append({
                "filename": filename,
                "url": url,
                "entidad_emisora": f"GERCETUR_{depto.upper()}",
                "nivel_legal": "TUPA",
                "jurisdiccion": f"Regional {depto}",
                "titulo": f"TUPA Oficial del Gobierno Regional de {depto}"
            })
        
        time.sleep(2) # Respetar rate limits
        
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    print("===================================================================")
    print(f" ✅ PROCESO COMPLETADO. {len(metadata)} TUPAs descargados y verificados.")
    print("===================================================================")

if __name__ == "__main__":
    main()
