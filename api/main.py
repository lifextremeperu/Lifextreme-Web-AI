import os
import sys
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from google.oauth2 import service_account
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

# Configuración de producción
app = FastAPI(title="Lifextreme AI Master API")

# Habilitar CORS para que tu web pueda hablar con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambia esto a tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-7ccd00cc-f448-42df-90a")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
DB_DIR = 'chroma_db'

# 1. Configuración del Modelo e IA
# En la nube, las credenciales se manejan automáticamente o vía Service Account
model = GoogleModel('gemini-1.5-flash-002') # Simplificado para Cloud Run

class LifextremeResponse(BaseModel):
    mensaje_principal: str
    fuentes_utilizadas: List[str]
    nivel_confianza: float

master_agent = Agent(
    model,
    output_type=LifextremeResponse,
    system_prompt=(
        "Eres MAX, el Agente Maestro de Lifextreme Peru. Experto en turismo de aventura y leyes en Cusco. "
        "Usa la herramienta 'search_knowledge' para responder con datos reales basados en los PDFs y Cixtur. "
        "Sé amable, profesional y enfocado en la seguridad."
    )
)

# 2. Herramienta de Búsqueda Semántica
@master_agent.tool
async def search_knowledge(ctx: RunContext[None], query: str) -> str:
    # Usamos las credenciales por defecto del entorno (ADC)
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION
    )
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=3)
    return "\n---\n".join([d.page_content for d in docs])

# 3. Endpoints de la API
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await master_agent.run(request.message)
        return result.data
    except Exception as e:
        print(f"Error en el chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "agent": "MAX", "knowledge_base": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
