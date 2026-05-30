import time
import sys
sys.stdout.reconfigure(encoding='utf-8')
from integrations.core.normalizer import DataNormalizer
from integrations.core.pubsub_client import pubsub
from integrations.core.supabase_cache import cache

def simular_llamada_api_aviation():
    """Simula una llamada HTTP a AviationStack que cuesta dinero."""
    time.sleep(1) # Simula latencia
    return "Vuelo LATAM 204 CANCELADO en Arequipa"

def main():
    print("==================================================")
    print("INICIANDO PRUEBA DEL BLOQUE 1 (DAI-v1 CORE)")
    print("==================================================")
    
    sensor_key = "flight_status_latam204_aqp"
    
    print("\n--- Intento 1: Primera vez que el sensor revisa el vuelo ---")
    # Usa la caché. Como es la primera vez, llamará a la API.
    payload_crudo = cache.get_or_set(sensor_key, simular_llamada_api_aviation)
    
    # Normalizar la data cruda al esquema JSON estricto
    json_normalizado = DataNormalizer.normalize(
        source="AVIATION_STACK",
        severity=4, # 4 = Alto impacto (vuelo cancelado)
        location={"lat": -16.3988, "lng": -71.5369, "region": "Arequipa"},
        payload=payload_crudo
    )
    
    # Publicar en el bus de eventos
    pubsub.publish(json_normalizado)
    
    print("\n--- Intento 2: 5 minutos después, el sensor vuelve a revisar ---")
    # Usa la caché. Como pasaron menos de 60 mins, NO llamará a la API (ahorra dinero).
    payload_cacheado = cache.get_or_set(sensor_key, simular_llamada_api_aviation)
    
    json_normalizado_2 = DataNormalizer.normalize(
        source="AVIATION_STACK",
        severity=4,
        location={"lat": -16.3988, "lng": -71.5369, "region": "Arequipa"},
        payload=payload_cacheado
    )
    pubsub.publish(json_normalizado_2)
    
    print("\n==================================================")
    print("PRUEBA COMPLETADA CON ÉXITO")

if __name__ == "__main__":
    main()
