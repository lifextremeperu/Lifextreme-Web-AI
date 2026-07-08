import sys
import time
import requests
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.models.lifextreme_schema import LifextremeSchema
from src.integrations.core.pubsub_client import pubsub
from src.integrations.core.supabase_cache import cache

class BcrpService:
    def __init__(self):
        # Endpoint de la API del BCRP (Estadísticas)
        # La serie PD04637PD es el Tipo de Cambio Bancario de Compra (Soles por Dólar)
        self.bcrp_api_url = "https://estadisticas.bcrp.gob.pe/estadisticas/observaciones/api/PD04637PD/json"

    def fetch_tipo_cambio(self):
        """
        Consulta la API del Banco Central de Reserva del Perú para obtener 
        el tipo de cambio oficial del día (USD a PEN).
        """
        print(f"[BCRP] 🏦 Conectando a la API de Estadísticas del Banco Central de Reserva del Perú...")
        
        try:
            response = requests.get(self.bcrp_api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                periodos = data.get("periods", [])
                if periodos:
                    # El último periodo registrado
                    ultimo_dato = periodos[-1]
                    fecha = ultimo_dato.get("name")
                    valor = float(ultimo_dato.get("values")[0])
                    return {"fecha": fecha, "usd_pen": valor}
        except Exception as e:
            print(f"[BCRP] ⚠️ Error conectando al BCRP ({e}). Usando tipo de cambio de contingencia.")
            
        # Fallback de seguridad si la API no responde
        return {"fecha": datetime.now().strftime("%d.%b.%y"), "usd_pen": 3.75}

    def ejecutar_ingesta(self):
        cache_key = "bcrp_exchange_rate_usd"
        
        # El tipo de cambio se actualiza diario, guardamos en caché por 12 horas
        datos = cache.get_or_set(
            key=cache_key,
            fetch_function=self.fetch_tipo_cambio,
            ttl_minutes=720 
        )
        
        if not datos:
            return
            
        print(f"[BCRP] 💵 Tipo de Cambio Oficial ({datos['fecha']}): 1 USD = {datos['usd_pen']} PEN.")
        
        try:
            evento_validado = LifextremeSchema(
                source_id="BCRP",
                category="MARKET", 
                location={"lat": -12.0464, "lng": -77.0428, "country": "Perú", "region": "Nacional"},
                payload=datos,
                confidence_score=1.0 # BCRP es la fuente oficial máxima
            )
            
            pubsub.publish(evento_validado.model_dump_json())
            print(f"[BCRP] ✅ Datos financieros validados e inyectados al ecosistema para conversión de precios.")
            
        except Exception as e:
            print(f"[PYDANTIC-ERROR] ❌ Validación fallida en BCRP: {e}")

def main():
    print("==================================================")
    print("INICIANDO AGENTE FINANCIERO (BCRP)")
    print("==================================================")
    
    sensor = BcrpService()
    sensor.ejecutar_ingesta()
    
if __name__ == "__main__":
    main()
