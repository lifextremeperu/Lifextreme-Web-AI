import os
import sys
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuración de consola
sys.stdout.reconfigure(encoding='utf-8')

DB_DIR = 'chroma_db'

# 1. Configurar Pydantic AI para apuntar a Ollama local
os.environ['OPENAI_API_KEY'] = 'ollama'
os.environ['OPENAI_BASE_URL'] = 'http://localhost:11434/v1'

# 2. Definir la Estructura de Respuesta
class LifextremeResponse(BaseModel):
    mensaje_principal: str = Field(description="Respuesta al usuario")
    fuentes_utilizadas: List[str] = Field(description="Documentos consultados")
    nivel_confianza: float = Field(description="Puntuación de confianza 0-1")

# 3. Crear el Agente Maestro
master_agent = Agent(
    'openai:llama3',
    output_type=LifextremeResponse,
    system_prompt=(
        "Eres MAX, el Agente Maestro de Lifextreme Peru. Experto en turismo de aventura y leyes en Cusco. "
        "Usa la herramienta 'search_knowledge' para responder con datos reales."
    )
)

# 4. Herramienta de Búsqueda
@master_agent.tool
async def search_knowledge(ctx: RunContext[None], query: str) -> str:
    print(f"🔍 Buscando en el cerebro: {query}")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    docs = vectorstore.similarity_search(query, k=3)
    return "\n---\n".join([d.page_content for d in docs])

# 5. Ejecución
async def ask_max(pregunta: str):
    result = await master_agent.run(pregunta)
    return result.data

if __name__ == "__main__":
    async def test():
        print("--- PRUEBA AGENTE MAESTRO (PRO) ---")
        respuesta = await ask_max("¿Qué equipo se necesita para rafting según el reglamento?")
        print(f"\n🤖 MAX responde:\n{respuesta.model_dump_json(indent=2)}")
    
    asyncio.run(test())
