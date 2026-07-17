import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.integrations.core.pubsub_client import pubsub
from src.models.lifextreme_schema import LifextremeSchema

class TravelAdvisorySpider:
    def __init__(self):
        # US State Department Official RSS Feed for Travel Advisories
        self.rss_url = "https://travel.state.gov/_res/rss/TAsTWs.xml"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }

    def fetch_advisories(self):
        print("==================================================")
        print("🌎🕷️ INICIANDO AGENTE: TRAVEL ADVISORY (USA)")
        print("==================================================")
        print(f"[*] Escaneando alertas de viaje globales desde: {self.rss_url}")
        
        try:
            response = requests.get(self.rss_url, headers=self.headers, timeout=15)
            if response.status_code == 200:
                # Usamos parser XML porque es un RSS Feed
                soup = BeautifulSoup(response.content, 'xml')
                items = soup.find_all('item')
                
                peru_found = False
                for item in items:
                    title = item.title.text if item.title else ""
                    description = item.description.text if item.description else ""
                    link = item.link.text if item.link else ""
                    
                    # Buscamos específicamente a Perú
                    if "peru" in title.lower() or "peru" in description.lower():
                        peru_found = True
                        print(f"    [!] ¡ALERTA INTERNACIONAL DETECTADA PARA PERÚ!")
                        print(f"        -> Título: {title}")
                        
                        # Determinar severidad basada en el texto (Nivel 1 a 4)
                        severity = 1
                        if "level 4" in title.lower() or "do not travel" in title.lower(): severity = 4
                        elif "level 3" in title.lower() or "reconsider travel" in title.lower(): severity = 3
                        elif "level 2" in title.lower() or "exercise increased caution" in title.lower(): severity = 2
                        
                        try:
                            evento_validado = LifextremeSchema(
                                source_id="US_STATE_DEPT",
                                category="MARKET", 
                                location={"lat": -9.19, "lng": -75.015, "country": "Perú", "region": "Nacional"},
                                payload={"alerta": title, "nivel": f"Nivel {severity}", "enlace": link},
                                confidence_score=1.0
                            )
                            pubsub.publish(evento_validado.model_dump_json())
                            print("    [+] Alerta enviada a la red neuronal para estrategia de mitigación.")
                        except Exception as e:
                            print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")
                
                if not peru_found:
                    print("    [-] Ninguna alerta nueva o crítica para Perú en el feed oficial de EE.UU.")
            else:
                print(f"    ⚠️ Error leyendo RSS de USA (HTTP {response.status_code}).")
                
        except Exception as e:
            print(f"    ⚠️ Fallo de conexión: {e}")

if __name__ == "__main__":
    spider = TravelAdvisorySpider()
    spider.fetch_advisories()
