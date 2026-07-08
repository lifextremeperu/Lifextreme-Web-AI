import sys
import time
import os
import requests
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache
from dotenv import load_dotenv

class GoogleMapsTrafficSensor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        
    def fetch_route_traffic(self, origin: str, destination: str):
        """
        Consulta la API REST de Google Maps (Distance Matrix) para comparar 
        el tiempo de viaje ideal vs el tiempo actual con tráfico.
        """
        print(f"[SENSOR-TRÁFICO] 🗺️ Analizando ruta EN VIVO por satélite: {origin} -> {destination}...")
        
        if not self.api_key:
            print("[SENSOR-TRÁFICO] ⚠️ No se encontró la API Key de Google Maps. Usando mock.")
            return {"origin": origin, "destination": destination, "duration": 120, "duration_in_traffic": 120}
            
        params = {
            "origins": origin,
            "destinations": destination,
            "departure_time": "now", # Clave para obtener duration_in_traffic
            "key": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "OK":
                    element = data["rows"][0]["elements"][0]
                    if element.get("status") == "OK":
                        # Convertimos los segundos a minutos
                        duration_mins = element["duration"]["value"] // 60
                        # Si no hay datos de tráfico, asumimos que es igual a la duración normal
                        duration_in_traffic_mins = element.get("duration_in_traffic", element["duration"])["value"] // 60
                        
                        return {
                            "origin": origin,
                            "destination": destination,
                            "duration": duration_mins,
                            "duration_in_traffic": duration_in_traffic_mins
                        }
                    else:
                        print(f"[SENSOR-TRÁFICO] ⚠️ Google Maps no pudo calcular la ruta: {element.get('status')}")
                else:
                    print(f"[SENSOR-TRÁFICO] ❌ Error de API Google Maps: {data.get('error_message', data.get('status'))}")
            else:
                print(f"[SENSOR-TRÁFICO] ❌ Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"[SENSOR-TRÁFICO] ❌ Fallo crítico de conexión a Google Maps: {e}")
            
        return None

    def ejecutar_monitoreo(self, origin: str, destination: str, region_asociada: str):
        cache_key = f"maps_traffic_{origin.lower()}_{destination.lower()}"
        
        # El tráfico cambia rápido. TTL = 15 minutos
        ruta = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_route_traffic(origin, destination),
            ttl_minutes=15
        )
        
        if not ruta:
            return
            
        ideal = ruta["duration"]
        actual = ruta["duration_in_traffic"]
        
        # ratio: qué tanto más nos estamos demorando respecto al ideal
        ratio = actual / ideal if ideal > 0 else 1
        
        # Clasificar la severidad del tráfico según la matemática acordada
        if ratio >= 2.0:
            severidad = 5 # Más del doble del tiempo (Posible Bloqueo/Huelga)
            mensaje = f"TRÁFICO CRÍTICO: La ruta {origin}-{destination} está tomando {actual} mins (Normal: {ideal} mins). Desvío del {int((ratio-1)*100)}%."
        elif ratio >= 1.5:
            severidad = 3 # Tráfico pesado (Accidente menor)
            mensaje = f"RETRASO LOGÍSTICO: La ruta {origin}-{destination} está tomando {actual} mins (Normal: {ideal} mins)."
        else:
            print(f"[SENSOR-TRÁFICO] 🟢 Tráfico fluido en ruta {origin}-{destination} ({actual} mins). Todo OK.")
            return
            
        print(f"[SENSOR-TRÁFICO] 🚨 {mensaje}")
        
        try:
            evento_validado = LifextremeSchema(
                source_id="GOOGLE_MAPS",
                category="RISK", 
                location={"lat": -15.8402, "lng": -70.0219, "country": "Perú", "region": region_asociada},
                payload={"ruta": f"{origin}-{destination}", "retraso_porcentaje": (ratio-1)*100, "mensaje": mensaje},
                confidence_score=0.98 # Google Maps es altamente confiable
            )
            
            pubsub.publish(evento_validado.model_dump_json())
            print(f"[SENSOR-TRÁFICO] ✅ Alerta vial validada e inyectada al ecosistema.")
            
        except Exception as e:
            print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")

def main():
    print("==================================================")
    print("INICIANDO SENSOR VIAL EN VIVO (GOOGLE MAPS)")
    print("==================================================")
    
    sensor = GoogleMapsTrafficSensor()
    # Monitoreamos una ruta real en Cusco
    sensor.ejecutar_monitoreo("Cusco, Peru", "Ollantaytambo, Peru", "Cusco")
    
if __name__ == "__main__":
    main()
