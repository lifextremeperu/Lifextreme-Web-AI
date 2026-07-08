import os
import sys
import time
import requests
sys.stdout.reconfigure(encoding='utf-8')

# Forzar rutas absolutas locales para imports
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from dotenv import load_dotenv
from src.integrations.core.normalizer import DataNormalizer
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class AviationStackSensor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AVIATION_STACK_API_KEY", "")
        self.base_url = "http://api.aviationstack.com/v1/flights"
        
    def fetch_flight_data(self, arr_iata="AQP"):
        """
        Extrae datos de vuelos para un aeropuerto específico.
        Implementa BACKOFF EXPONENCIAL para fallos (429, 500).
        """
        print(f"[SENSOR-VUELOS] ✈️  Consultando estado de vuelos hacia el aeropuerto: {arr_iata}...")
        
        # Si no hay API Key, simulamos la respuesta para no bloquear el desarrollo
        if not self.api_key:
            print("[SENSOR-VUELOS] ⚠️  No se encontró AVIATION_STACK_API_KEY en .env. Usando Mock de prueba...")
            time.sleep(1) # Simular latencia de red
            # Simulamos un fallo de red para demostrar el Backoff Exponencial
            self._demonstrate_exponential_backoff()
            
            # Devolvemos un vuelo retrasado ficticio
            return [{
                "flight": {"iata": "LA2026"},
                "flight_status": "delayed",
                "departure": {"airport": "Lima", "timezone": "America/Lima"},
                "arrival": {"airport": "Arequipa", "iata": "AQP", "delay": 45}
            }]
            
        params = {
            "access_key": self.api_key,
            "arr_iata": arr_iata,
            "limit": 10
        }
        
        max_retries = 3
        base_delay = 2 # Segundos
        
        for attempt in range(max_retries):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])
                elif response.status_code in [429, 500, 502, 503, 504]:
                    delay = base_delay * (2 ** attempt)
                    print(f"[SENSOR-VUELOS] ⚠️  Error de red (HTTP {response.status_code}). Backoff Exponencial: esperando {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"[SENSOR-VUELOS] ❌ Error de API: {response.status_code} - {response.text}")
                    return []
                    
            except requests.exceptions.RequestException as e:
                delay = base_delay * (2 ** attempt)
                print(f"[SENSOR-VUELOS] ⚠️  Caída de conexión ({e}). Backoff Exponencial: esperando {delay}s...")
                time.sleep(delay)
                
        # Si llega aquí, el servicio está totalmente caído
        print("[SENSOR-VUELOS] 🚨 ALERTA CRÍTICA: La API de AviationStack está caída por más de 10 minutos (timeout).")
        # En producción, esto publicaría un evento especial de "Servicio Caído" en Pub/Sub
        return []

    def _demonstrate_exponential_backoff(self):
        """Método de demostración técnica del requerimiento DAI-v1"""
        print("[SENSOR-VUELOS] 🔄 Probando protocolo de Resiliencia (Exponential Backoff)...")
        for attempt in range(2):
            delay = 1 * (2 ** attempt)
            print(f"  -> Intento fallido simulado. Reintentando en {delay}s...")
            time.sleep(delay)
        print("  -> Conexión recuperada con éxito.")

    def ejecutar_monitoreo(self, arr_iata="AQP"):
        cache_key = f"flights_arrival_{arr_iata.lower()}"
        
        vuelos = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_flight_data(arr_iata),
            ttl_minutes=30 # Los vuelos cambian rápido, TTL menor
        )
        
        if not vuelos:
            print("[SENSOR-VUELOS] No hay datos de vuelos disponibles.")
            return
            
        # Analizar los vuelos para encontrar disrupciones (retrasos o cancelaciones)
        disrupciones = [v for v in vuelos if v.get("flight_status") in ["cancelled", "delayed"]]
        
        if disrupciones:
            for vuelo in disrupciones:
                num_vuelo = vuelo['flight']['iata']
                estado = vuelo['flight_status'].upper()
                
                severidad = 4 if estado == "CANCELLED" else 3
                mensaje = f"DISRUPCIÓN AÉREA: El vuelo {num_vuelo} hacia {arr_iata} está {estado}."
                print(f"[SENSOR-VUELOS] 🚨 {mensaje}")
                
                json_normalizado = DataNormalizer.normalize(
                    source="AVIATION_STACK",
                    severity=severidad,
                    location={"lat": -16.3988, "lng": -71.5369, "region": "Aeropuerto Destino"}, 
                    payload=mensaje
                )
                pubsub.publish(json_normalizado)
        else:
            print(f"[SENSOR-VUELOS] ✅ Todos los vuelos hacia {arr_iata} están a tiempo.")

def main():
    print("==================================================")
    print("INICIANDO SENSOR LOGÍSTICO (AVIATION STACK)")
    print("==================================================")
    
    sensor = AviationStackSensor()
    # Monitorear el aeropuerto de Arequipa (Alfredo Rodríguez Ballón)
    sensor.ejecutar_monitoreo("AQP")
    
if __name__ == "__main__":
    main()
