import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.integrations.core.pubsub_client import pubsub

class RiskCorrelator:
    def __init__(self):
        # Pesos matemáticos aprobados en la Directiva DAI-P-v3
        self.risk_weights = {
            "GOOGLE_MAPS": 4,   # Bloqueo vial detectado por GPS
            "GDELT": 3,         # Noticias de protestas sociales
            "SENAMHI": 2,       # Alerta climática Naranja/Roja
            "AVIATION_STACK": 2,# Disrupciones en vuelos
            "SERNANP": 4,       # Cierre oficial de parques
            "CONSETTUR": 5,     # Suspensión de buses a Machu Picchu
            "SUTRAN": 5         # Bloqueo oficial MTC
        }

    def calcular_score_regional(self, region: str):
        """
        Lee todos los eventos del Bus de Mensajes y calcula el Score (1-10)
        cruzando las fuentes de riesgo para una región específica.
        """
        print(f"\n[MOTOR DE CORRELACIÓN] 🧠 Analizando amenazas cruzadas para: {region}...")
        
        score_riesgo = 1 # Estado base: Seguro
        fuentes_activas = []
        
        # Leemos los eventos que los sensores publicaron
        for evento_str in pubsub.messages:
            evento = evento_str if isinstance(evento_str, dict) else json.loads(evento_str)
            categoria = evento.get('category', '')
            
            if categoria != 'RISK':
                if not ('severity' in evento and evento['severity'] >= 3):
                    # print(f"DEBUG: Ignorando evento sin RISK ni severity>=3: {evento}")
                    continue
            
            source = evento.get('source_id') or evento.get('source')
            ubicacion = evento.get('location', {})
            region_evento = ubicacion.get('region', '')
            
            # Puno está en la región
            if region.lower() in region_evento.lower() or not region_evento:
                peso = self.risk_weights.get(source, 0)
                if peso > 0 and source not in fuentes_activas:
                    score_riesgo += peso
                    fuentes_activas.append(source)
                    print(f"  -> Peligro detectado por {source} (+{peso} puntos).")
                else:
                    if peso == 0:
                        print(f"  -> DEBUG: Fuente {source} no tiene peso asignado en risk_weights.")
                    
        # Limitar el score a 10 como máximo
        score_riesgo = min(score_riesgo, 10)
        
        print(f"\n[SCORE TOTAL] Nivel de Riesgo para {region}: {score_riesgo}/10")
        
        # Lógica de Umbrales Autónomos (DAI-P-v3)
        if score_riesgo >= 7:
            print("🔴 ALERTA CRÍTICA (CRISIS CONFIRMADA)")
            self._activar_kill_switch(region, fuentes_activas)
        elif score_riesgo >= 5:
            print("🟠 ALERTA TEMPRANA")
            print(f"   -> Notificando al equipo de Operaciones por Telegram: 'Posible disrupción en {region}'.")
            from src.integrations.core.telegram_client import telegram_bot
            telegram_bot.send_alert(f"⚠️ <b>ALERTA TEMPRANA (Lifextreme AI)</b>\n\nPosible disrupción turística detectada en <b>{region}</b>.\nScore de Riesgo: {score_riesgo}/10\nFuentes: {', '.join(fuentes_activas)}")
        else:
            print("🟢 OPERACIÓN NORMAL")
            print("   -> Condiciones seguras para venta y operación.")
            
        return score_riesgo

    def _activar_kill_switch(self, region: str, fuentes: list):
        print("\n" + "!"*60)
        print("🚨 INICIANDO PROTOCOLO KILL-SWITCH 🚨")
        print("!"*60)
        print(f"MOTIVO: Múltiples sensores ({', '.join(fuentes)}) confirman crisis inminente en {region}.")
        print(f"ACCIÓN 1: Bloqueando temporalmente las ventas de todos los tours a {region} en el Frontend (Booking API).")
        print(f"ACCIÓN 2: Activando 'Agente de Crisis' para redactar comunicados de desvío de ruta.")
        print("ESTADO: Ecosistema Protegido. Esperando revisión humana para reactivar.")
        print("!"*60 + "\n")
        
        from src.integrations.core.telegram_client import telegram_bot
        mensaje_urgente = (
            f"🚨 <b>¡PROTOCOLO KILL-SWITCH ACTIVADO!</b> 🚨\n\n"
            f"<b>Región:</b> {region}\n"
            f"<b>Razón:</b> Crisis inminente detectada por sensores satelitales/gubernamentales.\n"
            f"<b>Fuentes de Riesgo:</b> {', '.join(fuentes)}\n\n"
            f"<i>Acción Autónoma:</i> Se han bloqueado automáticamente las ventas hacia esta región para proteger la operación.\n"
            f"<i>Por favor, revisa el panel de control.</i>"
        )
        telegram_bot.send_alert(mensaje_urgente)

def main():
    # Simulamos el ecosistema corriendo
    # 1. Cargamos el Sensor de GDELT (Protestas) y Google Maps (Bloqueos viales)
    # y los hacemos inyectar sus alertas a nuestro PubSub
    print("==================================================")
    print("SIMULACIÓN DE CRISIS LIFTEXREME (DAI-P-v3)")
    print("==================================================")
    
    from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
    # Este script de GDELT (DAI-v1) inyectaba "severity": 5, que nuestro Motor atrapa por compatibilidad
    from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
    
    maps_sensor = GoogleMapsTrafficSensor()
    gdelt_sensor = GdeltCrisisSensor()
    
    print("\n[FASE 1] SENSORES MONITOREANDO EL MUNDO REAL...")
    gdelt_sensor.ejecutar_monitoreo(pais="PE", region_objetivo="Puno")
    maps_sensor.ejecutar_monitoreo(origin="Puno", destination="Juliaca", region_asociada="Puno")
    
    print("\n[FASE 2] MOTOR CRUZANDO DATOS AUTÓNOMAMENTE...")
    correlator = RiskCorrelator()
    correlator.calcular_score_regional("Puno")
    
if __name__ == "__main__":
    main()
