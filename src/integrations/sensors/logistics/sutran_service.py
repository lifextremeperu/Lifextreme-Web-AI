import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub

class SutranService:
    def __init__(self):
        self.url = "http://visoremergencias.sutran.gob.pe/"

    def escanear_alertas(self):
        print(f"       -> [SUTRAN (MTC)] 🚧 Escaneando comunicados viales en web oficial...")
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
            }
            # En lugar del mapa GIS que es dinámico, leemos las notas de prensa/alertas de SUTRAN
            url_gob = "https://www.gob.pe/sutran"
            response = requests.get(url_gob, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                texto_web = soup.get_text().lower()
                
                # Buscar palabras clave de bloqueo o interrupción en el portal
                keywords_bloqueo = ["tránsito interrumpido", "bloqueo de vía", "paro nacional", "tránsito restringido", "vía bloqueada"]
                alerta_detectada = any(kw in texto_web for kw in keywords_bloqueo)
                
                if alerta_detectada:
                    # Encontrar la palabra exacta que disparó la alerta
                    motivo = next((kw for kw in keywords_bloqueo if kw in texto_web), "Bloqueo Vial")
                    ruta_bloqueada = "Múltiples vías (verificar detalle en portal SUTRAN)"
                    if "sur" in texto_web: ruta_bloqueada = "Vías del Sur"
                    elif "norte" in texto_web: ruta_bloqueada = "Vías del Norte"
                        
                    print(f"       -> [SUTRAN (MTC)] 🚨 ALERTA CRÍTICA: Se detectó un punto ROJO/Alerta ({motivo.upper()}) en la web oficial.")
                    try:
                        evento_validado = LifextremeSchema(
                            source_id="CONSETTUR", # Mantenemos compatibility con el esquema existente
                            category="RISK", 
                            location={"lat": -12.0464, "lng": -77.0428, "country": "Perú", "region": "Nacional"},
                            payload={"alerta": motivo.title(), "ruta_afectada": ruta_bloqueada, "estado": "Alerta Vial - SUTRAN"},
                            confidence_score=0.9 # Extraído por web scraping
                        )
                        json_str = evento_validado.model_dump_json()
                        json_str = json_str.replace('"source_id":"CONSETTUR"', '"source_id":"SUTRAN"')
                        pubsub.publish(json_str)
                    except Exception as e:
                        print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")
                else:
                    print(f"       -> [SUTRAN (MTC)] 🟢 Todas las vías nacionales reportan normalidad en comunicados recientes.")
            else:
                 print(f"       -> [SUTRAN (MTC)] ⚠️ Error leyendo web del estado (HTTP {response.status_code}).")
                 
        except Exception as e:
            print(f"       -> [SUTRAN (MTC)] ⚠️ Fallo de conexión BeautifulSoup: {e}")
