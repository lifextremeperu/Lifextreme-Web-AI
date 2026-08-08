from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import logging

from qdrant_client import QdrantClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Lifextreme CEO Backend (Qdrant + Ollama)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_CEO = "Lifextreme_CEO_Vault"
OLLAMA_GENERATE = "http://127.0.0.1:11434/api/generate"
OLLAMA_EMBED = "http://127.0.0.1:11434/api/embed"
MODEL_CHAT = "phi3:latest"
MODEL_EMBED = "nomic-embed-text"

class ChatRequest(BaseModel):
    prompt: str

def get_embedding(text: str):
    response = requests.post(OLLAMA_EMBED, json={"model": MODEL_EMBED, "input": [text]})
    response.raise_for_status()
    return response.json().get("embeddings", [])[0]

def search_ceo_vault(query_text: str):
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=5.0)
        vector_query = get_embedding(query_text)
        
        search_result = client.search(
            collection_name=COLLECTION_CEO,
            query_vector=vector_query,
            limit=4
        )
        
        context = "\n".join([f"- {hit.payload.get('text_content', '')}" for hit in search_result])
        return context
    except Exception as e:
        logger.error(f"Error en Qdrant o Embeddings: {e}")
        return ""

@app.post("/api/ceo-chat")
async def ceo_chat(request: ChatRequest):
    logger.info(f"CEO Pregunta: {request.prompt}")
    
    context = search_ceo_vault(request.prompt)
    
    system_prompt = (
        "Eres la Inteligencia Artificial confidencial del CEO de Lifextreme (Agencia de Turismo B2B/B2C). "
        "Responde sus preguntas usando ÚNICAMENTE la siguiente información extraída de los documentos internos confidenciales. "
        "Si la respuesta no está en el contexto, díselo directamente al CEO, no inventes datos.\n\n"
        "=== BÓVEDA CONFIDENCIAL ===\n"
        f"{context}\n"
        "===========================\n"
    )
    
    prompt_final = f"{system_prompt}\nPregunta del CEO: {request.prompt}"
    
    try:
        ollama_response = requests.post(
            OLLAMA_GENERATE,
            json={
                "model": MODEL_CHAT,
                "prompt": prompt_final,
                "stream": False
            },
            timeout=60.0
        )
        ollama_response.raise_for_status()
        respuesta_ia = ollama_response.json().get("response", "Error procesando respuesta.")
        
        return {"response": respuesta_ia.strip()}
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error Ollama: {e}")
        return {"response": "Error: Ollama no está respondiendo. Verifica que esté abierto."}

# Ejecutar con:
# uvicorn scripts.ceo_backend:app --host 0.0.0.0 --port 8001 --reload
