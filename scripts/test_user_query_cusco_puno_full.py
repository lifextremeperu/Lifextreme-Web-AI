import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.transport.aviation_sensor import AviationStackSensor
from src.integrations.sensors.market.trends_sensor import GoogleTrendsSensor
from src.integrations.sensors.logistics.sernanp_service import SernanpService
from src.integrations.sensors.logistics.consettur_service import ConsetturService
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.risk_correlator import RiskCorrelator

def test_full_ecosystem_query():
    print("█"*80)
    print("🌍 ORQUESTACIÓN TOTAL: CONSULTA TURÍSTICA CUSCO -> PUNO")
    print("█"*80 + "\n")
    
    print("--- [CAPA 1: SENSORES DE MERCADO Y VUELOS] ---")
    aviation = AviationStackSensor()
    aviation.ejecutar_monitoreo("CUZ")
    
    trends = GoogleTrendsSensor()
    trends.ejecutar_monitoreo("Turismo Puno")
    
    print("\n--- [CAPA 2: SENSORES DE LOGÍSTICA TERRESTRE Y SATELITAL] ---")
    maps = GoogleMapsTrafficSensor()
    maps.ejecutar_monitoreo("Cusco, Peru", "Puno, Peru", "Puno")
    
    sernanp = SernanpService("https://www.gob.pe/sernanp")
    sernanp.escanear_alertas()
    
    consettur = ConsetturService("https://consettur.com/")
    consettur.escanear_alertas()
    
    print("\n--- [CAPA 3: SENSORES GUBERNAMENTALES Y DE CRISIS (LOS OJOS POLÍTICOS)] ---")
    sutran = SutranService()
    sutran.escanear_alertas()
    
    gdelt = GdeltCrisisSensor()
    gdelt.ejecutar_monitoreo(pais="PE", region_objetivo="Puno")
    
    print("\n" + "█"*80)
    print("🧠 CEREBRO CENTRAL: MOTOR DE CORRELACIÓN EVALUANDO LA SITUACIÓN")
    print("█"*80)
    correlator = RiskCorrelator()
    correlator.calcular_score_regional("Puno")
    
    print("\n✅ ORQUESTACIÓN FINALIZADA.")

if __name__ == "__main__":
    test_full_ecosystem_query()
