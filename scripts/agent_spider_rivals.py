import os
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data/knowledge/raw/internacional")

class RivalsSpider:
    def __init__(self):
        self.targets = {
            "Chile_Sernatur": "https://www.sernatur.cl/",
            "CostaRica_ICT": "https://www.ict.go.cr/"
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
        os.makedirs(RAW_DIR, exist_ok=True)

    def scrape_regulations(self):
        print("==================================================")
        print("🇨🇱🇨🇷 INICIANDO AGENTE SPIDER: BENCHMARKING (RIVALES)")
        print("==================================================")
        
        for pais, url in self.targets.items():
            print(f"\n[*] Analizando normativas en: {pais} ({url})")
            try:
                response = requests.get(url, headers=self.headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    pdf_links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.endswith('.pdf') and ('aventura' in href.lower() or 'reglamento' in href.lower()):
                            if not href.startswith('http'):
                                href = url + href if href.startswith('/') else url + '/' + href
                            pdf_links.append(href)
                    
                    if pdf_links:
                        print(f"    [+] Se encontraron {len(pdf_links)} normativas potenciales en PDF.")
                        for pdf in pdf_links[:3]: # Limitamos para demostración
                            print(f"        -> Encolando para descarga: {pdf.split('/')[-1]}")
                    else:
                        print("    [-] No se hallaron PDFs de normativas de aventura directamente en portada.")
                        print("    [*] La araña deberá navegar niveles más profundos (Sub-páginas de Transparencia).")
                else:
                    print(f"    ⚠️ Error HTTP {response.status_code}")
            except Exception as e:
                print(f"    ⚠️ Fallo de conexión: {e}")

if __name__ == "__main__":
    spider = RivalsSpider()
    spider.scrape_regulations()
