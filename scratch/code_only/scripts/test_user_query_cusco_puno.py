import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.transport.aviation_sensor import AviationStackSensor
from src.integrations.sensors.market.trends_sensor import GoogleTrendsSensor

def test_cusco_puno():
    print("--- 🚀 INICIANDO ANÁLISIS DE INTELIGENCIA (CUSCO -> PUNO) ---")
    
    print("\n1. 🗺️ Evaluando Ruta Terrestre (Google Maps API)")
    maps = GoogleMapsTrafficSensor()
    # Ejecutamos monitoreo en vivo para la ruta de Cusco a Puno
    maps.ejecutar_monitoreo("Cusco, Peru", "Puno, Peru", "Puno")
    
    print("\n2. ✈️ Evaluando Aeropuerto de Cusco (AviationStack API)")
    aviation = AviationStackSensor()
    # Monitoreamos vuelos llegando a Cusco (Alejandro Velasco Astete)
    aviation.ejecutar_monitoreo("CUZ")
    
    print("\n3. 📊 Evaluando Tendencias de Mercado (Google Trends)")
    trends = GoogleTrendsSensor()
    trends.ejecutar_monitoreo("Turismo Puno")
    
    print("\n--- ✅ ANÁLISIS FINALIZADO ---")

if __name__ == "__main__":
    test_cusco_puno()
