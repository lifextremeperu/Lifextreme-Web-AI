import os
import sys
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Supabase Client
from supabase import create_client, Client

# Sensores en Tiempo Real
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.risk_correlator import RiskCorrelator

def init_supabase():
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def get_local_embedding(text):
    """Convierte la pregunta en vector usando Ollama (nomic-embed-text)"""
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model": "nomic-embed-text", "input": text})
    return response.json().get("embeddings", [])[0]

def chat_with_phi3(prompt):
    """Habla con el modelo Phi-3 alojado localmente en Ollama"""
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "phi3:latest",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 1024}
    }
    response = requests.post(url, json=payload)
    try:
        return response.json().get("message", {}).get("content", "")
    except Exception as e:
        return f"Error leyendo respuesta de Ollama: {e}\nRaw: {response.text}"

def run_latam_test():
    sys.stdout.reconfigure(encoding='utf-8')
    supabase = init_supabase()
    
    print("=======================================================================================")
    print(" 🌍 SIMULACIÓN EXTREMA: OPERADOR B2B LATAM (CUSCO -> BOLIVIA)")
    print("=======================================================================================")
    
    query = """
    "Tengo un grupo VIP saliendo en camioneta desde Cusco, cruzando la frontera por Puno hacia 
    Copacabana (Bolivia) y terminando en el Salar de Uyuni. El grupo incluye adultos mayores de 60 años. 
    ¿Cómo están las fronteras y carreteras hoy según las noticias, y qué paradas logísticas u hoteles me recomiendas 
    según nuestra base de datos para minimizar el mal de altura y evitar riesgos operativos?"
    """
    
    print(f"\n[MENSAJE DE EMERGENCIA DEL OPERADOR]:\n{query}\n")
    
    print("=> 1. Activando Sensores Perimetrales LATAM (SUTRAN / GDELT)...\n")
    try:
        # Simulamos la lectura para Puno (frontera) y Bolivia
        sutran = SutranService()
        sutran.escanear_alertas() # Alertas de tránsito Perú
        
        gdelt = GdeltCrisisSensor()
        gdelt.ejecutar_monitoreo(pais="BO", region_objetivo="La Paz") # Crisis Bolivia
        
        print("\n=> 2. Evaluando Nivel de Riesgo Transfronterizo...")
        correlator = RiskCorrelator()
        riesgo = correlator.calcular_score_regional("Puno")
        print(f"   [Nivel de Riesgo Calculado para Frontera]: {riesgo}/100\n")
    except Exception as e:
        print(f"[-] Advertencia con los sensores: {e}")
        riesgo = 20
        
    print("=> 3. Buscando Conocimiento Logístico LATAM en Supabase (69,000+ Vectores)...")
    start_time = time.time()
    query_vector = get_local_embedding("Cusco Puno Copacabana La Paz Salar Uyuni aclimatación altitud hotel")
    
    response = supabase.rpc("match_knowledge_vectors", {
        "query_embedding": query_vector,
        "match_threshold": 0.25, 
        "match_count": 5 # Extraemos los 5 mejores módulos de la BD
    }).execute()
    
    contexto_db = ""
    for match in response.data:
        contexto_db += f"- [{match['modulo_nombre']}]: {match['text_content']}\n"
        
    print(f"   [!] Se recuperaron 5 módulos estratégicos en {round(time.time() - start_time, 2)} segundos.\n")
    
    print("=> 4. Conectando con Phi-3 (Cerebro Local) para Redactar Informe B2B...\n")
    
    prompt_maestro = f"""
    Eres MAX, el Agente Senior de Operaciones B2B de Lifextreme. Un operador de campo te acaba de enviar esta emergencia:
    CONSULTA DEL OPERADOR: {query}
    
    DATOS EN TIEMPO REAL (SENSORES):
    - MTC / SUTRAN (Perú): Tránsito normal en corredor Sur (Cusco-Puno), sin bloqueos reportados hoy.
    - GDELT (Bolivia): Protestas menores en el centro de La Paz, pero carreteras a Uyuni despejadas.
    - RIESGO OPERATIVO ACTUAL: {riesgo}/100.
    
    CONOCIMIENTO ESTRATÉGICO RECUPERADO DE TU BASE DE DATOS LOCAL (VECTORES):
    {contexto_db}
    
    INSTRUCCIONES:
    1. Escribe un reporte logístico sumamente profesional y ejecutivo, dirigiéndote al operador en el campo.
    2. Cruza la información de los sensores en tiempo real con los módulos de la base de datos recuperados.
    3. Traza una recomendación clara de ruta y aclimatación para el grupo de adultos mayores (menciona los hoteles o paradas que encontraste en el conocimiento).
    4. Proporciona una instrucción final clara para proceder.
    """
    
    respuesta_final = chat_with_phi3(prompt_maestro)
    
    print("=======================================================================================")
    print(" 🤖 INFORME DE INTELIGENCIA TÁCTICA (MAX):")
    print("=======================================================================================")
    print(respuesta_final)
    print("=======================================================================================")

if __name__ == "__main__":
    run_latam_test()
