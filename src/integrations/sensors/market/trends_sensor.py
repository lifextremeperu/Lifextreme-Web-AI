import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

# Forzar rutas absolutas locales para que los imports funcionen al testear
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from pytrends.request import TrendReq
from src.integrations.core.normalizer import DataNormalizer
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class GoogleTrendsSensor:
    def __init__(self):
        # hl=es para idioma español, tz=300 (GMT-5, hora Perú)
        self.pytrends = TrendReq(hl='es-PE', tz=300)
        
    def fetch_trend_data(self, keyword="Puno turismo"):
        """Llama a la API comercial (Google Trends) - Cuesta ancho de banda / rate limits."""
        print(f"[SENSOR-MERCADO] 🔍 Extrayendo datos reales de Google Trends para: '{keyword}'...")
        # geo='PE' para enfocarnos solo en búsquedas dentro de Perú
        self.pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='PE', gprop='')
        data = self.pytrends.interest_over_time()
        
        if data.empty:
            return 0
            
        # Tomar el último valor de interés (escala 0-100)
        ultimo_interes = data[keyword].iloc[-1]
        # Para que sea serializable a JSON, lo convertimos a int de python nativo
        return int(ultimo_interes)
        
    def ejecutar_monitoreo(self, keyword: str):
        # 1. Definir una key única para la caché
        cache_key = f"trends_{keyword.replace(' ', '_').lower()}"
        
        # 2. Obtener dato usando la estrategia de Caché (TTL 60 mins)
        interes_actual = cache.get_or_set(
            key=cache_key,
            fetch_function=lambda: self.fetch_trend_data(keyword),
            ttl_minutes=60
        )
        
        # 3. Lógica de Negocio: Solo emitir alertas si hay un pico real (> 70 de interés)
        if interes_actual > 70:
            severidad = 3 # Impacto medio-alto (alerta de mercado)
            mensaje = f"PICO DE MERCADO DETECTADO: Interés de {interes_actual}/100 en '{keyword}' en los últimos 7 días."
        else:
            severidad = 1 # Informativo (bajo)
            mensaje = f"Interés estable o bajo: {interes_actual}/100 en '{keyword}'."
            
        print(f"[SENSOR-MERCADO] 📊 {mensaje}")
            
        # 4. Normalizar el dato obligatoriamente
        json_normalizado = DataNormalizer.normalize(
            source="GOOGLE_TRENDS",
            severity=severidad,
            location={"lat": -15.8402, "lng": -70.0219, "region": "Puno"}, # Asumimos Puno por el keyword
            payload=mensaje
        )
        
        # 5. Publicar evento al Bus de Mensajería
        pubsub.publish(json_normalizado)

def main():
    print("==================================================")
    print("INICIANDO SENSOR DE MERCADO (GOOGLE TRENDS)")
    print("==================================================")
    
    sensor = GoogleTrendsSensor()
    # Ejecutamos el monitoreo de un destino que nuestro agente minero está procesando
    sensor.ejecutar_monitoreo("Puno turismo")
    
if __name__ == "__main__":
    main()
