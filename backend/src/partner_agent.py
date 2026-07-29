"""
partner_agent.py - Partner AI: Analista Estratégico y Legal de Lifextreme (B2B)
RAG real con Supabase knowledge_vectors (320,000 vectores, incluyendo normativas peruanas, INACAL y base institucional)
LLM: qwen2.5:7b via Ollama (local)
"""
import os
from pydantic_ai import Agent, RunContext
from .rag_service import get_rag_context
from typing import List, AsyncGenerator

SYSTEM_PROMPT = """Eres LIFEXTREME-CORE, el Analista Estratégico, Legal y Operativo B2B exclusivo para las agencias de viaje partners de Lifextreme.
Eres un auditor experto, abogado turístico y estratega de negocios con profundo conocimiento de las normativas del MINCETUR, códigos penales, INACAL y el mercado peruano de aventura.

OBJETIVO: Proteger a las agencias partners de riesgos legales, optimizar su rentabilidad y asegurar el cumplimiento de la ley (Ley 29783, D.Leg 1350, Reglamentos de Turismo).

REGLAS CRÍTICAS:
1. Usa SIEMPRE el contexto de la base de conocimiento que te proporciona tu herramienta de búsqueda vectorial.
2. NUNCA inventes leyes o normativas. Si una ley, artículo o multa no aparece en el contexto, indica que requieres verificación o que no tienes el dato exacto en tu base normativa.
3. Habla con un tono altamente profesional, consultivo, estructurado y directo. No uses tono de vendedor turístico.
4. Si te preguntan sobre multas, responsabilidades o riesgos operacionales, usa viñetas para ser claro y advierte sobre el impacto en el negocio.
5. Si un partner propone una idea que va contra las normativas (ej: operar un deporte de aventura sin equipo certificado), DEBES ADVERTIR de la negligencia o el riesgo penal.
6. Cita las fuentes (nombre de la ley, decreto, excel institucional) si aparecen en el contexto.

VALORES: Seguridad operativa, cumplimiento estricto, excelencia corporativa, rentabilidad sostenible."""

partner_agent = Agent(
    'openai:qwen2.5:7b',
    system_prompt=SYSTEM_PROMPT
)

from datetime import datetime

@partner_agent.system_prompt
def add_date_context(ctx: RunContext[None]) -> str:
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"RELOJ DEL SISTEMA: La fecha actual es {fecha_actual}. Analiza las estrategias de negocio con este marco temporal."

@partner_agent.tool
async def buscar_en_base_normativa_y_comercial(ctx: RunContext[None], consulta: str) -> str:
    """
    Busca información en la base de datos de 320,000 vectores.
    LLAMAR SIEMPRE para responder dudas sobre leyes, agencias registradas, requisitos operativos o regulaciones.
    
    Args:
        consulta: La pregunta del partner detallada (ej: 'requisitos legales para operar canotaje', 'artículos sobre negligencia en código penal', 'guías registrados en Cusco').
    """
    try:
        # Usamos la misma función robusta de RAG que MAX, que ahora apunta a la DB unificada
        context = await get_rag_context(consulta)
        return context
    except Exception as e:
        return f"[ERROR DEL SISTEMA: No se pudo conectar a la base vectorial: {str(e)}]. Avisa al partner que operen con precaución y revisen El Peruano."

async def process_b2b_stream(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> AsyncGenerator[str, None]:
    """
    Procesa un mensaje del Partner y retorna un generador asíncrono para Server-Sent Events (SSE).
    """
    try:
        async with partner_agent.run_stream(
            prompt,
            message_history=history or []
        ) as result:
            async for chunk in result.stream_text(delta=True):
                yield chunk
    except Exception as e:
        import traceback; traceback.print_exc()
        yield f"\n\n[Error en el procesamiento analítico: {str(e)[:100]}]"

