"""
max_agent.py - MAX: Operador Experto y Asesor Consultivo de Lifextreme Peru
Arquitectura Hibrida Nivel 1 + Nivel 2 (Groq LPU llama-3.3-70b-versatile + Qdrant 336k vectores).
"""
import os
import json
import httpx
from datetime import datetime
from typing import List, AsyncGenerator
from dotenv import load_dotenv
from .rag_service import get_rag_context

load_dotenv(override=True)

OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

_llm_http = httpx.AsyncClient(timeout=45.0)

SYSTEM_PROMPT = """Eres MAX, el Operador Experto de Montaña y Asesor de Aventuras de Lifextreme Perú (certificado UIAGM).
Atiendes por chat como un guía y operador humano real por WhatsApp: cálido, ágil, observador y muy profesional.

CÓMO DEBES CONVERSAR (ESTILO OPERADOR EXPERTO DE WHATSAPP):
1. FLUIDEZ Y BREVEDAD (PROHIBIDO LANZAR MUROS DE TEXTO):
   - Responde en 1 o 2 párrafos cortos (máximo 70 a 95 palabras por mensaje).
   - Conversa de ida y vuelta esperando la respuesta del viajero, igual que en un chat real de WhatsApp.

2. PERFILAMIENTO INTELIGENTE DEL VIAJERO (ANTES DE RECETAR UN TOUR A CIEGAS):
   - Un buen operador no lanza precios ni rutas extremas sin conocer a su grupo.
   - Revisa el historial de la conversación. Si aún NO sabes el perfil del cliente, responde brevemente a su inquietud usando el conocimiento de Qdrant y hazle **1 o máximo 2 preguntas naturales** para perfilarlo:
     a) ¿Con quién viajas? (¿Vienen en familia con niños/adultos mayores, en pareja, grupo de amigos o vas solo?)
     b) ¿Qué edades aproximadas tienen o cómo se sienten con las caminatas en altura?
     c) ¿Para qué fecha o cuántos días tienen pensados?
   - ¡IMPORTANTE!: No hagas las 3 preguntas como un interrogatorio policial. Haz 1 o 2 de forma cálida y natural según lo que el cliente acaba de decir, y espera su respuesta.

3. RECOMENDACIÓN A MEDIDA CON EL CONOCIMIENTO DE QDRANT:
   - Cuando el cliente te cuente si es familia, amigos, edades o nivel físico, cruza eso con el CONTEXTO VERIFICADO DE QDRANT (altitudes, exigencia física, clima, qué incluye, precios reales):
     * Si es familia / niños / adultos mayores / poca aclimatación -> sugiere experiencias seguras, culturales o de aclimatación progresiva (Valle Sagrado VIP, Maras Moray, Huchuy Qosqo, Laguna Humantay con caballo de apoyo, etc.).
     * Si es grupo de amigos / jóvenes / buscan adrenalina o trekking -> sugiere retos memorables (Salkantay, Ausangate, Choquequirao, Lares, parques de aventura / zipline / vía ferrata).

4. CIERRE AL CARRITO DE COMPRAS WEB (SISTEMA LIFEXTREME 30/30/40):
   - Cuando ya conozcas el perfil del cliente y le recomiendes un tour específico con precio, o cuando el cliente elija un tour / quiera pagar o reservar:
     * Menciona que puede bloquear sus cupos en el Carrito de la web pagando hoy solo el **30%** (30% hoy, 30% antes del tour y 40% el día del tour).
     * AL FINAL de tu respuesta (en la última línea), escribe SIEMPRE esta etiqueta exacta para que aparezca el botón del Carrito de Compras en su pantalla:
       `[CARRITO: Nombre del Tour | PrecioTotalEnSoles | NumeroDePersonas]`
       Ejemplo para 2 personas en Montaña 7 Colores (S/ 450 c/u = 900 total):
       `[CARRITO: Montaña de los 7 Colores Express | 900 | 2]`
   - Tarifas base referenciales por persona del catálogo web (si el RAG no especifica otra):
     * Camino Inca a Machu Picchu 4D (Cusco): S/ 2450
     * Ciclismo Downhill Abra Málaga (Cusco): S/ 180
     * Montaña de los 7 Colores Express (Cusco): S/ 450
     * Trekking Choquequirao 4D (Cusco): S/ 3200
     * Circuito Ausangate 6D (Cusco): S/ 2100
     * Salkantay Trek a Machu Picchu 4D (Cusco): S/ 1850
     * Trekking Santa Cruz 4D (Huaraz): S/ 1200
     * Trekking Laguna 69 y Llanganuco (Huaraz): S/ 350
     * Expedición Pacaya Samiria 5D (Iquitos): S/ 2800
     * Trekking Cañón del Colca 3D (Arequipa): S/ 850
     * Ascenso Volcán Misti 2D (Arequipa): S/ 1100
     * Buggies y Sandboard Extremo (Ica): S/ 180

5. GUARDRAIL GUBERNAMENTAL (MINCETUR):
   - Camino Inca y Machu Picchu Llaqta requieren de 1 a 6 meses de anticipación. Si el viajero quiere ir hoy, mañana o esta semana, adviértele con honestidad de operador experto que los boletos estatales están agotados a corto plazo y ofrécele alternativas espectaculares con salida inmediata (Salkantay, Lares, Choquequirao, Ausangate o Huchuy Qosqo)."""


_QUICK_GREETINGS = {"hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hi", "hello", "que tal", "ola"}


async def _build_messages(prompt: str, history: List[dict] = None) -> List[dict]:
    """
    Construye el historial y extrae el contexto de Qdrant combinando la intencion actual
    con el contexto reciente de la conversacion para no perder el hilo del destino.
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    clean_q = prompt.strip().lower().rstrip("?!.")

    # Si el usuario responde corto (ej. "somos 4 amigos de 28 años"), enriquecer la query de Qdrant con el turno anterior
    rag_query = prompt
    if history and len(prompt.split()) <= 10:
        prev_user_msgs = [m.get("content", "") for m in history[-4:] if isinstance(m, dict) and m.get("role") == "user"]
        if prev_user_msgs:
            rag_query = f"{prev_user_msgs[-1]} {prompt}"

    if clean_q in _QUICK_GREETINGS and not history:
        rag_context = (
            "El viajero acaba de saludar. Dale una bienvenida cálida como MAX de Lifextreme Perú "
            "y pregúntale qué destino le llama la atención y si viaja en familia, con amigos, en pareja o solo."
        )
    else:
        rag_context = await get_rag_context(rag_query)

    system_with_rag = (
        f"{SYSTEM_PROMPT}\n\n"
        f"FECHA ACTUAL DEL SISTEMA: {fecha_actual}\n\n"
        f"=== CONOCIMIENTO REAL LIFEXTREME (QDRANT 336K VECTORES) ===\n{rag_context}"
    )

    messages = [{"role": "system", "content": system_with_rag}]

    if history:
        for msg in history[-8:]:
            if isinstance(msg, dict):
                role = "user" if msg.get("role") == "user" else "assistant"
                content = str(msg.get("content", "")).strip()
                if content:
                    messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": prompt})
    return messages


async def _stream_groq(messages: List[dict], api_key: str) -> AsyncGenerator[str, None]:
    """Nivel 2: Streaming ultra-rapido via Groq LPU (~0.4s TTFT)."""
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 900,
        "reasoning_effort": "low",
        "stream": True,
    }
    async with _llm_http.stream("POST", GROQ_API_URL, headers=headers, json=payload) as resp:
        resp.raise_for_status()
        async for line in resp.aiter_lines():
            if not line or not line.startswith("data: "):
                continue
            data_str = line[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                data = json.loads(data_str)
                delta = data["choices"][0].get("delta", {}).get("content")
                if delta:
                    yield delta
            except Exception:
                continue


async def _stream_ollama(messages: List[dict]) -> AsyncGenerator[str, None]:
    """Nivel 1 (Fallback local): Streaming directo en 1 solo viaje a Ollama local."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
        "keep_alive": -1,
        "options": {
            "temperature": 0.45,
            "num_ctx": 2048,
            "num_predict": 320,
        },
    }
    async with _llm_http.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as resp:
        resp.raise_for_status()
        async for line in resp.aiter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                chunk = data.get("message", {}).get("content")
                if chunk:
                    yield chunk
            except Exception:
                continue


async def process_message_stream(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> AsyncGenerator[str, None]:
    try:
        load_dotenv(override=True)
        messages = await _build_messages(prompt, history)
        groq_key = os.getenv("GROQ_API_KEY", "").strip()

        if groq_key and groq_key.startswith("gsk_"):
            try:
                async for chunk in _stream_groq(messages, groq_key):
                    yield chunk
                return
            except Exception as groq_err:
                print(f"[MAX] Groq fallback a Ollama local: {groq_err}")

        async for chunk in _stream_ollama(messages):
            yield chunk

    except Exception as e:
        import traceback
        traceback.print_exc()
        yield f"\n\n[Error de conexión: {str(e)[:100]}]"


async def process_message(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> dict:
    try:
        chunks = []
        async for c in process_message_stream(prompt, history, user_data):
            chunks.append(c)
        mensaje = "".join(chunks).strip() or "Lo siento, no pude generar una respuesta."
        return {
            "mensaje": mensaje,
            "datos_cotizacion": None,
            "action_required": None,
        }
    except Exception as e:
        return {
            "mensaje": (
                "¡Hola! Soy MAX, operador de aventura de Lifextreme 🏔️. "
                "Escríbenos por WhatsApp al +51 958 050 928 para ayudarte al instante."
            ),
            "datos_cotizacion": None,
            "action_required": None,
            "_debug_error": str(e)[:300],
        }
