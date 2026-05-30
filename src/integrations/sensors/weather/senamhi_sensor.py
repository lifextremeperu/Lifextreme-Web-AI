import sys
import time
import random
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from integrations.core.normalizer import DataNormalizer
from integrations.core.pubsub_client import pubsub
from integrations.core.supabase_cache import cache

class SenamhiWeatherSensor:
    def __init__(self):
        # En un escenario real, aquí configuraríamos BeautifulSoup o requests para leer el RSS de SENAMHI
        self.base_url = "https://www.senamhi.gob.pe/avisos"
        
    def fetch_weather_alerts(self, region: str):
        """
        Extrae avisos meteorológicos.
        Simularemos la extracción de una alerta para demostrar la lógica de prevención turística.
        """
        print(f"[SENSOR-CLIMA] 🌩️  Escaneando avisos meteorológicos oficiales para: {region}...")
        time.sleep(1) # Simular scraping
        
        # Simulación: Puno suele tener alertas por Heladas (Nevadas) o Lluvias intensas
        # Vamos a simular que encontramos una "Alerta Naranja"
        alerta_simulada = {
            "region": region,
            "nivel": "Naranja", # Puede ser Amarillo, Naranja, Rojo
            "fenomeno": "Nevadas y Descenso Extremo de Temperatura",
            "validez": "Próximas 48 horas",
            "zonas_afectadas": ["Juliaca", "Lampa", "Carabaya"]
        }
        
        return alerta_simulada

    def ejecutar_monitoreo(self, region: str):
        cache_key = f"weather_alert_{region.lower()}"
        
        # El clima no cambia minuto a minuto. Un TTL de 120 mins ahorra recursos.
        alerta = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_weather_alerts(region),
            ttl_minutes=120 
        )
        
        if not alerta:
            print(f"[SENSOR-CLIMA] ✅ No hay alertas meteorológicas graves para {region}.")
            return
            
        # Evaluar la severidad de la alerta para nuestro ecosistema
        nivel = alerta.get("nivel", "").lower()
        if nivel == "rojo":
            severidad = 5 # Peligro extremo - Detener operaciones turísticas
        elif nivel == "naranja":
            severidad = 4 # Peligro alto - Preparar rutas alternativas
        elif nivel == "amarillo":
            severidad = 2 # Precaución
        else:
            severidad = 1
            
        if severidad >= 3:
            zonas = ", ".join(alerta.get("zonas_afectadas", []))
            mensaje = f"ALERTA METEOROLÓGICA {alerta['nivel'].upper()}: {alerta['fenomeno']} en {region}. Zonas afectadas: {zonas}. Validez: {alerta['validez']}."
            
            print(f"[SENSOR-CLIMA] 🚨 {mensaje}")
            
            # Normalizar y publicar
            json_normalizado = DataNormalizer.normalize(
                source="SENAMHI",
                severity=severidad,
                # Usamos coordenadas aproximadas de la capital de la región
                location={"lat": -15.8402, "lng": -70.0219, "region": region}, 
                payload=mensaje
            )
            pubsub.publish(json_normalizado)
        else:
             print(f"[SENSOR-CLIMA] ℹ️ Alerta menor detectada. Operaciones normales.")

def main():
    print("==================================================")
    print("INICIANDO SENSOR METEOROLÓGICO REGIONAL (SENAMHI)")
    print("==================================================")
    
    sensor = SenamhiWeatherSensor()
    # Monitoreamos Puno, que es donde nuestro agente minero está trabajando
    sensor.ejecutar_monitoreo("Puno")
    
if __name__ == "__main__":
    main()
