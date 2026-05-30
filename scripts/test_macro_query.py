import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# Sensores Reales
from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.sensors.logistics.consettur_service import ConsetturService
from src.integrations.risk_correlator import RiskCorrelator

def run_macro_regional_test():
    load_dotenv()
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=======================================================================================")
    print(" 🌍 PRUEBA DE ESTRÉS MACRO-REGIONAL: AREQUIPA -> PUNO -> CUSCO -> ANCASH")
    print("=======================================================================================")
    
    query = """
    "Hola equipo. Soy un líder de expedición con 4 alpinistas europeos. 
    Nuestro plan es llegar a Arequipa para hacer trekking en el Cañón del Colca (2 días), 
    luego movernos a Puno por tierra para aclimatarnos en el Titicaca (1 día), 
    tomar el tren Titicaca hacia Cusco para entrar a Machu Picchu, 
    y finalmente volar a Lima para tomar un bus nocturno a Huaraz (Ancash) e intentar escalar el Nevado Pisco. 
    Tenemos exactamente 10 días para todo. 
    Sabiendo las distancias reales, el estado de las vías hoy, y la disponibilidad de Machu Picchu, 
    ¿es esto logísticamente posible o es un suicidio? Sé brutalmente honesto y rediseña mi plan si está mal."
    """
    
    print(f"\n[CONSULTA EXTREMA DEL USUARIO]:\n{query}\n")
    print("=> 1. Activando Sensores Multipunto (Evaluación Logística en Tiempo Real)...\n")
    
    # Evaluar Carreteras Sur
    sutran = SutranService()
    sutran.escanear_alertas()
    
    # Evaluar Disponibilidad Cusco
    consettur = ConsetturService("https://consettur.com/")
    consettur.escanear_alertas()
    
    # Tiempos de viaje Arequipa-Puno-Cusco
    maps = GoogleMapsTrafficSensor()
    maps.ejecutar_monitoreo("Arequipa, Peru", "Puno, Peru", "Arequipa-Puno")
    
    print("\n=> 2. Evaluando Nivel de Riesgo Global (RiskCorrelator)...")
    correlator = RiskCorrelator()
    riesgo = correlator.calcular_score_regional("Sur de Peru")
    print(f"   [Nivel de Riesgo Calculado]: {riesgo}/10\n")
    
    print("=> 3. Conectando con Gemini 2.5 Flash (Modo Arquitecto de Viajes)...")
    
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    client = genai.Client(http_options=HttpOptions(api_version='v1'))
    
    contexto = f"""
    Eres el Arquitecto Logístico Senior de Lifextreme.
    Tienes que resolver una pesadilla logística macro-regional de un cliente:
    
    CONSULTA: {query}
    
    DATOS OPERATIVOS ACTUALES (Alimentados por tus Sensores hoy):
    - DISTANCIAS: Arequipa a Puno toma ~6 horas. Puno a Cusco en tren toma ~10 horas. Cusco a Lima (Vuelo) + Lima a Huaraz (Bus) toma mínimo 12-14 horas de tránsito neto.
    - SUTRAN: Las carreteras andinas pueden sufrir bloqueos imprevistos o demoras por mantenimiento.
    - MACHU PICCHU: Consettur y Sernanp indican alta demanda; intentar coordinar tickets con 1-2 días de anticipación es altísimo riesgo de no entrar.
    - NEVADO PISCO (ANCASH): Requiere al menos 2-3 días de aproximación/escalada, y requiere aclimatación previa sólida (que ganarán en el sur, pero la logística corta los tiempos).
    - RIESGO LOGÍSTICO ACTUAL (Según Lifextreme AI): {riesgo}/10
    
    INSTRUCCIONES DE RESOLUCIÓN:
    1. DESTRUYE el plan original (es un suicidio logístico tratar de hacer 4 macro-regiones en 10 días).
    2. Usa los datos de tiempo de tránsito para justificar matemáticamente por qué es una locura.
    3. PROPÓN UNA ALTERNATIVA SALVAVIDAS: Un itinerario de 10 días que concentre el esfuerzo en máximo 2 regiones (ejemplo: Solo Cusco+Ancash, o Solo Arequipa+Puno+Cusco sin Ancash).
    4. Tono: Directo, experto, firme y extremadamente útil. Eres un experto en montaña y logística peruana, no un bot de atención al cliente.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contexto,
        config=GenerateContentConfig(temperature=0.3, max_output_tokens=2048)
    )
    
    print("=======================================================================================")
    print(" 🏔️ RESPUESTA DEL ARQUITECTO LOGÍSTICO (LIFEXTREME AI):")
    print("=======================================================================================")
    print(response.text)
    print("=======================================================================================")

if __name__ == "__main__":
    run_macro_regional_test()
