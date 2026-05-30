import sys
import time
import requests
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub

class ConsetturService:
    def __init__(self, url):
        self.url = url
        self.keywords_riesgo = ["huelga de transportistas", "suspensión de operaciones", "bloqueo en la vía"]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

    def escanear_alertas(self):
        print(f"       -> [CONSETTUR] 🚌 Escaneando portal oficial EN VIVO: {self.url}...")
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                html_real = response.text.lower()
                
                alerta_detectada = any(kw in html_real for kw in self.keywords_riesgo)
                
                if alerta_detectada:
                    print(f"       -> [CONSETTUR] 🚨 ALERTA CRÍTICA: Se detectó un bloqueo real en la web de buses.")
                    try:
                        evento_validado = LifextremeSchema(
                            source_id="CONSETTUR",
                            category="RISK", 
                            location={"lat": -13.1631, "lng": -72.5450, "country": "Perú", "region": "Machu Picchu"},
                            payload={"alerta": "Suspensión real de buses detectada", "ruta_afectada": "Aguas Calientes - Machu Picchu"},
                            confidence_score=1.0
                        )
                        pubsub.publish(evento_validado.model_dump_json())
                    except Exception as e:
                        print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")
                else:
                    print(f"       -> [CONSETTUR] 🟢 Buses a Machu Picchu operando con normalidad (Venta abierta).")
            else:
                 print(f"       -> [CONSETTUR] ⚠️ Error leyendo web (HTTP {response.status_code}).")
                 
        except Exception as e:
            print(f"       -> [CONSETTUR] ⚠️ Fallo de conexión real: {e}")
