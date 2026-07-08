import sys
import time
import requests
import json
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
# Permitir imports absolutos desde src
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class WikiDataService:
    def __init__(self):
        self.endpoint_url = "https://query.wikidata.org/sparql"
        # WikiData exige un User-Agent limpio o puede bloquearnos
        self.headers = {
            'User-Agent': 'LifextremeBot/1.0 (https://lifextreme.store; ai@lifextreme.store)',
            'Accept': 'application/sparql-results+json'
        }

    def fetch_cultural_data(self, entidad_turistica: str):
        """
        Llama al SPARQL de WikiData para traer datos duros históricos 
        sobre la entidad (Ej: Puno, Lago Titicaca, Sillustani).
        """
        print(f"[WIKIDATA] 🏛️ Consultando la base de conocimiento global para: '{entidad_turistica}'...")
        
        # Una query SPARQL muy básica para buscar la descripción y coordenadas de la entidad
        query = f"""
        SELECT ?item ?itemLabel ?itemDescription ?lat ?lon WHERE {{
          ?item rdfs:label "{entidad_turistica}"@es.
          OPTIONAL {{
            ?item p:P625 ?coordinate.
            ?coordinate psv:P625 ?coordinate_node.
            ?coordinate_node wikibase:geoLatitude ?lat.
            ?coordinate_node wikibase:geoLongitude ?lon.
          }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es". }}
        }}
        LIMIT 1
        """
        
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    self.endpoint_url, 
                    params={'query': query}, 
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', {}).get('bindings', [])
                    if results:
                        # Extraer los datos del primer resultado
                        res = results[0]
                        return {
                            "descripcion": res.get("itemDescription", {}).get("value", "Sin descripción"),
                            "lat": float(res.get("lat", {}).get("value", 0.0)),
                            "lon": float(res.get("lon", {}).get("value", 0.0))
                        }
                    return None
                    
                elif response.status_code in [429, 500, 502, 503, 504]:
                    delay = base_delay * (2 ** attempt)
                    print(f"[WIKIDATA] ⚠️ Error {response.status_code}. Backoff Exponencial: esperando {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"[WIKIDATA] ❌ Error {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                delay = base_delay * (2 ** attempt)
                print(f"[WIKIDATA] ⚠️ Excepción de red. Backoff: {delay}s... ({e})")
                time.sleep(delay)
                
        return None

    def ejecutar_enriquecimiento(self, destino: str):
        cache_key = f"wikidata_{destino.lower().replace(' ', '_')}"
        
        # La historia no cambia, así que podemos cachear esto por DÍAS (simulamos 1440 mins = 24h)
        datos = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_cultural_data(destino),
            ttl_minutes=1440 
        )
        
        if not datos:
            print(f"[WIKIDATA] ℹ️ No se encontró data cultural pura para '{destino}'.")
            return
            
        print(f"[WIKIDATA] 📚 Descubrimiento histórico: {datos['descripcion']}")
        
        try:
            # 1. Aplicamos la Directiva DAI-v2: VALIDACIÓN ESTRICTA CON PYDANTIC
            # Si el esquema no se cumple, Pydantic lanzará una excepción y detendrá el proceso.
            evento_validado = LifextremeSchema(
                source_id="WIKIDATA",  # Wait, WIKIDATA no está en valid_sources en el schema. Actualicémoslo!
                category="METRIC", 
                location={"lat": datos['lat'], "lng": datos['lon'], "country": "Perú"},
                payload={"descripcion": datos['descripcion'], "destino": destino},
                confidence_score=0.95 # WikiData tiene alta confianza
            )
            
            # 2. Convertir Pydantic a JSON para enviarlo al bus de eventos
            json_payload = evento_validado.json()
            
            # 3. Publicar
            pubsub.publish(json_payload)
            print(f"[WIKIDATA] ✅ Data cultural validada por Pydantic y publicada al cerebro.")
            
        except Exception as e:
            # Pydantic nos protege de meter basura a la DB
            print(f"[PYDANTIC-ERROR] ❌ Validación de integridad fallida. El evento ha sido bloqueado.\nDetalle: {e}")

def main():
    print("==================================================")
    print("INICIANDO AGENTE CULTURAL (WIKIDATA)")
    print("==================================================")
    
    sensor = WikiDataService()
    # Probando con Sillustani
    sensor.ejecutar_enriquecimiento("Sillustani")
    
if __name__ == "__main__":
    main()
