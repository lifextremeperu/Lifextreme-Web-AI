import os
import sys
import subprocess
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from google.oauth2 import credentials
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma

# Configuración de consola
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ID = "project-7ccd00cc-f448-42df-90a"
REGION = "us-central1"
DB_DIR = 'chroma_db'

# 1. Obtener Credenciales de Google Cloud
def get_creds():
    gcloud = r'C:\Users\ASUS\AppData\Local\Google\google-cloud-sdk\bin\gcloud.cmd'
    env = os.environ.copy()
    env['CLOUDSDK_PYTHON'] = r'C:\Python313\python.exe'
    token = subprocess.check_output([gcloud, 'auth', 'print-access-token'], env=env, text=True).strip()
    return credentials.Credentials(token)

creds = get_creds()

# 2. Configurar el Proveedor y Modelo de IA
provider = GoogleProvider(
    credentials=creds,
    project=PROJECT_ID,
    location=REGION,
    vertexai=True
)

model = GoogleModel(
    model_name='gemini-1.5-pro-002',
    provider=provider
)

# 3. Definir la Estructura de Respuesta
class LifextremeResponse(BaseModel):
    mensaje_principal: str = Field(description="Respuesta al usuario")
    fuentes_utilizadas: List[str] = Field(description="Documentos consultados")
    nivel_confianza: float = Field(description="Puntuación de confianza 0-1")

# 4. Crear el Agente Maestro
master_agent = Agent(
    model,
    output_type=LifextremeResponse, # <--- CORREGIDO: Era output_type
    system_prompt=(
        "Eres MAX, el Agente Maestro de Lifextreme Peru. Experto en turismo de aventura y leyes en Cusco. "
        "Usa la herramienta 'search_knowledge' para responder con datos reales."
    )
)

# 5. Herramienta de Búsqueda
@master_agent.tool
async def search_knowledge(ctx: RunContext[None], query: str) -> str:
    print(f"🔍 Buscando en el cerebro: {query}")
    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=REGION,
        credentials=creds
    )
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=3)
    return "\n---\n".join([d.page_content for d in docs])

# 6. Ejecución
async def ask_max(pregunta: str):
    result = await master_agent.run(pregunta)
    return result.data

if __name__ == "__main__":
    async def test():
        print("--- PRUEBA AGENTE MAESTRO (PRO) ---")
        respuesta = await ask_max("¿Qué equipo se necesita para rafting según el reglamento?")
        print(f"\n🤖 MAX responde:\n{respuesta.model_dump_json(indent=2)}")
    
    asyncio.run(test())
