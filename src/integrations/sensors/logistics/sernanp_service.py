import sys
import time
import requests
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub

class SernanpService:
    def __init__(self, url):
        self.url = url
        # Palabras clave que denotan crisis en áreas naturales
        self.keywords_riesgo = ["cierre temporal", "suspendido por mantenimiento", "huayco", "deslizamiento bloquea"]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

    def escanear_alertas(self):
        print(f"       -> [SERNANP] 🌳 Escaneando portal oficial EN VIVO: {self.url}...")
        
        try:
            # Petición HTTP Real
            response = requests.get(self.url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                texto_web = soup.get_text().lower()
                
                alerta_detectada = any(kw in texto_web for kw in self.keywords_riesgo)
                
                if alerta_detectada:
                    motivo = next((kw for kw in self.keywords_riesgo if kw in texto_web), "Alerta no especificada")
                    print(f"       -> [SERNANP] 🚨 ALERTA CRÍTICA: Se detectó '{motivo}' en el portal de áreas naturales.")
                    try:
                        evento_validado = LifextremeSchema(
                            source_id="SERNANP",
                            category="RISK", 
                            location={"lat": -13.1631, "lng": -72.5450, "country": "Perú", "region": "Nacional"},
                            payload={"alerta": motivo.title(), "ruta_afectada": "Parques Nacionales"},
                            confidence_score=1.0
                        )
                        pubsub.publish(evento_validado.model_dump_json())
                    except Exception as e:
                        print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")
                else:
                    print(f"       -> [SERNANP] 🟢 Parques Nacionales operando con normalidad (Confirmado por Gobierno Peruano).")
            else:
                 print(f"       -> [SERNANP] ⚠️ Error leyendo web del estado (HTTP {response.status_code}).")
                 
        except Exception as e:
            print(f"       -> [SERNANP] ⚠️ Fallo de conexión real: {e}")
