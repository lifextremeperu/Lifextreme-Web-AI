import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class PromperuService:
    def __init__(self):
        # Endpoint de la API CKAN de Datos Abiertos del Perú (Portal Nacional)
        self.ckan_url = "https://www.datosabiertos.gob.pe/api/3/action/datastore_search"
        self.dataset_id_vuelos = "dataset-mincetur-llegadas-nacionales" # ID ficticio representativo

    def fetch_datos_abiertos(self, region: str):
        """
        Descarga en Lote (Batch) las estadísticas de arribos desde MINCETUR/PROMPERÚ.
        En producción usaría pd.read_csv o la API CKAN.
        """
        print(f"[PROMPERÚ] 🇵🇪 Descargando Padrón de Datos Abiertos para: {region}...")
        time.sleep(1) # Simula descarga de CSV pesado
        
        # Simulación de la tabla CSV procesada
        datos_historicos = {
            "Arequipa": {"llegadas_mes_pasado": 45000, "nacionalidad_top": "Chile", "crecimiento": 5.2},
            "Puno": {"llegadas_mes_pasado": 12000, "nacionalidad_top": "Francia", "crecimiento": -2.1},
            "Cusco": {"llegadas_mes_pasado": 150000, "nacionalidad_top": "EEUU", "crecimiento": 8.0}
        }
        
        return datos_historicos.get(region)

    def ejecutar_ingesta(self, region: str):
        cache_key = f"promperu_stats_{region.lower()}"
        
        # Las estadísticas de gobierno se publican mensual/anualmente. TTL enorme (30 días).
        datos = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_datos_abiertos(region),
            ttl_minutes=43200 # 30 días
        )
        
        if not datos:
            print(f"[PROMPERÚ] ℹ️ No hay estadísticas publicadas este mes para {region}.")
            return
            
        print(f"[PROMPERÚ] 📈 Insights: Llegadas a {region}: {datos['llegadas_mes_pasado']} turistas. Nacionalidad Top: {datos['nacionalidad_top']}.")
        
        try:
            # 1. Validación estricta con Pydantic (DAI-v2)
            evento_validado = LifextremeSchema(
                source_id="PROMPERU",
                category="METRIC", 
                # Usamos ubicación general para reportes macro
                location={"lat": -12.0464, "lng": -77.0428, "country": "Perú", "region": region},
                payload=datos,
                confidence_score=0.99 # Data oficial del gobierno
            )
            
            # 2. Publicar al Bus de Eventos para que el Marketing Agent y los Agentes de Venta lo usen
            pubsub.publish(evento_validado.model_dump_json())
            print(f"[PROMPERÚ] ✅ Métricas de gobierno validadas e inyectadas al ecosistema Lifextreme.")
            
        except Exception as e:
            print(f"[PYDANTIC-ERROR] ❌ Validación fallida en PROMPERÚ: {e}")

def main():
    print("==================================================")
    print("INICIANDO AGENTE ESTRATÉGICO (PROMPERÚ / MINCETUR)")
    print("==================================================")
    
    sensor = PromperuService()
    # Puno y Arequipa
    sensor.ejecutar_ingesta("Puno")
    sensor.ejecutar_ingesta("Arequipa")
    
if __name__ == "__main__":
    main()
