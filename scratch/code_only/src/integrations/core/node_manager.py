import sys
import json
import os
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

class NodeManager:
    """
    Orquestador de Capas (Capa 0, 1, 2) basado en nodos.json.
    Permite escalar el número de entidades monitoreadas sin colapsar el sistema.
    """
    def __init__(self):
        self.config_path = Path(__file__).resolve().parent.parent.parent.parent / "config" / "nodos.json"
        self.nodos = self._cargar_configuracion()
        
    def _cargar_configuracion(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[NODE-MANAGER] ❌ Error cargando nodos.json: {e}")
            return {}

    def ejecutar_capa(self, capa_id: str):
        capas = self.nodos.get("capas", {})
        if capa_id not in capas:
            print(f"[NODE-MANAGER] ⚠️ Capa {capa_id} no encontrada en la configuración.")
            return
            
        info_capa = capas[capa_id]
        print("\n" + "="*60)
        print(f"🚀 INICIANDO EJECUCIÓN DE: Capa {capa_id} ({info_capa['descripcion']})")
        print("="*60)
        
        for nombre_nodo in info_capa["nodos"]:
            endpoint = self.nodos.get("endpoints", {}).get(nombre_nodo)
            if not endpoint:
                print(f"[NODE-MANAGER] ⚠️ Configuración de endpoint faltante para {nombre_nodo}")
                continue
                
            print(f"\n[NODO] Activando Agente para: {nombre_nodo}")
            print(f"       Tipo: {endpoint['tipo']} | Método: {endpoint['metodo']}")
            
            # En un entorno real, aquí usaríamos un Factory Pattern para instanciar 
            # la clase específica (ej. SernanpService) o un Scraper genérico.
            self._simular_ejecucion_nodo(nombre_nodo, endpoint)

    def _simular_ejecucion_nodo(self, nombre_nodo: str, endpoint: dict):
        """Simulación del enrutador de agentes"""
        if nombre_nodo == "SERNANP":
            from src.integrations.sensors.logistics.sernanp_service import SernanpService
            agente = SernanpService(endpoint["url"])
            agente.escanear_alertas()
        elif nombre_nodo == "CONSETTUR":
            from src.integrations.sensors.logistics.consettur_service import ConsetturService
            agente = ConsetturService(endpoint["url"])
            agente.escanear_alertas()
        else:
            print(f"       -> [TODO] Desarrollar servicio específico para {nombre_nodo}...")

def main():
    manager = NodeManager()
    # En producción, esto sería llamado por un CRON job cada 30 minutos
    manager.ejecutar_capa("0")
    
if __name__ == "__main__":
    main()
