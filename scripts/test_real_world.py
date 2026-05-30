import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.integrations.core.node_manager import NodeManager
from src.integrations.sensors.transport.aviation_sensor import AviationStackSensor
from src.integrations.risk_correlator import RiskCorrelator

def test_mundo_real():
    print("\n" + "█"*60)
    print("🌍 INICIANDO PRUEBA CON DATOS 100% REALES (VIVO)")
    print("█"*60 + "\n")
    
    # 1. Vuelos Reales
    print("--- [FASE 1] LECTURA DE VUELOS (API REAL) ---")
    aviation_sensor = AviationStackSensor()
    # Consultamos vuelos en Lima (LIM) usando tu API Key
    aviation_sensor.ejecutar_monitoreo(arr_iata="LIM")
    time.sleep(1)
    
    # 2. Logística y Gobierno Reales
    print("\n--- [FASE 2] LECTURA GUBERNAMENTAL (SCRAPING REAL) ---")
    node_manager = NodeManager()
    node_manager.ejecutar_capa("0")
    time.sleep(1)
    
    # 3. El Motor Decide
    print("\n--- [FASE 3] MOTOR DE CORRELACIÓN EVALUANDO REALIDAD ---")
    correlator = RiskCorrelator()
    # Calculamos el riesgo global usando 'Perú' u omitiendo la región para que sume todo
    correlator.calcular_score_regional("Cusco")
    correlator.calcular_score_regional("Lima")
    
    print("\n" + "█"*60)
    print("✅ PRUEBA DEL MUNDO REAL FINALIZADA.")
    print("█"*60 + "\n")

if __name__ == "__main__":
    test_mundo_real()
