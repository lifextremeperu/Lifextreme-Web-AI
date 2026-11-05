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
try:
    from .rag_service import get_rag_context
    from .agents.medical_acclimatization_agent import MedicalAcclimatizationAgent, MedicalAssessRequest
    from .agents.duffle_bag_optimizer_agent import DuffleBagOptimizerAgent, DuffleOptimizeRequest, DuffleItemInput
    from .agents.tailor_made_private_agent import TailorMadePrivateAgent, TailorMadeRequest
    from .agents.booking_registry import BookingRegistry
except ImportError:
    from rag_service import get_rag_context
    from agents.medical_acclimatization_agent import MedicalAcclimatizationAgent, MedicalAssessRequest
    from agents.duffle_bag_optimizer_agent import DuffleBagOptimizerAgent, DuffleOptimizeRequest, DuffleItemInput
    from agents.tailor_made_private_agent import TailorMadePrivateAgent, TailorMadeRequest
    from agents.booking_registry import BookingRegistry

_medical_subagent = MedicalAcclimatizationAgent()
_duffle_subagent = DuffleBagOptimizerAgent()
_tailor_subagent = TailorMadePrivateAgent()
_booking_registry = BookingRegistry()


def _consult_specialized_agents(query: str) -> str:
    """
    Orquestador de Sub-Agentes Especializados:
    Detecta la intención del usuario en tiempo real y ejecuta el Agente Especializado correspondiente
    para enriquecer la respuesta de MAX con cálculos exactos y protocolos verificados.
    """
    q = query.lower()
    insights = []

    # 1. Detección de consulta Médica / Aclimatación / Mal de Altura
    if any(k in q for k in ["altura", "aclimata", "soroche", "oxigeno", "oxígeno", "presion", "mareo", "4600", "5000", "fisioterapia", "medico", "médico"]):
        try:
            res = _medical_subagent.assess(MedicalAssessRequest(
                client_name="Viajero Lifextreme",
                age=38,
                target_route="Salkantay / Ausangate Alta Montaña",
                max_altitude_m=4630,
                days_prior_in_altitude=1 if "1 dia" in q or "recien" in q or "mañana" in q else 2,
                has_cardio_condition=False,
                lake_louise_score=0
            ))
            plan_str = " | ".join(res.acclimatization_plan[:3])
            insights.append(
                f"[DICTAMEN EN VIVO - AGENTE 1 (ASESOR MÉDICO & ACLIMATACIÓN)]:\n"
                f"• Nivel de Riesgo: {res.risk_level} ({res.approval_status})\n"
                f"• Escalera de Aclimatación Sugerida: {plan_str}\n"
                f"• Monitoreo y Recuperación Activa: {'; '.join(res.biometric_monitoring_rules[:2])} + Fisioterapia en campamento con botas de compresión neumática solar y pediluvios botánicos andinos (romero, llantén y molle)."
            )
        except Exception:
            pass

    # 2. Detección de consulta Logística / Equipaje / Duffle Bag 7 kg / Porteadores
    if any(k in q for k in ["equipaje", "mochila", "duffle", "7 kg", "7kg", "peso", "llevar", "ropa", "porteador", "mula", "saco de dormir", "packing"]):
        try:
            res = _duffle_subagent.optimize(DuffleOptimizeRequest(
                passenger_name="Viajero Lifextreme",
                route_name="Salkantay / Camino Inca",
                items=[
                    DuffleItemInput(item_id="sleeping_bag_pluma", item_name="Saco de dormir pluma -10°C", weight_grams=1450, quantity=1),
                    DuffleItemInput(item_id="casaca_plumas_abrigo", item_name="Chaqueta térmica de pluma", weight_grams=380, quantity=1),
                    DuffleItemInput(item_id="mudas_interiores_x3", item_name="Capas base térmicas merino", weight_grams=250, quantity=2),
                    DuffleItemInput(item_id="pantalon_hardshell_goretex", item_name="Pantalón impermeable trekking", weight_grams=540, quantity=1),
                    DuffleItemInput(item_id="casaca_impermeable_goretex", item_name="Casaca impermeable Gore-Tex", weight_grams=485, quantity=1),
                    DuffleItemInput(item_id="botella_agua_o_camelbak_2l", item_name="Hidratación Camelbak 2L", weight_grams=2100, quantity=1),
                ]
            ))
            insights.append(
                f"[DICTAMEN EN VIVO - AGENTE 2 (DUFFLE BAG OPTIMIZER 7 KG & LEY 31614)]:\n"
                f"• Regla Operativa: Límite de {res.max_duffle_allowance_kg} kg en el Duffle Bag entregado a los arrieros/porteadores (simulación base: {res.duffle_total_weight_kg} kg usados, {res.remaining_allowance_kg} kg libres).\n"
                f"• Garantía Ética Lifextreme: Cumplimiento estricto de la Ley del Porteador N° 31614 (máx. 20 kg auditados en balanza digital visible ante el cliente) + Pasaporte Ético Animal."
            )
        except Exception:
            pass

    # 3. Detección de consulta Privada / Tailor-Made / 4x4 / VIP / Glamping / Lujo
    if any(k in q for k in ["privad", "vip", "lujo", "tailor", "medida", "4x4", "glamping", "domo", "exclusiv", "pareja"]):
        try:
            res = _tailor_subagent.generate_quote(TailorMadeRequest(
                client_name="Viajero VIP",
                pax_count=2,
                trip_days=5,
                preferred_regions=["Cusco", "Salkantay", "Ausangate"],
                special_interests=["Domos Exclusivos", "Alta Gastronomía Andina"],
                budget_tier="VIP_PREMIUM"
            ))
            insights.append(
                f"[DICTAMEN EN VIVO - AGENTE 3 (PRIVATE TAILOR-MADE AWASI/EXPLORA)]:\n"
                f"• Propuesta: {res.itinerary_title} (${res.estimated_price_per_pax_usd:,.0f} USD por persona | Depósito 30%: ${res.deposit_required_30_usd:,.0f} USD)\n"
                f"• Asignación Exclusiva: {res.private_guide_profile} + {res.private_vehicle_profile}\n"
                f"• Diferenciación Lifextreme: Desfase horario inteligente (Offset Trekking +/- 90 min sin multitudes), baños secos ecológicos y gastronomía hiperlocal con comunidades."
            )
        except Exception:
            pass

    return "\n\n".join(insights)

load_dotenv(override=True)

OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL   = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

_llm_http = httpx.AsyncClient(timeout=45.0)

SYSTEM_PROMPT = """Eres MAX, el Asistente Experto de Montaña y Expediciones de Lifextreme Perú (certificado UIAGM), conectado en vivo al cerebro vectorial de Qdrant (+337,000 vectores) y a los 5 Agentes Operativos.

CÓMO DEBES CONVERSAR (ESTILO LIMPIO, ORGÁNICO Y CONSULTIVO TIPO GEMINI / CHATGPT):
1. RESPONDE SIEMPRE LA PREGUNTA EXACTA DEL USUARIO PRIMERO:
   - Si pregunta por fechas (ej. "fechas para Salkantay 4D/3N en diciembre"), confírmale de inmediato que contamos con **salidas diarias garantizadas durante todo diciembre (del 1 al 31 de diciembre, incluyendo Navidad y Año Nuevo)** a partir de 2 viajeros, tanto en grupos reducidos (ratio máx. 1:8) como en modalidad Privada VIP.
   - NUNCA cambies el destino por el que pregunta el usuario (si pregunta por Salkantay, habla de Salkantay, jamás lo cambies por Choquequirao).
   - Responde en 1 o 2 párrafos breves y limpios (máximo 70 a 95 palabras).

2. CONVERSACIÓN ORGÁNICA Y SUTILEZA COMERCIAL (SIN APURAR AL CLIENTE):
   - No lances bloques de precios ni enlaces de pago si el usuario solo está haciendo una consulta informativa.
   - Guía la charla con naturalidad haciendo al final **1 sola pregunta suave** para conocer mejor su viaje (por ejemplo: para qué días de ese mes planean viajar, cuántos integrantes son o si prefieren ir a su propio ritmo).

3. CONOCIMIENTO DIFERENCIADOR DE QDRANT Y LOS 5 AGENTES:
   - Integra de forma natural las ventajas de Lifextreme según el tema: Domos Geodésicos Glamping en Soraypampa (3,900m), desfase horario (Offset Trekking sin multitudes), Duffle Bag de 7 kg porteado bajo la Ley N° 31614 con pesaje digital, fisioterapia en campamento (botas de compresión y pediluvios botánicos) y monitoreo biométrico de altura (SpO2) con soporte de O2 Medical Network.

4. CUÁNDO MOSTRAR OPCIÓN DE RESERVA (SOLO CON INTENCIÓN DE COMPRA):
   - Solo cuando el usuario pregunte precios, cómo reservar o muestre intención clara de separar sus fechas, indícale que puede asegurar sus cupos con el **30%** (sistema 30/30/40) y agrega al final:
     `[CARRITO: Nombre del Tour | PrecioTotalEnSoles | NumeroDePersonas]`
   - Tarifas base referenciales por persona del catálogo oficial:
     * Salkantay Trek & Glamping a Machu Picchu 4D/3N (Cusco): S/ 1850
     * Camino Inca a Machu Picchu 4D (Cusco): S/ 2450
     * Trekking Choquequirao 4D (Cusco): S/ 3200
     * Circuito Ausangate 6D (Cusco): S/ 2100
     * Montaña de los 7 Colores Express (Cusco): S/ 450
     * Trekking Santa Cruz 4D (Huaraz): S/ 1200
     * Trekking Laguna 69 y Llanganuco (Huaraz): S/ 350
     * Expedición Pacaya Samiria 5D (Iquitos): S/ 2800
     * Trekking Cañón del Colca 3D (Arequipa): S/ 850
     * Ascenso Volcán Misti 2D (Arequipa): S/ 1100

5. GUARDRAIL GUBERNAMENTAL (MINCETUR):
   - Camino Inca cierra solo en febrero por mantenimiento anual (en diciembre está abierto con reserva previa). Si alguien busca Camino Inca para mañana mismo sin reserva previa, ofrécele Salkantay Glamping, Lares o Ausangate con salida inmediata."""


_QUICK_GREETINGS = {"hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hi", "hello", "que tal", "ola"}


async def _build_messages(prompt: str, history: List[dict] = None, user_data: dict = None) -> List[dict]:
    """
    Construye el historial y extrae el contexto de Qdrant combinando la intencion actual
    con el contexto reciente de la conversacion y verificando en el Registro de Reservas
    si es un VISITANTE WEB o un CLIENTE CON RESERVA CONFIRMADA.
    """
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    clean_q = prompt.strip().lower().rstrip("?!.")

    # Verificar si el usuario ya tiene reserva activa (por localStorage profile, código LX-XXXX en texto, email o teléfono)
    u_dict = user_data if isinstance(user_data, dict) else {}
    active_booking = _booking_registry.find_booking(
        booking_code=u_dict.get("booking_code"),
        phone=u_dict.get("phone"),
        email=u_dict.get("email"),
        text_message=prompt
    )
    # Si el navegador envió directamente los datos de localStorage ('lifextreme_last_order') pero aún no estaba en disco, registrarlo
    if not active_booking and u_dict.get("booking_code") and u_dict.get("tour_name"):
        active_booking = {
            "booking_code": u_dict.get("booking_code"),
            "passenger_name": u_dict.get("passenger_name", "Explorador Lifextreme"),
            "tour_name": u_dict.get("tour_name"),
            "tour_date": u_dict.get("tour_date", "Próxima salida"),
            "paid_amount_pen": u_dict.get("paid_today", 0),
            "lifecycle_stage": u_dict.get("lifecycle_stage", "RESERVA_CONFIRMADA_PRE_VIAJE")
        }

    booking_context_banner = ""
    if active_booking:
        booking_context_banner = (
            f"\n=== 🎫 ESTADO DEL CLIENTE: PASAJERO CON RESERVA CONFIRMADA ({active_booking['booking_code']}) ===\n"
            f"• Nombre: {active_booking.get('passenger_name')} | Expedición Reservada: {active_booking.get('tour_name')}\n"
            f"• Fecha de Salida: {active_booking.get('tour_date')} | Etapa Actual: {active_booking.get('lifecycle_stage')}\n"
            f"• DIRECTIVA DE ROL PARA MAX: ¡Este cliente YA COMPRÓ y tiene su reserva activa! NO le vendas de nuevo ni pongas etiqueta [CARRITO:...]. "
            f"Atiéndelo como su Concierge Oficial Post-Venta de Lifextreme ayudándolo con su Escalera de Aclimatación (Agente 1), "
            f"su Duffle Bag de 7 kg (Agente 2) o su seguimiento de Calidad Post-Viaje (Agente 5).\n"
        )
    else:
        booking_context_banner = (
            "\n=== 🟢 ESTADO DEL CLIENTE: VISITANTE EN LA WEB (AÚN SIN RESERVA) ===\n"
            "• DIRECTIVA DE ROL PARA MAX: Este usuario aún no tiene reserva registrada. Atiéndelo en Modo Ventas Consultivas, "
            "resuelve sus dudas con excelencia y guíalo al cierre de reserva con el 30% en el Carrito.\n"
        )

    # Si el usuario responde corto (ej. "somos 4 amigos de 28 años"), enriquecer la query de Qdrant con el turno anterior
    rag_query = prompt
    if history and len(prompt.split()) <= 10:
        prev_user_msgs = [m.get("content", "") for m in history[-4:] if isinstance(m, dict) and m.get("role") == "user"]
        if prev_user_msgs:
            rag_query = f"{prev_user_msgs[-1]} {prompt}"

    if clean_q in _QUICK_GREETINGS and not history and not active_booking:
        rag_context = (
            "El viajero acaba de saludar. Dale una bienvenida cálida como MAX de Lifextreme Perú "
            "y pregúntale qué destino le llama la atención y si viaja en familia, con amigos, en pareja o solo."
        )
    else:
        rag_context = await get_rag_context(rag_query)
        subagent_insights = _consult_specialized_agents(rag_query)
        if subagent_insights:
            rag_context = f"{subagent_insights}\n\n{rag_context}"

    system_with_rag = (
        f"{SYSTEM_PROMPT}\n"
        f"{booking_context_banner}\n"
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
        messages = await _build_messages(prompt, history, user_data)
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
