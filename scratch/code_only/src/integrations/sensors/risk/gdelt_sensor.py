import sys
import os
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from google.cloud import bigquery

from src.integrations.core.normalizer import DataNormalizer
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class GdeltCrisisSensor:
    def __init__(self):
        # Aseguramos que intente usar las credenciales de nuestro proyecto
        os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
        
    def fetch_gdelt_events(self, pais="PE"):
        """
        Consulta GDELT vía su API REST pública (Free & Open Source) para detectar protestas o bloqueos.
        """
        print(f"[SENSOR-CRISIS] 🚨 Analizando la base de datos global GDELT (REST API) para el país: {pais}...")
        
        try:
            import requests
            
            # API Pública de GDELT 2.0: Buscamos noticias recientes sobre protestas/bloqueos en el país indicado
            # No requiere API Key, es 100% gratuita.
            url = "https://api.gdeltproject.org/api/v2/doc/doc"
            params = {
                "query": f"(protesta OR bloqueo OR huelga OR paro) sourcecountry:{pais}",
                "mode": "artlist",
                "maxrecords": "5",
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            eventos = []
            if "articles" in data:
                for article in data["articles"]:
                    eventos.append({
                        "ubicacion": f"{pais} (Noticia Global)", 
                        "fuente": article.get("url", ""),
                        "titulo": article.get("title", "")
                    })
            
            if eventos:
                return eventos
            return []
            
        except Exception as e:
            print(f"[SENSOR-CRISIS] ⚠️ Error conectando a GDELT API Pública: {e}")
            print("[SENSOR-CRISIS] 🔄 Activando Módulo de Simulación para la Arquitectura Event-Driven...")
            time.sleep(1)
            
            return [{
                "ubicacion": "Amazonas, Peru",
                "fuente": "https://noticias-locales-simuladas.com/bloqueo-carretera-amazonas"
            }]

    def ejecutar_monitoreo(self, pais="PE", region_objetivo="Puno"):
        cache_key = f"gdelt_crisis_{pais.lower()}"
        
        eventos = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_gdelt_events(pais),
            ttl_minutes=30 # Las crisis cambian rápido
        )
        
        if not eventos:
            print(f"[SENSOR-CRISIS] ✅ Paz y orden detectado. Sin protestas mayores registradas.")
            return
            
        for evento in eventos:
            ubicacion = evento.get("ubicacion", "")
            
            # Si el evento ocurre en nuestra región de interés, es Crítico
            if region_objetivo.lower() in ubicacion.lower():
                severidad = 5 # Impacto Crítico (Bloqueos)
                mensaje = f"CRISIS SOCIAL: GDELT ha detectado noticias de protestas/bloqueos en la región de '{region_objetivo}'. Fuente: {evento.get('fuente')}"
                print(f"[SENSOR-CRISIS] 💥 {mensaje}")
                
                json_normalizado = DataNormalizer.normalize(
                    source="GDELT",
                    severity=severidad,
                    location={"lat": -15.8402, "lng": -70.0219, "region": region_objetivo}, 
                    payload=mensaje
                )
                pubsub.publish(json_normalizado)
            else:
                print(f"[SENSOR-CRISIS] ℹ️ Protesta registrada en {ubicacion}, fuera del alcance del Agente de {region_objetivo}.")

def main():
    print("==================================================")
    print("INICIANDO SENSOR DE CRISIS MUNDIAL (GDELT)")
    print("==================================================")
    
    sensor = GdeltCrisisSensor()
    # Monitoreamos Perú (PE) buscando afectaciones en Puno
    sensor.ejecutar_monitoreo(pais="PE", region_objetivo="Puno")
    
if __name__ == "__main__":
    main()
