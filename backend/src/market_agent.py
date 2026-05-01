import os
import json
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from typing import List, Optional

# --- MODELOS DE DATOS ---
class MarketInsight(BaseModel):
    title: str
    summary: str
    relevance: str
    source_url: str

class ResearchReport(BaseModel):
    topic: str
    date: str
    insights: List[MarketInsight]
    conclusion: str
    recommendation: str

# --- AGENTE INVESTIGADOR ---
market_agent = Agent(
    'openai:hub-llama3', # O el modelo que prefieras en la nube
    output_type=ResearchReport,
    system_prompt=(
        "Eres el Director de Inteligencia de Mercado de Lifextreme. "
        "Tu objetivo es encontrar datos técnicos, precios y tendencias en el sector turismo. "
        "Enfócate en números reales y fuentes verificables."
    ),
)

@market_agent.tool
async def search_internet(ctx: RunContext[None], query: str) -> str:
    """Busca en internet información actualizada sobre turismo."""
    # Aquí iría la integración con Tavily o similar vía variable de entorno
    return f"Simulación de búsqueda para: {query}. En producción, conectamos con Tavily/Firecrawl."

# --- LOGICA DE EXPORTACIÓN ---
def save_report(report: ResearchReport):
    path = os.path.join(os.path.dirname(__file__), "..", "data", "market_reports.json")
    # Lógica para guardar reportes acumulativos
    pass
