import os
import sys
import json
import requests
from typing import List, Optional, Dict
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

def chat_with_phi3(prompt: str, history: list = None, system_prompt: str = None):
    url = "http://localhost:11434/api/chat"
    
    if system_prompt is not None:
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
    else:
        messages = [{"role": "user", "content": prompt}]

    payload = {
        "model": "phi3:latest",
        "messages": messages,
        "stream": False
    }
    response = requests.post(url, json=payload)
    return response.json().get("message", {}).get("content", "")

# ==========================================
# 3. Modelos de Entrada/Salida
# ==========================================
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class LifextremeResponse(BaseModel):
    mensaje_principal: str
    fuentes_utilizadas: List[str]
    nivel_confianza: float

# ==========================================
# 4. Endpoint Principal
# ==========================================
def retrieve_b2c_context(user_query: str):
    # Búsqueda RAG rápida en Supabase (MAX)
    query_vector = get_local_embedding(user_query)
    res = supabase.rpc(
        "match_knowledge_vectors", 
        {"query_embedding": query_vector, "match_threshold": 0.3, "match_count": 4}
    ).execute()
    
    contextos = res.data if res.data else []
    texto_contexto = "\n---\n".join([c.get("text_content", "") for c in contextos])
    fuentes = list(set([c.get("modulo_nombre", "General") for c in contextos]))
    return texto_contexto, fuentes

# Lazy loader para BGE-M3 para no bloquear inicio de FastAPI
_bge_embedder = None
def get_bge_embedder():
    global _bge_embedder
    if _bge_embedder is None:
        from sentence_transformers import SentenceTransformer
        _bge_embedder = SentenceTransformer('BAAI/bge-m3')
    return _bge_embedder

def retrieve_b2b_context(user_query: str):
    # Búsqueda RAG profunda (Volvemos a usar nomic-embed-text para evitar colapso de RAM)
    query_vector = get_local_embedding(user_query)
    
    res = supabase.rpc(
        'match_knowledge_vectors',
        {
            'query_embedding': query_vector,
            'match_threshold': 0.3,
            'match_count': 4
        }
    ).execute()
    
    resultados = res.data if res.data else []
    contextos_list = []
    fuentes_list = []
    for r in resultados:
        origen = r.get('modulo_nombre', 'Desconocido')
        region = r.get('region', 'Desconocido')
        texto = r.get('text_content', '')
        contextos_list.append(f"ORIGEN: {origen} (REGION: {region})\nCONTENIDO: {texto}")
        fuentes_list.append(f"{origen} ({region})")
        
    texto_contexto = "\n---\n".join(contextos_list)
    fuentes = list(set(fuentes_list))
    return texto_contexto, fuentes

@app.post("/api/v1/b2c/chat", response_model=LifextremeResponse)
def b2c_chat(request: ChatRequest):
    try:
        user_query = request.message
        
        # RAG Conversacional: Si responde algo corto como "julio", no perder el contexto de búsqueda
        search_query = user_query
        if request.history and len(user_query.split()) <= 3:
            for msg in reversed(request.history):
                if msg.get("role") == "user":
                    search_query = msg.get("content", "") + " " + user_query
                    break
        
        riesgo = 10
        try:
            correlator = RiskCorrelator()
            riesgo = correlator.calcular_score_regional("Cusco")
        except:
            pass

        texto_contexto, fuentes = retrieve_b2c_context(search_query)
        
        system_prompt = f"""
        Eres MAX, Asesor de Ventas de Lifextreme Peru. Tu objetivo es chatear como un humano real por WhatsApp.

        REGLAS DE CHAT HUMANO (ESTRICTAS):
        1. CORTEDAD EXTREMA: Tu mensaje debe tener MÁXIMO 2 oraciones. Eres rápido y directo.
        2. PING-PONG: Haz UNA SOLA pregunta corta y termina tu mensaje ahí. NO sigas hablando.
        3. HONESTIDAD: Si el cliente pregunta por un lugar y no tienes detalles precisos en tu "DATA FQSA", responde: "Déjame confirmar con nuestro equipo de operaciones los detalles exactos".
        4. PROHIBICIÓN ABSOLUTA: JAMÁS inventes nombres de lagos, rutas, montañas o parques. Solo menciona lugares que existan en la "DATA FQSA".
        5. RIESGO: {riesgo}/100. Da un tip súper breve de seguridad.
        6. CERO ETIQUETAS: No uses títulos ni listas.

        EJEMPLO DE TU COMPORTAMIENTO ESPERADO:
        "¡Hola! El Cañón de los Perdidos es alucinante, puro desierto y misterio. El clima está perfecto ahora, solo lleven mucha agua. ¿Para qué fechas tienen pensado viajar para ir viendo los cupos?"

        DATA FQSA (Tu Memoria):
        {texto_contexto}
        """
        
        respuesta_ia = chat_with_phi3(prompt=user_query, history=request.history, system_prompt=system_prompt)
        
        return LifextremeResponse(mensaje_principal=respuesta_ia, fuentes_utilizadas=[], nivel_confianza=0.95)
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

        texto_contexto, fuentes = retrieve_b2b_context(user_query)
        
        master_prompt = f"""
# ROL Y MISIÓN
Eres **LIFEXTREME-CORE V3**, el Asesor Estratégico Senior para Agencias Turísticas PYME en Perú.
Tu misión no es dar descripciones turísticas básicas. Tu misión es hacer que el operador GANE MÁS DINERO, reduzca costos logísticos, mitigue riesgos y venda mejor. 
Tienes 50+ años de experiencia. Piensas en márgenes de ganancia, cuellos de botella operativos, nichos de mercado y estrategias de marketing de guerrilla.

# DOMINIOS DE ASESORÍA
Identifica la consulta y responde con extrema profundidad analítica:
  [FIN] Rentabilidad: Estructura de costos, pricing, márgenes y ticket promedio.
  [REG] Regulaciones: MINCETUR, licencias, seguros obligatorios.
  [RIE] Riesgos: Contingencias climáticas, conflictos, planes de rescate.
  [MKT] Marketing: Cómo vender este paquete, a qué nicho apuntar (parejas, corporativo, familias), canales de venta.
  [LOG] Logística: Rutas críticas, proveedores, optimización de tiempos y transporte.

# REGLAS DE ORO (CRÍTICO)
1. CERO RESPUESTAS BÁSICAS: Está estrictamente prohibido dar consejos genéricos como "verifica con transportistas". DAME ESTRATEGIAS COMERCIALES REALES Y TÁCTICAS ACCIONABLES para una PYME.
2. CONTROL DE ALUCINACIONES (RAG): Lee la "DATA FQSA". Si la data entregada NO CORRESPONDE geográficamente al destino que pide el operador (ej. preguntan por Lunahuaná y la data es de la Amazonía/Bolivia), IGNORA COMPLETAMENTE LA DATA FQSA. En ese caso, usa tu "[NIVEL 2 — Conocimiento sectorial]" y decláralo. No mezcles destinos.
3. APORTA VALOR COMERCIAL: Piensa como dueño de negocio. ¿Cómo hago que este tour sea más rentable? ¿Cómo me diferencio de la competencia?

## ESCALA DE RIESGO
Score actual: {riesgo}/100 (Inyéctalo en tu análisis logístico).

# FORMATO DE RESPUESTA
Genera un Reporte Ejecutivo de Inteligencia estructurado usando formato Markdown profesional. Debe lucir como un documento técnico formal de consultoría turística (estilo MINCETUR), pero firmado por nuestra plataforma.

ESTRUCTURA OBLIGATORIA (Usa Markdown real con #, **, y viñetas):

# REPORTE DE INTELIGENCIA OPERATIVA
**Destino/Sector Evaluado:** [Extraer de la consulta]
**Nivel de Riesgo Operativo:** {riesgo}/100

## 📊 ANÁLISIS ESTRATÉGICO
[Tu análisis técnico y financiero profundo, separado en párrafos claros]

## 💡 TÁCTICA PYME ACCIONABLE
[La estrategia concreta de negocio o marketing para el operador]

## ⚠️ CUELLOS DE BOTELLA Y MITIGACIÓN
[El principal riesgo logístico/operativo y exactamente cómo solucionarlo]

---
*Reporte generado de manera autónoma por **LIFEXTREME-CORE AI V3**.*
*Motor de Inteligencia B2B para Turismo Latinoamericano.*

# INPUTS DEL SISTEMA

## DATA FQSA (Recházala si no es del destino):
{texto_contexto}

## CONSULTA DEL OPERADOR:
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
