from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import logging

# IMPORTANTE: Instalar dependencias antes de ejecutar
# pip install fastapi uvicorn qdrant-client requests

try:
    from qdrant_client import QdrantClient
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Procasa RAG Backend (Qdrant + DeepSeek)")

# Habilitar CORS para que el HTML pueda consumir esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de Qdrant (Ajusta la URL y el nombre de tu colección)
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "procasa_knowledge"

# Modelo de petición esperado del PMV
class ChatRequest(BaseModel):
    prompt: str

def buscar_contexto_en_qdrant(query_text: str):
    """
    Busca en los 330k vectores de Qdrant los textos más relevantes a la pregunta.
    """
    if not QDRANT_AVAILABLE:
        logger.warning("Librería qdrant-client no instalada. Omitiendo RAG.")
        return ""

    try:
        # 1. Conectar a Qdrant
        client = QdrantClient(url=QDRANT_URL, timeout=5.0)
        
        # OJO: Para buscar texto, necesitas convertir el "query_text" en un vector (embedding) primero.
        # Aquí asumimos que usas un modelo ligero de embeddings (Ollama o HuggingFace).
        # Por simplicidad, simularemos la obtención del vector (Debes reemplazar esto con tu generador real de embeddings):
        vector_query = [0.0] * 384 # Vector simulado
        
        # 2. Buscar en Qdrant
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector_query,
            limit=3
        )
        
        # 3. Concatenar los textos encontrados
        contexto_recuperado = "\n".join([hit.payload.get("texto", "") for hit in search_result])
        return contexto_recuperado
        
    except Exception as e:
        logger.error(f"Error conectando a Qdrant en {QDRANT_URL}: {e}")
        return ""

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"Pregunta del usuario: {request.prompt}")
    
    # 1. Recuperar Contexto (RAG - Retrieval)
    contexto = buscar_contexto_en_qdrant(request.prompt)
    
    # 2. Construir el Prompt Enriquecido para DeepSeek
    if contexto.strip():
        system_prompt = (
            "Eres el Asesor IA experto de la inmobiliaria Procasa. "
            "Usa la siguiente información recuperada de nuestra base de datos para responder a la pregunta del cliente. "
            "Si la información no es suficiente, usa tu conocimiento general pero mantén un tono profesional y enfocado en ventas inmobiliarias en Cusco.\n\n"
            f"INFORMACIÓN RECUPERADA (Cerebro Qdrant):\n{contexto}\n\n"
        )
        prompt_final = f"{system_prompt}Pregunta del cliente: {request.prompt}"
        logger.info("RAG activado: Contexto inyectado en el prompt.")
    else:
        # Fallback si Qdrant falla o está vacío
        prompt_final = (
            "Eres el Asesor IA experto de la inmobiliaria Procasa. "
            "Responde de forma profesional, amigable y enfocada en neuromarketing inmobiliario en Cusco. "
            f"Pregunta del cliente: {request.prompt}"
        )
        logger.info("Sin RAG: Usando prompt base.")

    # 3. Enviar al LLM local (DeepSeek vía Ollama)
    try:
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder", # o el modelo más rápido que tengas
                "prompt": prompt_final,
                "stream": False
            },
            timeout=30.0
        )
        ollama_response.raise_for_status()
        data = ollama_response.json()
        respuesta_ia = data.get("response", "Lo siento, tuve un problema procesando la información.")
        
        return {"response": respuesta_ia}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error conectando a Ollama: {e}")
        return {"response": "Error: El cerebro de DeepSeek (Ollama) no está respondiendo en el puerto 11434."}

# Para ejecutar:
# uvicorn backend_rag:app --host 0.0.0.0 --port 8000 --reload
