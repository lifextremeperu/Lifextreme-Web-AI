"""
agent_pyme_advisor.py - El Asesor Virtual de Negocios (SaaS B2B para PYMES Turísticas)

Este script simula el envío diario de "Mentorías de Alta Dirección" por WhatsApp a 
los dueños de agencias PYME. Utiliza la bóveda Qdrant (nutrida con SUNAT, SUNAFIL, Meta Ads) 
para generar consejos hiper-personalizados.

Flujo:
1. Lee la lista de PYMES suscritas.
2. Selecciona un eje temático del día (Tributario, Laboral, Marketing, Operaciones).
3. Consulta a Qdrant por las leyes/tácticas exactas.
4. Genera un mensaje de WhatsApp persuasivo y accionable usando Mistral/DeepSeek.
5. (Simulación) Imprime el mensaje en consola listo para conectarse a Evolution API o Twilio.
"""
import os
import random
import asyncio
import httpx
from datetime import datetime
from qdrant_client import AsyncQdrantClient

# ==========================================
# CONFIGURACIÓN
# ==========================================
OLLAMA_URL = "http://localhost:11434"
QDRANT_URL = "http://localhost:6333"
KNOWLEDGE_VAULT = "Lifextreme_Knowledge"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "mistral:latest" # O deepseek-r1

qclient = AsyncQdrantClient(url=QDRANT_URL)

# Base de datos simulada de clientes PYME
PYMES_SUSCRITAS = [
    {
        "nombre_dueño": "Carlos",
        "agencia": "Andes Trekking EIRL",
        "ubicacion": "Huaraz",
        "problema_actual": "Contrata muchos guías freelance por día, teme multas de Sunafil.",
        "regimen": "Nuevo RUS"
    },
    {
        "nombre_dueño": "Sofia",
        "agencia": "Amazon Expeditions SAC",
        "ubicacion": "Iquitos",
        "problema_actual": "Vende paquetes caros a europeos, pero le cobran IGV y pierde margen.",
        "regimen": "MYPE Tributario"
    },
    {
        "nombre_dueño": "Miguel",
        "agencia": "Cusco Mágico Tours",
        "ubicacion": "Cusco",
        "problema_actual": "Bajas ventas, quiere hacer anuncios en Facebook pero no sabe segmentar.",
        "regimen": "Régimen Especial"
    }
]

# Ejes temáticos de la semana
EJES_TEMATICOS = [
    "SUNAT: Diferencia entre Locación de Servicios y Planilla (Riesgo SUNAFIL)",
    "SUNAT: Inafectación del IGV para turistas extranjeros (Exportación de Servicios)",
    "Marketing: Segmentación en Meta Ads para turistas extranjeros de alto gasto",
    "SUNAT: Límites de ventas en el Nuevo RUS y obligación de emitir facturas electrónicas"
]

async def obtener_embedding(texto: str) -> list[float]:
    """Obtiene el embedding de la consulta."""
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": texto})
            return res.json().get("embedding", [])
    except Exception as e:
        print(f"[-] Error Embedding: {e}")
        return []

async def extraer_consejo_qdrant(tema: str, limit=3) -> str:
    """Busca la doctrina oficial en Qdrant."""
    vector = await obtener_embedding(tema)
    if not vector: return ""
    
    try:
        search_result = await qclient.query_points(
            collection_name=KNOWLEDGE_VAULT, query=vector, limit=limit, score_threshold=0.3
        )
        contexto = ""
        for i, p in enumerate(search_result.points):
            texto = p.payload.get("text_content", "")
            fuente = p.payload.get("source", "Manual Oficial")
            contexto += f"\n[Fuente: {fuente}]\n{texto}\n"
        return contexto
    except Exception as e:
        print(f"[!] Error Qdrant: {e}")
        return ""

async def redactar_whatsapp(contexto_legal: str, pyme: dict, tema_dia: str) -> str:
    """Usa el LLM para redactar el mensaje de WhatsApp perfecto."""
    sys_prompt = """Eres el "Consultor Estratégico Jefe" de Lifextreme. 
Tu trabajo es asesorar a dueños de agencias de turismo PYME en Perú vía WhatsApp.
Usa un tono hiper-profesional, directo y empático (usa emojis moderadamente). 
Tus mensajes deben ser cortos, al grano, y dar una recomendación ACCIONABLE basada estrictamente en el contexto legal proporcionado.
NUNCA alucines leyes, cíñete al contexto de SUNAT/SUNAFIL/META que recibas.
Termina siempre con una pregunta de cierre para que el cliente te responda."""

    user_prompt = f"""
Hoy vas a asesorar a: {pyme['nombre_dueño']}, dueño de la agencia "{pyme['agencia']}" en {pyme['ubicacion']}.
Sabemos que su problema principal es: {pyme['problema_actual']}. Su régimen es: {pyme['regimen']}.

El tema del día es: {tema_dia}
Aquí tienes la doctrina legal/técnica extraída de nuestros manuales:
{contexto_legal}

Redacta el mensaje de WhatsApp que le enviaremos hoy por la mañana (Max 150 palabras).
"""
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": LLM_MODEL, "system": sys_prompt, "prompt": user_prompt, "stream": False}
            )
            if res.status_code == 200:
                return res.json().get("response", "")
            return "[Error al generar el mensaje]"
    except Exception as e:
        return f"[Error de conexión con Ollama: {e}]"

async def main():
    print("======================================================")
    print(" 🚀 LIFEXTREME CEO VIRTUAL - ENVIADOR WHATSAPP B2B")
    print("======================================================")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Elegir el tema del día al azar
    tema_dia = random.choice(EJES_TEMATICOS)
    print(f"[*] Tema Central de Hoy: {tema_dia}")
    
    print("[*] Consultando a Qdrant por manuales oficiales...")
    contexto = await extraer_consejo_qdrant(tema_dia)
    
    if not contexto.strip():
        print("[!] No se encontró doctrina en Qdrant. (¿Ya ejecutaste agent_pyme_ingestor.py?)")
        # Continuamos con un contexto por defecto solo para demostración
        contexto = "Según la ley peruana, hay fuertes multas por no estar en el régimen correcto o no tener SCTR."
    
    print("\n--- INICIANDO ENVÍO MASIVO DE ASESORÍAS (SIMULACIÓN) ---\n")
    
    for pyme in PYMES_SUSCRITAS:
        print(f"Generando mensaje para {pyme['agencia']} ({pyme['nombre_dueño']})...")
        mensaje = await redactar_whatsapp(contexto, pyme, tema_dia)
        
        print(f"\n[ENVIANDO A WHATSAPP DE {pyme['nombre_dueño'].upper()}] 📱")
        print("-" * 50)
        print(mensaje)
        print("-" * 50)
        print("✓ Enviado con éxito.\n")
        
        # Pausa pequeña para no saturar Ollama
        await asyncio.sleep(2)
        
    print("[+] Rondas de Mentoría Matutina Finalizadas.")

if __name__ == "__main__":
    asyncio.run(main())
