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
        Extrae avisos meteorológicos de SENAMHI usando BeautifulSoup.
        """
        print(f"[SENSOR-CLIMA] 🌩️  Escaneando avisos meteorológicos oficiales en la web para: {region}...")
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
            }
            # Intentamos conectarnos al portal principal
            response = requests.get(self.base_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                texto_web = soup.get_text().lower()
                
                # Buscar si la región y palabras de alerta están en la página actual
                if region.lower() in texto_web and ("alerta" in texto_web or "aviso" in texto_web):
                    # Determinar severidad basada en texto
                    nivel = "Amarillo"
                    if "rojo" in texto_web or "roja" in texto_web:
                        nivel = "Rojo"
                    elif "naranja" in texto_web:
                        nivel = "Naranja"
                        
                    fenomeno = "Condición climática adversa (Lluvia/Nevada)"
                    if "nieve" in texto_web or "nevada" in texto_web or "helada" in texto_web:
                        fenomeno = "Nevadas y Descenso Extremo de Temperatura"
                    elif "lluvia" in texto_web or "precipitación" in texto_web:
                        fenomeno = "Lluvias Intensas"
                        
                    return {
                        "region": region,
                        "nivel": nivel,
                        "fenomeno": fenomeno,
                        "validez": "Próximas 24-48 horas",
                        "zonas_afectadas": [region]
                    }
                else:
                    return None # No hay alertas graves para esta región
            else:
                print(f"[SENSOR-CLIMA] ⚠️ No se pudo acceder a SENAMHI (HTTP {response.status_code}).")
                return None
                
        except Exception as e:
            print(f"[SENSOR-CLIMA] ⚠️ Error de conexión BeautifulSoup: {e}")
            return None

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
