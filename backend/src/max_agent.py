import os
import json
from pydantic_ai import Agent, RunContext
from .models import MAXResponse, Cotizacion, PerfilUsuario
from typing import List, Optional, Literal

# --- CONFIGURACION DEL AGENTE ---
# Prioriza variables de entorno para máxima flexibilidad en la nube
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-hub-cusco-2026')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://hub-cusco-2026.tail883d62.ts.net/v1')

max_agent = Agent(
    'openai:hub-llama3', 
    output_type=MAXResponse,
    system_prompt=(
        "Eres MAX, el Asesor Maestro de Aventura de Lifextreme. Tu objetivo es cerrar reservas "
        "usando el Lifextreme Pro System (30/30/40). Hablas con autoridad técnica (UIAGM). "
        "Usa siempre el ADN de ventas (Sales DNA) para responder con los valores de la marca."
    )
)

# --- HERRAMIENTAS (TOOLS) ---

@max_agent.tool
async def consultar_adn_ventas(ctx: RunContext[None], query: str) -> str:
    """Consulta el ADN de ventas y doctrina de Lifextreme para responder correctamente."""
    try:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "max_sales_dna.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                dna = json.load(f)
                # Búsqueda simple por palabras clave en el ADN
                relevant = [str(v) for k, v in dna.items() if any(word in str(v).lower() for word in query.lower().split())]
                return "\n".join(relevant[:3]) if relevant else "Usa el tono de experto UIAGM."
        return "Sigue el protocolo 30/30/40."
    except Exception as e:
        return f"Error consultando ADN: {str(e)}"

@max_agent.tool
async def generar_link_pago_niubiz(ctx: RunContext[None], monto: float) -> str:
    """Genera un link de pago dinámico usando la API de Niubiz para la reserva del 30%."""
    return f"https://niubiz.visanet.com.pe/pay/lifextreme_resva_{int(monto)}"

@max_agent.tool
async def calcular_ahorro_membresia(ctx: RunContext[None], monto_total: float) -> str:
    """Calcula el ahorro si el usuario decide comprar la membresía Elite."""
    ahorro = monto_total * 0.15
    return (f"Si te unes hoy al Club Elite por S/ 450, ahorras S/ {ahorro} en esta compra "
            f"y viajas al costo todo el año.")

# --- LÓGICA DE PROCESAMIENTO ---
async def process_message(prompt: str, history: List[dict] = None, user_data: Optional[PerfilUsuario] = None):
    # Ejecución asíncrona del agente con el historial de conversación
    result = await max_agent.run(prompt, message_history=history)
    return result.data
