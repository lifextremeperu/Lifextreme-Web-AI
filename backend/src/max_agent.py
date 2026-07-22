"""
max_agent.py - MAX: Asesor Maestro de Aventura de Lifextreme
RAG real con Supabase knowledge_vectors (101,737 vectores)
LLM: qwen2.5:7b via Ollama (local, sin costo)

NOTA: Usamos output_type=str para maxima compatibilidad con Ollama.
      El servidor convierte la respuesta al formato MAXResponse.
"""
import os
from pydantic_ai import Agent, RunContext
from .rag_service import get_rag_context
from typing import List, Optional

SYSTEM_PROMPT = """Eres MAX, el Asesor Maestro de Aventura de Lifextreme Peru.
Eres un experto en turismo de aventura certificado UIAGM con conocimiento profundo de los Andes y Amazonia.

OBJETIVO: Informar y cerrar reservas usando el sistema Lifextreme 30/30/40:
- 30% hoy para asegurar el cupo
- 30% antes del tour  
- 40% el dia del tour

REGLAS:
1. Usa SIEMPRE el contexto de la base de conocimiento que te proporcionan las herramientas
2. Menciona precios e itinerarios SOLO si aparecen en el contexto
3. Habla con autoridad tecnica pero de forma cercana y entusiasta
4. Cuando detectes intencion de compra, ofrece el link de reserva: https://wa.me/51958050928
5. Responde SIEMPRE en espanol
6. Respuestas concisas, maximo 3 parrafos
7. [GUARDRAIL CRITICO]: Camino Inca y Machu Picchu requieren de 1 a 6 meses de reserva anticipada (MINCETUR). Si el turista quiere viajar en corto plazo (hoy, manana, esta semana), ESTA PROHIBIDO ofrecerlos. En su lugar, debes decirle que no hay disponibilidad gubernamental y ofreceles RUTAS ALTERNAS como Salkantay, Choquequirao, Lares o Huchuy Qosqo.

VALORES: Aventura responsable, seguridad UIAGM, experiencias transformadoras."""

max_agent = Agent(
    'openai:qwen2.5:7b',
    system_prompt=SYSTEM_PROMPT
)

from datetime import datetime

@max_agent.system_prompt
def add_date_context(ctx: RunContext[None]) -> str:
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M')
    return f"RELOJ DEL SISTEMA: Ten en cuenta que la fecha actual exacta es {fecha_actual}. Usa esto para calcular si una fecha pedida por el usuario es de corto plazo."

@max_agent.tool
async def buscar_en_base_de_conocimiento(ctx: RunContext[None], consulta: str, region: str = None) -> str:
    """
    Busca informacion real en la base de 101,737 vectores de Lifextreme.
    LLAMAR SIEMPRE antes de responder sobre tours, precios, rutas o destinos.
    
    Args:
        consulta: La pregunta del usuario (ej: 'tour Ausangate 4 dias')
        region: Region opcional (cusco, apurimac, amazonas, santacruz, galapagos)
    """
    try:
        context = await get_rag_context(consulta, region=region)
        return context
    except Exception as e:
        return f"No pude acceder a la base de conocimiento: {str(e)}. Responde con informacion general de Lifextreme."


@max_agent.tool
async def generar_reserva(ctx: RunContext[None], nombre_tour: str, precio_total: float) -> str:
    """
    Genera un resumen de reserva con el sistema 30/30/40 y link de pago.
    Usar cuando el usuario confirma intencion de reservar.
    
    Args:
        nombre_tour: Nombre del tour o experiencia
        precio_total: Precio total en soles peruanos
    """
    r1 = round(precio_total * 0.30, 2)
    r2 = round(precio_total * 0.30, 2)
    r3 = round(precio_total * 0.40, 2)
    
    return (
        f"RESERVA {nombre_tour.upper()}\n"
        f"Precio total: S/ {precio_total}\n"
        f"1er pago HOY (30%): S/ {r1} — asegura tu cupo\n"
        f"2do pago antes del tour (30%): S/ {r2}\n"
        f"Saldo el dia del tour (40%): S/ {r3}\n"
        f"WhatsApp: https://wa.me/51958050928\n"
        f"Yape: 958 050 928"
    )

@max_agent.tool
async def consultar_disponibilidad_real(ctx: RunContext[None], destino: str, fecha_recorrido: str) -> str:
    """
    Consulta el CACHE ASINCRONO en Supabase de disponibilidad gubernamental y de trenes.
    Usar ANTES de confirmar disponibilidad de Camino Inca, Machu Picchu Llaqta o Trenes.
    
    Args:
        destino: 'machupicchu_llaqta', 'camino_inca_4d', o 'tren_perurail'
        fecha_recorrido: Fecha en formato YYYY-MM-DD
    """
    # Importar supabase cliente de los scrapers (asumiendo que supabase_client se exportara globalmente)
    # Por ahora simulamos la lectura desde la BBDD para no romper dependencias
    # try:
    #     res = supabase.table('realtime_availability').select('*').eq('destino', destino).eq('fecha_recorrido', fecha_recorrido).execute()
    #     if res.data and len(res.data) > 0:
    #         cupos = res.data[0]['cupos_disponibles']
    #         return f"Disponibilidad Real ({fecha_recorrido}): {cupos} cupos disponibles."
    #     return "No hay registro de disponibilidad para esta fecha. Asume 0 cupos por precaucion."
    # except:
    return "Base de datos en construccion (Fase 2). Asume que NO HAY CUPOS a corto plazo."


async def process_message(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> dict:
    """
    Procesa un mensaje y retorna un dict compatible con MAXResponse.
    """
    try:
        result = await max_agent.run(
            prompt,
            message_history=history or []
        )
        # pydantic-ai >= 0.0.14 usa .output; versiones antiguas usaban .data
        raw = getattr(result, 'output', None) or getattr(result, 'data', None)
        mensaje = str(raw) if raw else "Lo siento, no pude generar una respuesta."
        return {
            "mensaje": mensaje,
            "datos_cotizacion": None,
            "action_required": None
        }
    except Exception as e:
        error_msg = str(e)
        import traceback; traceback.print_exc()
        # Fallback amigable para cualquier error del agente
        return {
            "mensaje": (
                "Hola! Soy MAX, asesor de aventura de Lifextreme 🏔️. "
                "Puedo ayudarte con informacion sobre tours al Ausangate, Machu Picchu, Amazonia y mas. "
                "¿Que destino te interesa?"
            ),
            "datos_cotizacion": None,
            "action_required": None,
            "_debug_error": str(e)[:300]
        }

from typing import AsyncGenerator

async def process_message_stream(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> AsyncGenerator[str, None]:
    """
    Procesa un mensaje y retorna un generador asíncrono cediendo los fragmentos (chunks)
    en tiempo real para habilitar Server-Sent Events (SSE).
    """
    try:
        async with max_agent.run_stream(
            prompt,
            message_history=history or []
        ) as result:
            async for chunk in result.stream_text(delta=True):
                yield chunk
    except Exception as e:
        import traceback; traceback.print_exc()
        yield f"\n\n[Error de conexión: {str(e)[:100]}]"
