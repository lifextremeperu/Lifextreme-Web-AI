import sys
import json
import httpx
from pathlib import Path

# Ajustar el PATH para importar los sensores desde src/integrations
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.integrations.sensors.weather.senamhi_sensor import SenamhiWeatherSensor
from src.integrations.sensors.transport.flight_demand_sensor import FlightDemandSensor
from src.integrations.sensors.market.sentiment_sensor import SentimentSensor

sys.stdout.reconfigure(encoding='utf-8')

OLLAMA_URL = "http://localhost:11434/api/generate"

class PredictiveOrchestrator:
    def __init__(self):
        self.weather_sensor = SenamhiWeatherSensor()
        self.flight_sensor = FlightDemandSensor()
        self.sentiment_sensor = SentimentSensor()

    def run_daily_prediction(self):
        print("===================================================================")
        print(" 🧠 ORQUESTADOR PREDICTIVO LIFEXTREME (Nivel 100) ")
        print("===================================================================")
        
        # 1. Recolectar datos del clima (Cusco/Puno)
        # Reutilizamos la lógica del sensor existente (usará el simulado de alerta)
        clima_data = self.weather_sensor.fetch_weather_alerts("Cusco")
        
        # 2. Recolectar datos de vuelos
        vuelos_data = self.flight_sensor.get_flight_demand_prediction()
        
        # 3. Recolectar quejas de la competencia
        sentimiento_data = self.sentiment_sensor.get_sentiment_prediction()
        
        print("\n[CEREBRO] 🔄 Cruzando datos estocásticos en LLM Local (Ollama)...")
        
        # Construir el prompt para la IA
        prompt = f"""
        Actúa como el Oráculo Predictivo de Lifextreme AI, un director de inteligencia turística.
        Cruza los siguientes 3 factores del día y genera UNA recomendación estratégica agresiva de ventas 
        para nuestra agencia, priorizando rentabilidad y seguridad. Sé directo (máximo 4 líneas).

        1. CLIMA (SENAMHI): Alerta {clima_data.get('nivel')} - {clima_data.get('fenomeno')}.
        2. VUELOS (DEMANDA): Precio promedio ${vuelos_data['precio_detectado_usd']}. Perfil: {vuelos_data['perfil_demanda']}.
        3. COMPETENCIA (QUEJAS): Los turistas se quejan hoy de: {', '.join(sentimiento_data['quejas_detectadas'][:2])}.
        
        RECOMENDACIÓN DE NEGOCIO:
        """
        
        try:
            response = httpx.post(OLLAMA_URL, json={
                "model": "llama3", # Ajustar según el modelo instalado
                "prompt": prompt,
                "stream": False
            }, timeout=30.0)
            
            if response.status_code == 200:
                decision = response.json().get('response', '')
            else:
                decision = self._algorithmic_decision(clima_data, vuelos_data, sentimiento_data)
        except Exception as e:
            # Si Ollama está apagado, fallback a algoritmo lógico
            print("    [!] Ollama no responde. Ejecutando red neuronal lógica (Fallback).")
            decision = self._algorithmic_decision(clima_data, vuelos_data, sentimiento_data)
            
        print("\n===================================================================")
        print(" 🔮 VEREDICTO PREDICTIVO DIARIO:")
        print("===================================================================")
        print(f"\n{decision}\n")
        print("===================================================================")

    def _algorithmic_decision(self, clima, vuelos, sentimiento):
        # Lógica dura en caso de que el LLM esté apagado
        decision = "ESTRATEGIA SINTÉTICA:\n"
        if "Nevadas" in clima.get('fenomeno', '') or "Lluvias" in clima.get('fenomeno', ''):
            decision += "- ⚠️ Riesgo Climático: CANCELAR trekking (Choquequirao/Vinicunca). Desviar ventas a City Tours y Museos.\n"
        
        if vuelos['precio_detectado_usd'] < 50:
            decision += "- 💰 Demanda Masiva: Subir el presupuesto de Ads en Facebook. Hay volumen alto de turistas llegando.\n"
            
        decision += "- 🗣️ Ventaja Competitiva: Ataca el marketing prometiendo 'Catering Caliente y Transporte Moderno' para aplastar a la competencia."
        return decision

if __name__ == "__main__":
    orquestador = PredictiveOrchestrator()
    orquestador.run_daily_prediction()
