import sys
import time
import os
import glob
import json
from pathlib import Path
from dotenv import load_dotenv

# Configurar UTF-8 para la consola de Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.risk_correlator import RiskCorrelator

def animate_text(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    load_dotenv()
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'lifextreme-arequipa-agent'
    os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    print("\n" + "═"*80)
    print(" 🧠 LIFEXTREME OS - CEREBRO MAESTRO v2.0 (LIVE DEMO OPERADOR)")
    print("═"*80 + "\n")
    
    pregunta_operador = "Tengo un grupo de 8 turistas listos para salir a la Montaña de 7 Colores (Vinicunca) mañana a las 4 AM. Hay rumores de huelga de transportistas en la ruta sur (Sicuani/Pitumarca). Si cancelamos, perdemos $800 de utilidad. ¿Es seguro ir? Si no, ¿qué alternativa equivalente del Lóbulo B2C les ofrezco inmediatamente para no perder la venta?"
    
    animate_text(f"🗣️ CASO REAL DE OPERACIONES: \n\"{pregunta_operador}\"\n")
    time.sleep(1)
    
    # ---------------------------------------------------------
    # 1. ACTIVACIÓN DE SENSORES DE CAMPO EN TIEMPO REAL
    # ---------------------------------------------------------
    print("🛰️ [FASE 1] DESPLEGANDO SENSORES DE LOGÍSTICA Y SEGURIDAD...")
    
    print("   -> 🚨 Sensor de Carreteras (SUTRAN / Tráfico):")
    maps = GoogleMapsTrafficSensor()
    trafico = maps.ejecutar_monitoreo("Cusco", "Vinicunca", "Cusco")
    
    print("   -> 📉 Sensor de Conflictos Sociales (GDELT / Cusco Sur):")
    gdelt = GdeltCrisisSensor()
    crisis = gdelt.ejecutar_monitoreo(pais="PE", region_objetivo="Cusco")
    
    print("   -> 🧮 Motor de Riesgo Operativo (Risk Correlator):")
    correlator = RiskCorrelator()
    riesgo = correlator.calcular_score_regional("Cusco")
    time.sleep(1)
    
    # ---------------------------------------------------------
    # 2. RECUPERACIÓN DE ALTERNATIVAS B2C (Cerebro Local)
    # ---------------------------------------------------------
    print("\n📚 [FASE 2] BUSCANDO PLAN 'B' EN LA BASE DE DATOS FQSA (Lóbulo B2C)...")
    # Simulamos leer un FQSA del Valle Sagrado o Palccoyo
    alternativa_data = "Valle Sagrado VIP y Salineras de Maras: Ruta pavimentada, sin bloqueos reportados. Precio promedio superior. Altitud moderada, ideal para familias. Atractivo visual alto."
    
    try:
        # Intenta leer un JSON real de Cusco si existe
        archivos_cusco = glob.glob("data/knowledge/cusco/fqsas_deep/*.json")
        if archivos_cusco:
            with open(archivos_cusco[0], "r", encoding="utf-8") as f:
                data = json.load(f)
                alternativa_data = str(data.get("fqsas", "Alternativa: Valle Sagrado"))[:500]
            print(f"   ✅ Se encontró módulo turístico alternativo en la BD de Cusco.")
    except:
        print("   ✅ Alternativa de contingencia cargada desde la memoria base.")
    time.sleep(1)

    # ---------------------------------------------------------
    # 3. RAZONAMIENTO DEL LLM (Decisión Ejecutiva)
    # ---------------------------------------------------------
    print("\n🧠 [FASE 3] MOTOR DE DECISIÓN NEURAL (GEMINI 2.5 FLASH)...")
    animate_text("   Cruzando riesgo de carretera, clima y catálogo de ventas para armar respuesta...")
    
    prompt = f"""
    Eres el Gerente de Operaciones de Inteligencia Artificial de Lifextreme.
    Un operador humano tiene este problema urgente: "{pregunta_operador}"
    
    DATOS DE SENSORES EN VIVO:
    - Tráfico / SUTRAN: {trafico}
    - Reporte GDELT (Conflictos): {crisis}
    - Nivel de Riesgo Regional: {riesgo}
    
    DATOS DE LA BASE DE CONOCIMIENTO B2C (Para Plan B):
    {alternativa_data}
    
    Escribe un mensaje de respuesta directa al operador. 
    1. Da una instrucción CLARA: ¿Se cancela la salida a Vinicunca por seguridad operativa?
    2. Usa la táctica comercial: Redacta exactamente el mensaje (pitch) que el operador debe enviarle al cliente por WhatsApp para cambiar el tour al Plan B sin que pidan reembolso (usando los datos B2C).
    Sé muy profesional y ejecutivo.
    """
    
    try:
        client = genai.Client(http_options=HttpOptions(api_version='v1'))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=GenerateContentConfig(temperature=0.3)
        )
        
        print("\n" + "═"*80)
        print(" 📊 ORDEN DE OPERACIONES - LIFEXTREME IA")
        print("═"*80)
        animate_text(response.text.strip(), delay=0.015)
        print("═"*80)
        
    except Exception as e:
        print(f"\n[-] Error de conexión con Vertex AI: {e}")

if __name__ == "__main__":
    main()

