import sys
import time
import os
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class AmadeusMarketingService:
    def __init__(self):
        # Amadeus requiere autenticación OAuth2. Necesitaremos un Client ID y Client Secret
        self.api_key = os.getenv("AMADEUS_API_KEY", "")
        self.api_secret = os.getenv("AMADEUS_API_SECRET", "")
        self.auth_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        self.flight_intent_endpoint = "https://test.api.amadeus.com/v1/shopping/flight-destinations"
        
    def fetch_flight_intent(self, origin_iata: str, destination_iata: str = "LIM"):
        """
        Consulta la API de Amadeus para medir el interés de vuelo desde un país
        emisor hacia Perú (LIM).
        """
        print(f"[AMADEUS-MKT] 🛫 Analizando intención global de vuelo desde {origin_iata} hacia {destination_iata}...")
        
        # En producción: 
        # 1. Obtener Token OAuth2
        # 2. GET request a flight-destinations
        
        time.sleep(1) # Simulación de red
        
        # Simulamos la respuesta algorítmica de Amadeus
        # Ejemplo: Si origin es JFK (New York), vemos alta intención
        intent_score = 0
        crecimiento_mensual = 0
        
        if origin_iata == "JFK": # USA
            intent_score = 85
            crecimiento_mensual = 12.5
        elif origin_iata == "MAD": # España
            intent_score = 92
            crecimiento_mensual = 25.0 # Fuerte pico desde España
        elif origin_iata == "CDG": # Francia
            intent_score = 45
            crecimiento_mensual = -5.0
            
        return {
            "origen": origin_iata,
            "destino": destination_iata,
            "intent_score": intent_score,
            "crecimiento_porcentual": crecimiento_mensual
        }

    def ejecutar_analisis_mercado(self, mercados_objetivo: list):
        print("\n==================================================")
        print("INICIANDO MOTOR DE MARKETING PREDICTIVO (AMADEUS)")
        print("==================================================")
        
        recomendaciones = []
        
        for mercado in mercados_objetivo:
            cache_key = f"amadeus_intent_{mercado.lower()}"
            
            # La intención de vuelo se mide semanalmente
            datos = cache.get_or_set(
                key=cache_key,
                fetch_function=lambda: self.fetch_flight_intent(mercado, "LIM"),
                ttl_minutes=10080 # 7 días
            )
            
            if not datos:
                continue
                
            score = datos["intent_score"]
            crecimiento = datos["crecimiento_porcentual"]
            
            print(f"  -> Mercado {mercado}: Score de Interés = {score}/100 | Tendencia = {crecimiento}%")
            
            # Algoritmo de Decisión de Marketing (DAI-MKT)
            if crecimiento > 20:
                recomendacion = f"MERCADO EMERGENTE DETECTADO. Desplazar presupuesto de Ads hacia {mercado}."
                recomendaciones.append((mercado, recomendacion))
                print(f"  🔥 ALERTA MKT: {recomendacion}")
            elif crecimiento < 0:
                print(f"  📉 ALERTA MKT: Caída de interés en {mercado}. Reducir puja de palabras clave.")
            
            try:
                evento_validado = LifextremeSchema(
                    source_id="AMADEUS",
                    category="MARKET", 
                    location={"lat": 0.0, "lng": 0.0, "country": "Global", "region": mercado},
                    payload=datos,
                    confidence_score=0.99
                )
                
                pubsub.publish(evento_validado.model_dump_json())
                
            except Exception as e:
                print(f"[PYDANTIC-ERROR] ❌ Fallo en validación: {e}")
                
        print("\n[RESUMEN ESTRATÉGICO]")
        for rec in recomendaciones:
            print(f"✅ ACCIÓN SUGERIDA: {rec[1]}")

def main():
    sensor = AmadeusMarketingService()
    # Analizamos intención desde USA (JFK), España (MAD) y Francia (CDG)
    sensor.ejecutar_analisis_mercado(["JFK", "MAD", "CDG"])
    
if __name__ == "__main__":
    main()
