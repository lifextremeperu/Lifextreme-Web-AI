import os
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

RAW_DIR = Path("data/knowledge/raw/comunitario")

class ComunidadesSpider:
    def __init__(self):
        # Portales del estado y repositorios de investigación
        self.sources = {
            "Ley_Comunidades": "https://www.gob.pe/busquedas?institucion=&razon_social=&tipo_norma=ley",
            "MINCETUR_Turismo_Comunitario": "https://www.gob.pe/mincetur"
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }
        os.makedirs(RAW_DIR, exist_ok=True)

    def scrape_comunidades(self):
        print("==================================================")
        print("🤝🏞️ INICIANDO AGENTE SPIDER: TURISMO COMUNITARIO")
        print("==================================================")
        
        for fuente, url in self.sources.items():
            print(f"\n[*] Buscando PDFs oficiales en: {fuente} ({url})")
            try:
                response = requests.get(url, headers=self.headers, timeout=15)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    pdf_links = []
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        texto = link.get_text().lower()
                        
                        # Buscamos enlaces a PDFs que hablen de comunidades o turismo rural
                        if href.endswith('.pdf') or 'comunidad' in texto or 'comunitario' in texto:
                            if not href.startswith('http'):
                                href = "https://www.gob.pe" + href if href.startswith('/') else "https://www.gob.pe/" + href
                            pdf_links.append(href)
                            
                    if pdf_links:
                        print(f"    [+] Se encontraron {len(pdf_links)} documentos/leyes sobre comunidades.")
                        for i, pdf_url in enumerate(pdf_links[:3]):
                            print(f"        -> Descargando: {pdf_url}")
                            try:
                                pdf_resp = requests.get(pdf_url, headers=self.headers, timeout=20)
                                if pdf_resp.status_code == 200:
                                    # Generar nombre limpio
                                    file_name = pdf_url.split('/')[-1]
                                    if not file_name.endswith('.pdf'): file_name += f"_comunidad_{i}.pdf"
                                    
                                    file_path = RAW_DIR / file_name
                                    with open(file_path, 'wb') as f:
                                        f.write(pdf_resp.content)
                                    print(f"           ✅ Guardado en: {file_path}")
                                else:
                                    print(f"           ⚠️ Falló descarga HTTP {pdf_resp.status_code}")
                            except Exception as e:
                                print(f"           ⚠️ Error al descargar PDF: {e}")
                    else:
                        print("    [-] No se encontraron PDFs comunitarios en esta primera búsqueda.")
                        print("    [*] Expandiendo algoritmos de búsqueda a repositorios académicos (ALICIA/CONCYTEC).")
                else:
                    print(f"    ⚠️ Error HTTP {response.status_code}")
            except Exception as e:
                print(f"    ⚠️ Error de conexión: {e}")

if __name__ == "__main__":
    spider = ComunidadesSpider()
    spider.scrape_comunidades()
