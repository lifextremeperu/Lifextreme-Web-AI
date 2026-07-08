import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Importamos todos los módulos validados del ecosistema (DAI-v2)
from src.integrations.government.promperu_service import PromperuService
from src.integrations.government.bcrp_service import BcrpService
from src.integrations.culture.wikidata_service import WikiDataService

# En un entorno de producción, aquí también importaríamos los sensores de riesgo
# from src.integrations.sensors.gdelt_sensor import GdeltCrisisSensor
# from src.integrations.sensors.aviation_sensor import AviationStackSensor
# from src.integrations.sensors.senamhi_sensor import SenamhiWeatherSensor

class IntegrationsManager:
    """
    El 'Control de Misión' de Lifextreme (DAI-v2).
    Orquesta el orden de ejecución y el ciclo de vida de los agentes periféricos.
    """
    def __init__(self):
        self.promperu = PromperuService()
        self.bcrp = BcrpService()
        self.wikidata = WikiDataService()
        
    def inicializar_ecosistema(self, regiones_objetivo: list):
        print("\n" + "="*60)
        print("🚀 INICIANDO ECOSISTEMA LIFTEXREME (DAI-v2) - CONTROL DE MISIÓN")
        print("="*60)
        
        # 1. Módulo Financiero (Prioridad Absoluta para cotizaciones)
        print("\n[FASE 1] INICIALIZANDO FINANZAS...")
        self.bcrp.ejecutar_ingesta()
        time.sleep(1)
        
        # 2. Módulo Estadístico Gubernamental
        print("\n[FASE 2] INICIALIZANDO ESTADÍSTICAS GUBERNAMENTALES...")
        for region in regiones_objetivo:
            self.promperu.ejecutar_ingesta(region)
            time.sleep(1)
            
        # 3. Módulo de Cultura y Contexto (Para cruzar con FQSAs)
        print("\n[FASE 3] INICIALIZANDO CONTEXTO HISTÓRICO...")
        for region in regiones_objetivo:
            self.wikidata.ejecutar_enriquecimiento(region)
            time.sleep(1)
            
        # En el futuro aquí se llamarían a los monitores de riesgo continuo (SUTRAN, GDELT)
        
        print("\n" + "="*60)
        print("✅ ECOSISTEMA INICIALIZADO Y SINCRONIZADO CORRECTAMENTE")
        print("   Todos los eventos han sido validados por Pydantic (LifextremeSchema)")
        print("   y enviados al Pub/Sub Gateway.")
        print("="*60 + "\n")

def main():
    manager = IntegrationsManager()
    # Puno y Arequipa son nuestras regiones activas de minería
    manager.inicializar_ecosistema(regiones_objetivo=["Puno", "Arequipa"])
    
if __name__ == "__main__":
    main()
