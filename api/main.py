import os
import sys
import json
import requests
from typing import List
from fastapi import FastAPI, HTTPException
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
@app.post("/chat", response_model=LifextremeResponse)
def chat(request: ChatRequest):
    try:
        user_query = request.message
        
        # 1. Ejecutar sensores perimetrales (simulados/ligeros para no demorar la API)
        # Nota: Por motivos de latencia web, solo calculamos el score general
        riesgo = 10
        try:
            correlator = RiskCorrelator()
            # Asumimos "Peru" como region general para el web chat, o extraemos de la pregunta
            riesgo = correlator.calcular_score_regional("Cusco")
        except:
            pass

        # 2. Búsqueda RAG en Supabase
        query_vector = get_local_embedding(user_query)
        res = supabase.rpc(
            "match_knowledge_vectors", 
            {"query_embedding": query_vector, "match_threshold": 0.3, "match_count": 4}
        ).execute()
        
        contextos = res.data if res.data else []
        texto_contexto = "\n---\n".join([c.get("text_content", "") for c in contextos])
        fuentes = list(set([c.get("modulo_nombre", "General") for c in contextos]))
        
        # 3. Prompt Maestro para Phi-3 Local
        master_prompt = f"""
        Eres MAX, Agente Senior de Operaciones Turísticas en Lifextreme Peru.
        Reglas estrictas:
        - Responde SIEMPRE en español, sé sumamente cortés y profesional, como un experto UIAGM.
        - Usa EXCLUSIVAMENTE el siguiente conocimiento recuperado de la base de datos de la empresa para responder.
        - Nivel de riesgo operacional actual: {riesgo}/100.
        
        CONOCIMIENTO DE LA EMPRESA:
        {texto_contexto}
        
        PREGUNTA DEL TURISTA:
        {user_query}
        
        Redacta tu respuesta ejecutiva y amigable al turista.
        """
        
        respuesta_ia = chat_with_phi3(master_prompt)
        
        return LifextremeResponse(
            mensaje_principal=respuesta_ia,
            fuentes_utilizadas=fuentes,
            nivel_confianza=0.95
        )
        
    except Exception as e:
        print(f"Error en el chat local: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "MAX", "mode": "Local Free Operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
