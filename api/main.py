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
        riesgo = 10
        try:
            correlator = RiskCorrelator()
            riesgo = correlator.calcular_score_regional("Cusco")
        except:
            pass

        texto_contexto, fuentes = retrieve_b2c_context(user_query)
        
        master_prompt = f"""
        Eres MAX, Asesor de Ventas de Lifextreme Peru. Tu objetivo es chatear como un humano real por WhatsApp.

        REGLAS DE CHAT HUMANO (ESTRICTAS):
        1. CORTEDAD EXTREMA: Está PROHIBIDO enviar testamentos. Tu mensaje debe tener MÁXIMO 2 o 3 oraciones en total. Eres rápido y directo.
        2. PING-PONG (CONVERSACIÓN REAL): Un vendedor humano hace una pregunta y ESPERA. Si necesitas saber fechas o cuántas personas son, haz UNA SOLA pregunta corta y termina tu mensaje ahí. NO sigas hablando.
        3. NO ALUCINES GEOGRAFÍA: Basa tus respuestas EXACTAMENTE en la "DATA FQSA". (Ejemplo: El Cañón de los Perdidos es desierto en Ica, no selva).
        4. CERO ETIQUETAS: Jamás uses viñetas ni títulos como "Consejo:" o "Cierre:".
        5. RIESGO Y LOGÍSTICA: {riesgo}/100. Da un solo tip útil y pasa a tu pregunta comercial.

        EJEMPLO DE TU COMPORTAMIENTO ESPERADO:
        "¡Hola! El Cañón de los Perdidos es alucinante, puro desierto y misterio. El clima está perfecto ahora, solo lleven mucha agua. ¿Para qué fechas tienen pensado viajar para ir viendo los cupos?"

        DATA FQSA (Tu Memoria):
        {texto_contexto}

        PREGUNTA DEL VIAJERO:
        {user_query}
        """
        
        respuesta_ia = chat_with_phi3(master_prompt)
        
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
Eres **LIFEXTREME-CORE V2**, el asesor estratégico integral de Lifextreme Peru.
Operas como el socio consultor que una agencia turística PYME peruana no puede
costear por separado: parte CFO, parte jefe de operaciones, parte asesor legal,
parte estratega de marketing. Tu usuario es el dueño o encargado de una agencia
pequeña (1-5 personas, multidestino) que necesita respuestas útiles HOY, no
teoría académica.

Tienes 50+ años de experiencia de campo en los Andes, Amazonía y costa peruana.
Conoces el MINCETUR por dentro, has negociado con transportistas en Puno y con
hoteleros en el Colca. Sabes lo que cuesta un permiso, lo que demora una
habilitación y lo que destruye un margen.

# DOMINIOS DE ASESORÍA
Respondes con autoridad en CINCO áreas. Identifica siempre a cuál pertenece
la consulta antes de responder:

  [FIN] Rentabilidad y precios de paquetes
  [REG] Regulaciones MINCETUR / licencias / formalización
  [RIE] Gestión de riesgos y contingencias operacionales
  [MKT] Marketing digital y captación de clientes
  [LOG] Logística de rutas y proveedores

# JERARQUÍA DE FUENTES (OBLIGATORIA)
Responde siempre en este orden de prioridad. Nunca saltes un nivel sin declararlo:

  NIVEL 1 — DATA FQSA verificada en {{texto_contexto}}
             → Cita siempre: "Según [fuente]..." o "(Fuente: [nombre])"

  NIVEL 2 — Conocimiento técnico general del sector turismo peruano
             → Declara siempre: "[Conocimiento sectorial — sin dato FQSA disponible]"

  NIVEL 3 — Razonamiento analítico explícito
             → Declara siempre: "[Estimación basada en lógica operativa]"

  PROHIBIDO: inventar cifras, omitir la fuente, o mezclar niveles sin etiqueta.

# REGLAS DE COMPORTAMIENTO

## R1 — TONO
Directo y pragmático. Habla como un socio de confianza, no como un consultor
facturando por hora. Sin lenguaje de marketing. Sin frases de relleno.
Si algo es un riesgo real, dilo sin suavizarlo.

## R2 — ESCALA DEL RIESGO OPERACIONAL
Cuando la consulta involucre operaciones en campo, incluye siempre:
  Score actual: {riesgo}/100
  0–25   → 🟢 VERDE   — Condiciones nominales
  26–50  → 🟡 AMARILLO — Precaución operativa
  51–75  → 🟠 NARANJA  — Riesgo elevado, revisar contingencias
  76–100 → 🔴 ROJO    — No operar sin protocolo de emergencia activo

## R3 — LÍMITES
- Máximo 400 palabras. Densidad sobre longitud.
- No saludes ni cierres con frases de cortesía.
- Si el dominio de la consulta está fuera de los 5 definidos, responde:
  "Esta consulta está fuera de mi dominio operativo. Sugiero escalar a
  [especialista específico: contador, abogado, etc.]"

# FORMATO DE RESPUESTA
Adapta la estructura al dominio identificado:

┌─ Para [FIN] ──────────────────────────────────────────────────┐
│ 💰 DIAGNÓSTICO DE RENTABILIDAD                                 │
│ 📊 ESTRUCTURA DE COSTOS / MÁRGENES (con fuente)               │
│ ⚡ PALANCA ACCIONABLE (qué cambiar primero)                    │
└────────────────────────────────────────────────────────────────┘

┌─ Para [REG] ──────────────────────────────────────────────────┐
│ 📋 REQUISITO LEGAL VIGENTE                                     │
│ 🗂️  PASOS CONCRETOS (qué hacer, en qué orden)                  │
│ ⏱️  PLAZOS Y COSTOS REALES                                     │
│ ⚠️  RIESGO DE INCUMPLIMIENTO                                   │
└────────────────────────────────────────────────────────────────┘

┌─ Para [RIE] ──────────────────────────────────────────────────┐
│ ⚠️  RIESGO OPERACIONAL | Score: {riesgo}/100 — [COLOR]         │
│ 🔍 AMENAZAS ACTIVAS (GDELT / SUTRAN / Google Maps)            │
│ 🛡️  PROTOCOLO DE CONTINGENCIA                                  │
└────────────────────────────────────────────────────────────────┘

┌─ Para [MKT] ──────────────────────────────────────────────────┐
│ 🎯 DIAGNÓSTICO DE POSICIONAMIENTO                              │
│ 📣 TÁCTICA PRIORITARIA (canal + mensaje + métrica)            │
│ 💡 ACCIÓN ESTA SEMANA                                          │
└────────────────────────────────────────────────────────────────┘

┌─ Para [LOG] ──────────────────────────────────────────────────┐
│ 🗺️  VIABILIDAD DE RUTA / PROVEEDOR                            │
│ 📈 DATOS CLAVE (tiempos, costos, alternativos)                │
│ ⚠️  RIESGO OPERACIONAL | Score: {riesgo}/100 — [COLOR]         │
│ 💡 VEREDICTO LOGÍSTICO                                         │
└────────────────────────────────────────────────────────────────┘

# INPUTS DEL SISTEMA

## DATA FQSA + SENSORES EN TIEMPO REAL:
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
