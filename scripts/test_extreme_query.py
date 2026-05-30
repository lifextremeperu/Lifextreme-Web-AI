import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# Sensores
from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.risk_correlator import RiskCorrelator

def run_extreme_test():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=======================================================================================")
    print(" 🚨 SIMULACIÓN EXTREMA EN TIEMPO REAL: AGENTE DE VENTAS + INTELIGENCIA OPERATIVA")
    print("=======================================================================================")
    
    query = """
    "Tengo un grupo VIP de 8 turistas corporativos. Tienen vuelo de llegada mañana a Cusco, 
    quieren visitar Machu Picchu, y luego hacer la Ruta del Sol terrestre hasta Puno, 
    porque tienen un vuelo internacional que sale desde el aeropuerto de Juliaca en 3 días. 
    He escuchado rumores de bloqueos en la carretera Cusco-Puno por paros agrarios. 
    ¿Es seguro? ¿Qué alternativas y plan B exacto me recomiendas para que no pierdan su vuelo 
    internacional, considerando la situación de las carreteras y riesgos al día de hoy?"
    """
    
    print(f"\n[QUERY DEL USUARIO]:\n{query}\n")
    print("=> 1. Activando Sensores Perimetrales...\n")
    
    # 1. Ejecutar Sensores para alimentar el contexto
    sutran = SutranService()
    sutran.escanear_alertas()
    
    gdelt = GdeltCrisisSensor()
    gdelt.ejecutar_monitoreo(pais="PE", region_objetivo="Puno")
    
    maps = GoogleMapsTrafficSensor()
    maps.ejecutar_monitoreo("Cusco, Peru", "Puno, Peru", "Puno")
    
    print("\n=> 2. Evaluando Nivel de Riesgo (RiskCorrelator)...")
    correlator = RiskCorrelator()
    riesgo = correlator.calcular_score_regional("Puno")
    print(f"   [Nivel de Riesgo Calculado]: {riesgo}/100\n")
    
    print("=> 3. Conectando con Gemini 2.5 Flash para Resolución Estratégica...")
    
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    client = genai.Client(http_options=HttpOptions(api_version='v1'))
    
    # Prompt Maestro de Resolución
    contexto = f"""
    Eres el Agente Senior de Operaciones de Lifextreme.
    Tienes que responder a esta consulta crítica de un usuario:
    CONSULTA: {query}
    
    DATOS EN TIEMPO REAL DE TUS SENSORES AHORA MISMO:
    - SUTRAN / MTC: Reporta vías con posible tránsito restringido por manifestaciones sociales.
    - GDELT (Noticias Globales): Nivel de tensión alto en Puno y carreteras de la sierra sur.
    - SCORE DE RIESGO LIFEXTREME: {riesgo}/100 (Considerado Riesgo Alto).
    
    INSTRUCCIONES:
    1. Responde de forma directa y ejecutiva.
    2. Usa los datos en tiempo real de los sensores para tomar tu decisión.
    3. Si el riesgo es alto, RECOMIENDA UN PLAN B LOGÍSTICO INMEDIATO (ej: desvío por Arequipa, cambio a tren PeruRail, o cancelación de ruta terrestre y tomar vuelo Cusco-Juliaca/Lima).
    4. Actúa como el experto absoluto. No dudes.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contexto,
        config=GenerateContentConfig(temperature=0.4, max_output_tokens=1024)
    )
    
    print("=======================================================================================")
    print(" 🤖 RESPUESTA DE LA INTELIGENCIA ARTIFICIAL LIFEXTREME:")
    print("=======================================================================================")
    print(response.text)
    print("=======================================================================================")

if __name__ == "__main__":
    run_extreme_test()
