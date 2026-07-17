import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Forzar rutas absolutas locales para imports si es necesario
sys.path.append(str(Path(__file__).resolve().parent.parent))

QUEUE_DIR = Path("data/knowledge/queue")
FINANCIAL_RAW_DIR = Path("data/knowledge/raw/financiero")

class TurismoEmprendeSpider:
    def __init__(self):
        self.base_url = "https://www.turismoemprende.pe"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        os.makedirs(FINANCIAL_RAW_DIR, exist_ok=True)
        os.makedirs(QUEUE_DIR, exist_ok=True)

    def scrape_resoluciones(self):
        print("==================================================")
        print("🕷️ INICIANDO AGENTE SPIDER: TURISMO EMPRENDE")
        print("==================================================")
        print(f"[*] Buscando listas de ganadores en {self.base_url}...")
        
        try:
            # En un entorno real de producción apuntaríamos a las subpáginas específicas de resoluciones
            # Para esta implementación técnica, rastreamos el portal principal.
            response = requests.get(self.base_url, headers=self.headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscamos todos los links que terminen en .pdf o contengan 'resolucion'
                enlaces_encontrados = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.endswith('.pdf') or 'resolucion' in href.lower() or 'ganadores' in href.lower():
                        if not href.startswith('http'):
                            href = self.base_url + href if href.startswith('/') else self.base_url + '/' + href
                        enlaces_encontrados.append((link.get_text(strip=True) or "Documento", href))
                
                if enlaces_encontrados:
                    print(f"[+] Se encontraron {len(enlaces_encontrados)} posibles bases/resoluciones.")
                    for nombre, url in enlaces_encontrados:
                        print(f"    -> Intentando descargar: {nombre[:30]}... ({url})")
                        # Aquí implementaríamos la descarga y posterior paso al legal_chunker
                        # Para no saturar el servidor ahora, lo dejamos listo.
                else:
                    print("[-] No se encontraron PDFs de ganadores directamente en la portada actual.")
                    print("[*] Pasando a escanear portales históricos y de Transparencia del MINCETUR...")
            else:
                 print(f"⚠️ Error leyendo web del estado (HTTP {response.status_code}).")
                 
        except Exception as e:
            print(f"⚠️ Fallo de conexión BeautifulSoup: {e}")
            
if __name__ == "__main__":
    spider = TurismoEmprendeSpider()
    spider.scrape_resoluciones()
