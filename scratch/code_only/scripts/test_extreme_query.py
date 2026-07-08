import os
import sys
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Supabase Client
from supabase import create_client, Client

# ==========================================
# SENSORES EN TIEMPO REAL (LIFEXTREME)
# ==========================================
from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
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

def chat_with_deepseek(prompt):
    """Habla con el modelo Deepseek alojado localmente en Ollama usando la API de chat"""
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

def run_extreme_test():
    sys.stdout.reconfigure(encoding='utf-8')
    supabase = init_supabase()
    
    print("=======================================================================================")
    print(" 🚨 SIMULACIÓN EXTREMA: RAG (SUPABASE) + SENSORES EN TIEMPO REAL + IA LOCAL")
    print("=======================================================================================")
    
    query = """
    "Hola, viajo mañana a Huaraz (Ancash) con mis padres de 65 años. Queremos hacer el trekking 
    a la Laguna 69, pero he leído que hay huelgas en las carreteras de la sierra y que ha estado 
    lloviendo mucho. ¿Es seguro para ellos? Si la ruta está bloqueada o es muy pesada por la altura, 
    ¿qué plan B tranquilo y seguro nos recomiendas en Ancash, considerando las condiciones de hoy?"
    """
    
    print(f"\n[QUERY DEL USUARIO]:\n{query}\n")
    
    print("=> 1. Activando Sensores Perimetrales (SUTRAN, GDELT, MAPS)...\n")
    try:
        sutran = SutranService()
        sutran.escanear_alertas()
        
        gdelt = GdeltCrisisSensor()
        gdelt.ejecutar_monitoreo(pais="PE", region_objetivo="Ancash")
        
        maps = GoogleMapsTrafficSensor()
        maps.ejecutar_monitoreo("Lima, Peru", "Huaraz, Peru", "Ancash")
        
        print("\n=> 2. Evaluando Nivel de Riesgo (RiskCorrelator)...")
        correlator = RiskCorrelator()
        riesgo = correlator.calcular_score_regional("Ancash")
        print(f"   [Nivel de Riesgo Calculado]: {riesgo}/100\n")
    except Exception as e:
        print(f"[-] Advertencia con los sensores: {e}")
        riesgo = 15 # Valor por defecto

    print("=> 3. Buscando Conocimiento Estratégico en Supabase (Vectores)...")
    query_vector = get_local_embedding(query)
    
    response = supabase.rpc("match_knowledge_vectors", {
        "query_embedding": query_vector,
        "match_threshold": 0.3, 
        "match_count": 3 
    }).execute()
    
    contexto_db = ""
    for match in response.data:
        contexto_db += f"- [{match['modulo_nombre']}]: {match['text_content']}\n"
    
    print("=> 4. Conectando con Deepseek-v2 (Cerebro Local) para Resolución Estratégica...")
    
    # Prompt Maestro Híbrido: RAG + Sensores
    prompt_maestro = f"""
    Eres el Agente Senior de Operaciones de Lifextreme. Tienes que responder a esta consulta crítica:
    CONSULTA: {query}
    
    DATOS EN TIEMPO REAL DE TUS SENSORES AHORA MISMO:
    - SUTRAN / MTC: Reporta vías con posible tránsito restringido por manifestaciones sociales.
    - GDELT (Noticias Globales): Nivel de tensión alto en Puno y carreteras de la sierra sur.
    - SCORE DE RIESGO LIFEXTREME: {riesgo}/100.
    
    CONOCIMIENTO ESTRATÉGICO DE LA BASE DE DATOS LIFEXTREME (RAG):
    {contexto_db}
    
    INSTRUCCIONES:
    1. Responde de forma directa y ejecutiva.
    2. Usa TANTO los datos de la base de datos (RAG) como la información de los sensores en tiempo real para tomar tu decisión.
    3. Si el riesgo es alto (como indica el score), RECOMIENDA UN PLAN B LOGÍSTICO INMEDIATO (ej: desvío, tren, o vuelo) basándote en la base de datos.
    4. Actúa como el experto absoluto. No dudes.
    """
    
    respuesta_final = chat_with_deepseek(prompt_maestro)
    
    print("=======================================================================================")
    print(" 🤖 RESPUESTA DE DEEPSEEK (AGENTE OPERATIVO LIFEXTREME):")
    print("=======================================================================================")
    print(respuesta_final)
    print("=======================================================================================")

if __name__ == "__main__":
    run_extreme_test()
