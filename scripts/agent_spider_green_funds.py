import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

class GreenFundsSpider:
    def __init__(self):
        # Portales de inteligencia financiera internacional
        self.fuentes = {
            "BID_Turismo": "https://www.iadb.org/es/proyectos",
            "ProInnovate": "https://www.proinnovate.gob.pe/"
        }
        self.headers = {
            'User-Agent': 'Lifextreme_Financial_Spider_v1.0',
        }

    def scrape_fondos(self):
        print("==================================================")
        print("🌍🕷️ INICIANDO AGENTE SPIDER: FONDOS VERDES")
        print("==================================================")
        
        for nombre, url in self.fuentes.items():
            print(f"[*] Escaneando portal: {nombre} ({url})")
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    texto = soup.get_text().lower()
                    
                    keywords = ["bono de carbono", "turismo sostenible", "subvención verde", "fondo no reembolsable"]
                    
                    encontrado = [kw for kw in keywords if kw in texto]
                    if encontrado:
                        print(f"    [+] ¡OPORTUNIDAD DETECTADA! Palabras clave: {', '.join(encontrado)}")
                        print(f"    [+] Enviando alerta financiera a la base de conocimiento...")
                        # Aquí se generaría el JSONL para la cola
                    else:
                        print("    [-] No hay convocatorias verdes activas detectadas hoy en la portada.")
                else:
                    print(f"    ⚠️ Acceso denegado/Error HTTP {response.status_code}")
            except Exception as e:
                print(f"    ⚠️ Fallo de red: {e}")
            
if __name__ == "__main__":
    spider = GreenFundsSpider()
    spider.scrape_fondos()
