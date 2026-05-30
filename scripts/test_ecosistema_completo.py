import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.integrations.integrations_manager import IntegrationsManager
from src.integrations.marketing.amadeus_service import AmadeusMarketingService
from src.integrations.core.node_manager import NodeManager
from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.risk_correlator import RiskCorrelator

def test_ecosistema():
    print("\n" + "█"*60)
    print("🚀 INICIANDO PRUEBA GLOBAL DEL ECOSISTEMA LIFEXTREME")
    print("█"*60 + "\n")
    
    # FASE 1: Inteligencia de Datos Base
    print("--- [FASE 1] CEREBRO ESTADÍSTICO Y FINANCIERO ---")
    int_manager = IntegrationsManager()
    # Solo corremos BCRP y Promperu para acortar la demo
    int_manager.bcrp.ejecutar_ingesta()
    time.sleep(1)
    int_manager.promperu.ejecutar_ingesta("Cusco")
    time.sleep(1)
    
    # FASE 2: Inteligencia de Marketing Predictivo
    print("\n--- [FASE 2] INTELIGENCIA DE MERCADO (AMADEUS) ---")
    mkt_manager = AmadeusMarketingService()
    mkt_manager.ejecutar_analisis_mercado(["JFK", "MAD"])
    time.sleep(1)
    
    # FASE 3: Protección Logística Continua (Nodos Capa 0)
    print("\n--- [FASE 3] VIGILANCIA LOGÍSTICA (Nodos Capa 0) ---")
    node_manager = NodeManager()
    node_manager.ejecutar_capa("0")
    time.sleep(1)
    
    # FASE 4: Simulación de Desastre y Defensa Autónoma
    print("\n--- [FASE 4] SIMULACIÓN DE CRISIS EN CUSCO ---")
    print("   -> El sistema detectará autónomamente una crisis climática y vial...")
    
    maps_sensor = GoogleMapsTrafficSensor()
    gdelt_sensor = GdeltCrisisSensor()
    
    # Forzamos los eventos
    gdelt_sensor.ejecutar_monitoreo(pais="PE", region_objetivo="Cusco")
    time.sleep(1)
    maps_sensor.ejecutar_monitoreo("Cusco", "Ollantaytambo", "Cusco")
    time.sleep(1)
    
    # FASE 5: El Motor Toma la Decisión Final
    print("\n--- [FASE 5] MOTOR DE CORRELACIÓN Y DECISIÓN FINAL ---")
    correlator = RiskCorrelator()
    correlator.calcular_score_regional("Cusco")
    
    print("\n" + "█"*60)
    print("✅ PRUEBA DEL ECOSISTEMA FINALIZADA.")
    print("█"*60 + "\n")

if __name__ == "__main__":
    test_ecosistema()
