import os
import sys
import json
import requests
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# Agregar ruta para que reconozca la carpeta src
sys.path.append(str(Path(__file__).resolve().parent.parent))

from supabase import create_client, Client

# Integraciones Locales (Sensores)
from src.integrations.sensors.maps_sensor import GoogleMapsTrafficSensor
from src.integrations.sensors.logistics.sutran_service import SutranService
from src.integrations.sensors.risk.gdelt_sensor import GdeltCrisisSensor
from src.integrations.risk_correlator import RiskCorrelator

# ==========================================
# 1. Configuración de API y BD Local
# ==========================================
app = FastAPI(title="Lifextreme AI Local API (Free Operational)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# ==========================================
# 1.5. API KEY Security
# ==========================================
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)):
    # Usaremos una clave por defecto si no está en el .env para poder probar hoy
    expected_key = os.getenv("LIFEXTREME_B2B_API_KEY", "LIFEXTREME-TEST-KEY-2026")
    if api_key == expected_key:
        return api_key
    raise HTTPException(status_code=403, detail="Acceso denegado: API Key inválida o faltante")

# ==========================================
# 2. Motores IA Locales (Ollama)
# ==========================================
def get_local_embedding(text):
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model": "nomic-embed-text", "input": text})
    return response.json().get("embeddings", [])[0]

def chat_with_phi3(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "phi3:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json().get("message", {}).get("content", "")

# ==========================================
# 3. Modelos de Entrada/Salida
# ==========================================
class ChatRequest(BaseModel):
    message: str

class LifextremeResponse(BaseModel):
    mensaje_principal: str
    fuentes_utilizadas: List[str]
    nivel_confianza: float

# ==========================================
# 4. Endpoint Principal
# ==========================================
def retrieve_and_format_context(user_query: str):
    # Búsqueda RAG en Supabase
    query_vector = get_local_embedding(user_query)
    res = supabase.rpc(
        "match_knowledge_vectors", 
        {"query_embedding": query_vector, "match_threshold": 0.3, "match_count": 4}
    ).execute()
    
    contextos = res.data if res.data else []
    texto_contexto = "\n---\n".join([c.get("text_content", "") for c in contextos])
    fuentes = list(set([c.get("modulo_nombre", "General") for c in contextos]))
    return texto_contexto, fuentes

@app.post("/api/v1/b2c/chat", response_model=LifextremeResponse)
def b2c_chat(request: ChatRequest):
    try:
        user_query = request.message
        riesgo = 10
        try:
            correlator = RiskCorrelator()
            riesgo = correlator.calcular_score_regional("Cusco")
        except:
            pass

        texto_contexto, fuentes = retrieve_and_format_context(user_query)
        
        master_prompt = f"""
        Eres MAX, Asesor Turístico Experto de Lifextreme Peru.
        Reglas estrictas:
        - Responde SIEMPRE en español con un tono sumamente empático, amigable y servicial.
        - Dirígete a un turista (B2C) que quiere disfrutar su viaje pero requiere seguridad.
        - Nivel de riesgo operacional actual: {riesgo}/100.
        - Usa el siguiente contexto, pero NO lo menciones explícitamente como "datos", úsalo naturalmente para aconsejar.
        
        CONTEXTO:
        {texto_contexto}
        
        PREGUNTA DEL TURISTA:
        {user_query}
        """
        
        respuesta_ia = chat_with_phi3(master_prompt)
        
        return LifextremeResponse(mensaje_principal=respuesta_ia, fuentes_utilizadas=fuentes, nivel_confianza=0.95)
    except Exception as e:
        print(f"Error en chat B2C: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/b2b/query", response_model=LifextremeResponse)
def b2b_query(request: ChatRequest, api_key: str = Depends(get_api_key)):
    try:
        user_query = request.message
        riesgo = 10
        try:
            correlator = RiskCorrelator()
            riesgo = correlator.calcular_score_regional("Cusco")
        except:
            pass

        texto_contexto, fuentes = retrieve_and_format_context(user_query)
        
        master_prompt = f"""
        Eres LIFEXTREME-CORE, Analista Estratégico y Logístico de Operaciones.
        Reglas estrictas:
        - Responde a un Operador Turístico o Inversionista (B2B) en tono corporativo, frío, directo y analítico.
        - Enfócate en la viabilidad, presupuesto, logística de rutas y riesgos operacionales.
        - Nivel de riesgo operacional actual: {riesgo}/100.
        - Usa el contexto recuperado (FQSAs) para generar un micro-reporte estratégico.
        
        DATA MINADA (PERTUR/FQSAs):
        {texto_contexto}
        
        CONSULTA DEL OPERADOR:
        {user_query}
        """
        
        respuesta_ia = chat_with_phi3(master_prompt)
        
        return LifextremeResponse(mensaje_principal=respuesta_ia, fuentes_utilizadas=fuentes, nivel_confianza=0.95)
    except Exception as e:
        print(f"Error en query B2B: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "MAX", "mode": "Local Free Operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
