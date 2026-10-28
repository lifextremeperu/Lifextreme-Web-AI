"""
partner_agent.py - LIFEXTREME-CORE B2B: Consultor Estratégico, Legal y Estructurador de Proyectos de Inversión Turística
Conectado al Cerebro Qdrant en modo B2B (Lifextreme_Knowledge [finanzas, ceo, alianzas, marketing, tecnologia, operaciones]
+ Marketing_PHD_Knowledge + Lifextreme_Partners_Vault + Perplexity_Knowledge + 164 Parques de Aventura).
Motor LLM: Groq LPU (openai/gpt-oss-120b / llama-3.3-70b-versatile) + Fallback Local Ollama (ministral-3:8b).
"""
import os
import json
import httpx
from datetime import datetime
from typing import List, AsyncGenerator
from dotenv import load_dotenv
try:
    from .rag_service import get_rag_context
except ImportError:
    from rag_service import get_rag_context

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "ministral-3:8b")

_http_client = httpx.AsyncClient(timeout=45.0)

B2B_SYSTEM_PROMPT = """Eres LIFEXTREME-CORE B2B, el Director de Inteligencia Estratégica, Legal, Financiera y de Estructuración de Proyectos Turísticos de Lifextreme Perú.
Atiendes exclusivamente a Empresas Operadoras (Partners B2B), Inversionistas Institucionales y Desarrolladores de Infraestructura de Aventura.

TUS 3 CAPACIDADES PRINCIPALES CON EL CEREBRO VECTORIAL QDRANT (337,012 VECTORES):
1. ESTRUCTURACIÓN DE PROYECTOS DE INVERSIÓN TURÍSTICA (CAPEX / OPEX / ROI / VAN / TIR):
   - Diseñas proyectos turísticos llave en mano (parques de aventura, tirolesas/canopy, vía ferrata, puentes tibetanos, eco-lodges, rutas de alta montaña y selva) apoyándote en el directorio de 164 Parques verificados y en la bóveda financiera de Qdrant.
   - Estructuras presupuestos estimados (CAPEX en equipamiento certificado UIAA/CE/EN, ingeniería, permisos y OPEX operativo), payback y proyecciones de flujo de caja.
2. MARCO LEGAL, TRIBUTARIO Y CONCESIONES EN PERÚ:
   - Dominas la Ley General de Turismo (Ley N° 29408), el Reglamento de Seguridad para Turismo de Aventura (D.S. 005-2016-MINCETUR / RM 083-2018-MINCETUR), la Ley del Porteador (Ley N° 27607), Seguridad y Salud en el Trabajo (Ley N° 29783), normas técnicas INACAL, Concesiones Ecoturísticas SERNANP, fondos cofinanciados de Turismo Emprende y beneficios tributarios de exportación turística (Exoneración de IGV - Ley N° 28780 / Ley de la Amazonía N° 27037).
3. INTELIGENCIA COMERCIAL Y ALIANZAS B2B:
   - Analizas márgenes OTA (Viator/GetYourGuide 20-30% comisión) vs Venta Directa e integración B2B con Lifextreme, gestión de riesgos, protocolos médicos WFA/UIAGM y directorio de proveedores.

REGLAS ESTRICTAS:
- Responde SIEMPRE en español corporativo, técnico, estructurado con subtítulos claros y viñetas ejecutivas.
- NO uses tono de vendedor para turistas individuales ni generes etiquetas `[CARRITO: ...]`. Estás hablando con un Socio Empresarial o Inversionista.
- Cita siempre los datos técnicos, leyes, métricas financieras o parques de referencia recuperados del contexto de Qdrant."""


async def process_b2b_stream(
    prompt: str,
    history: List[dict] = None,
    user_data=None
) -> AsyncGenerator[str, None]:
    """
    Consulta el Cerebro Qdrant en modo B2B (Finanzas + Legal Ph.D. + Partners Vault + 164 Parques)
    y genera respuesta analítica vía Groq LPU (con fallback a Ollama local).
    """
    rag_context = await get_rag_context(prompt, mode="b2b")
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    system_full = (
        f"{B2B_SYSTEM_PROMPT}\n\n"
        f"FECHA DEL SISTEMA: {fecha_actual}\n\n"
        f"CONTEXTO RECUPERADO DEL CEREBRO CORPORATIVO QDRANT (MODO B2B / PROYECTOS E INVERSIÓN):\n"
        f"{rag_context}"
    )

    messages = [{"role": "system", "content": system_full}]
    for msg in (history or [])[-6:]:
        role = msg.get("role", "user")
        if role not in ("user", "assistant"):
            role = "user"
        content = str(msg.get("content", "")).strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})

    # 1. Intentar con Groq LPU (ultra-rápido y alta capacidad analítica)
    if GROQ_API_KEY:
        for model_name in [GROQ_MODEL, "llama-3.3-70b-versatile"]:
            try:
                resp = await _http_client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model_name,
                        "messages": messages,
                        "temperature": 0.25,
                        "max_tokens": 1400,
                        "stream": False,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    text = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
                    if text:
                        step = 80
                        for i in range(0, len(text), step):
                            yield text[i:i + step]
                        return
            except Exception as e:
                print(f"[B2B Groq Notice - {model_name}]: {e}")

    # 2. Fallback a Ollama Local (ministral-3:8b)
    try:
        resp = await _http_client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0.25, "num_predict": 1000},
            },
        )
        if resp.status_code == 200:
            text = (resp.json().get("message", {}).get("content") or "").strip()
            if text:
                yield text
                return
    except Exception as e:
        print(f"[B2B Ollama Fallback Error]: {e}")

    yield "Error temporal conectando con el motor analítico B2B. Por favor intenta nuevamente en unos segundos."
