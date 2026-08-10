"""
agent_whatsapp_sales.py — AGENTE DE VENTAS B2C 24/7 POR WHATSAPP
Área: Atención al Cliente & CRM — Lifextreme.store

FUNCIÓN:
  Convierte prospectos B2C (turistas individuales) en reservas reales.
  Opera las 24 horas usando IA generativa + RAG sobre Qdrant.
  Simula el flujo completo de ventas: saludo → calificación → cotización → cierre.

FLUJO DE VENTA LIFEXTREME (Sistema 30/30/40):
  1. Saludo personalizado + detección de interés (destino, fechas, grupo)
  2. Consulta al RAG de Qdrant para extraer precios e itinerarios reales
  3. Genera cotización personalizada con el sistema de pagos 30/30/40
  4. Ofrece el link de pago (Yape / Plin / Transferencia)
  5. Registra el lead en la base de datos local (SQLite) para seguimiento

INTEGRACIÓN:
  - Ollama (LLM local: mistral:latest o qwen2.5:7b)
  - Qdrant (base vectorial: Lifextreme_Knowledge)
  - SQLite (registro de leads y estado del funnel)
  - [Fase 2] Evolution API para envío real por WhatsApp Business API

AUTOR: Lifextreme AI Team
VERSIÓN: 1.0.0
"""

import os
import sys
import asyncio
import json
import sqlite3
import httpx
from datetime import datetime
from typing import Optional
from qdrant_client import AsyncQdrantClient

sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════
# CONFIGURACIÓN CENTRAL
# ══════════════════════════════════════════════
OLLAMA_URL      = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
QDRANT_URL      = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION      = "Lifextreme_Knowledge"
EMBED_MODEL     = "nomic-embed-text"
LLM_MODEL       = os.getenv("LLM_MODEL", "mistral:latest")

# Datos de contacto Lifextreme
WHATSAPP_NUMBER = "51958050928"
YAPE_NUMBER     = "958 050 928"
WEB_URL         = "https://www.lifextreme.store"
EMAIL_CONTACTO  = "contacto@lifextreme.store"

# Base de datos de leads
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data", "whatsapp_leads.db"
)

qclient = AsyncQdrantClient(url=QDRANT_URL)


# ══════════════════════════════════════════════
# SISTEMA PROMPT DEL AGENTE DE VENTAS
# ══════════════════════════════════════════════
SALES_AGENT_PROMPT = """
Eres LUCA, el Asesor de Aventuras de Lifextreme Peru. 🏔️
Tu único objetivo es convertir consultas de turistas en RESERVAS CONFIRMADAS.

PERSONALIDAD:
- Empático, entusiasta y profesional. Usas emojis con moderación.
- Hablas como un guía peruano experto que ama su país.
- NUNCA eres robótico ni repetitivo.

PROTOCOLO DE VENTA (sigue este orden):
1. DETECTAR: Identifica destino de interés, número de personas, fechas y presupuesto.
2. RECOMENDAR: Sugiere el paquete más adecuado basándote SOLO en el contexto del RAG.
3. COTIZAR: Presenta la cotización con el sistema 30/30/40 de forma clara.
4. CERRAR: Ofrece el link de reserva y los medios de pago.
5. GUARDRAIL: Si el cliente pide Camino Inca / Machu Picchu para menos de 30 días, 
   explica que el MINCETUR tiene cupos agotados y ofrece alternativas: 
   Salkantay, Choquequirao, Lares, Huchuy Qosqo.

SISTEMA DE PAGOS LIFEXTREME 30/30/40:
  💳 1er pago (30%) = asegura el cupo HOY
  💳 2do pago (30%) = 7 días antes del tour
  💳 Saldo final (40%) = el día del tour
  Medios: Yape {yape} | Transferencia BCP/Interbank | Tarjeta online

REGLAS CRÍTICAS:
- Responde SIEMPRE en español.
- Si no tienes información de precio en el contexto RAG, di "déjame confirmarte el precio exacto" 
  y ofrece el contacto directo con un humano: wa.me/{numero}.
- Máximo 200 palabras por respuesta.
- Termina SIEMPRE con una pregunta o llamado a la acción.
- NUNCA inventes precios ni fechas de disponibilidad.
""".format(yape=YAPE_NUMBER, numero=WHATSAPP_NUMBER)


# ══════════════════════════════════════════════
# BASE DE DATOS DE LEADS
# ══════════════════════════════════════════════
def init_leads_db():
    """Inicializa la base de datos SQLite para tracking de leads."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            telefono    TEXT,
            nombre      TEXT,
            destino     TEXT,
            fecha_viaje TEXT,
            personas    INTEGER,
            presupuesto TEXT,
            estado      TEXT DEFAULT 'NUEVO',
            ultima_msg  TEXT,
            creado_en   TEXT DEFAULT CURRENT_TIMESTAMP,
            actualizado TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id     INTEGER,
            rol         TEXT,  -- 'user' o 'assistant'
            mensaje     TEXT,
            timestamp   TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(lead_id) REFERENCES leads(id)
        )
    """)
    conn.commit()
    conn.close()
    print("[✓] Base de datos de leads lista.")

# Auto-inicializar al importar (bridge no ejecuta __main__)
init_leads_db()

def registrar_lead(telefono: str, destino: str = None, nombre: str = None) -> int:
    """Registra o actualiza un lead en la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM leads WHERE telefono = ?", (telefono,))
    row = cursor.fetchone()
    if row:
        lead_id = row[0]
        if destino:
            cursor.execute(
                "UPDATE leads SET destino=?, actualizado=? WHERE id=?",
                (destino, datetime.now().isoformat(), lead_id)
            )
    else:
        cursor.execute(
            "INSERT INTO leads (telefono, nombre, destino) VALUES (?, ?, ?)",
            (telefono, nombre or "Turista", destino)
        )
        lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lead_id


def guardar_mensaje(lead_id: int, rol: str, mensaje: str):
    """Registra cada mensaje de la conversación."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversaciones (lead_id, rol, mensaje) VALUES (?, ?, ?)",
        (lead_id, rol, mensaje)
    )
    cursor.execute(
        "UPDATE leads SET ultima_msg=?, actualizado=? WHERE id=?",
        (mensaje[:200], datetime.now().isoformat(), lead_id)
    )
    conn.commit()
    conn.close()


def actualizar_estado_lead(lead_id: int, estado: str):
    """Estados: NUEVO → CALIFICADO → COTIZADO → RESERVADO → PERDIDO"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE leads SET estado=?, actualizado=? WHERE id=?",
        (estado, datetime.now().isoformat(), lead_id)
    )
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════
# MOTOR RAG — BÚSQUEDA EN QDRANT
# ══════════════════════════════════════════════
async def obtener_embedding(texto: str) -> list:
    """Genera el vector de embeddings para la consulta."""
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBED_MODEL, "prompt": texto}
            )
            return res.json().get("embedding", [])
    except Exception as e:
        print(f"[!] Error embedding: {e}")
        return []


async def buscar_tours_rag(consulta: str, limite: int = 4) -> str:
    """Busca información de tours en Qdrant y devuelve contexto formateado."""
    vector = await obtener_embedding(consulta)
    if not vector:
        return "Sin contexto RAG disponible."
    try:
        resultados = await qclient.query_points(
            collection_name=COLLECTION,
            query=vector,
            limit=limite,
            score_threshold=0.3
        )
        if not resultados.points:
            return "No encontré información específica sobre ese tour en nuestra base de datos."
        partes = []
        for i, punto in enumerate(resultados.points, 1):
            texto    = punto.payload.get("text_content", "")
            modulo   = punto.payload.get("modulo_nombre", "Tour")
            region   = punto.payload.get("region", "Perú").capitalize()
            score    = round(punto.score, 2)
            partes.append(f"[Tour {i} | {modulo} | {region} | relevancia: {score}]\n{texto}")
        return "\n\n---\n\n".join(partes)
    except Exception as e:
        print(f"[!] Error Qdrant: {e}")
        return "Base de conocimiento no disponible temporalmente."


# ══════════════════════════════════════════════
# GENERADOR DE COTIZACIÓN
# ══════════════════════════════════════════════
def generar_cotizacion(nombre_tour: str, precio_total: float, personas: int = 1) -> str:
    """Genera el detalle de pago con el sistema 30/30/40."""
    precio_pp       = precio_total
    total           = precio_total * personas
    primer_pago     = round(total * 0.30, 2)
    segundo_pago    = round(total * 0.30, 2)
    saldo_final     = round(total * 0.40, 2)

    return f"""
╔══════════════════════════════════════╗
   🏔️  COTIZACIÓN LIFEXTREME
╚══════════════════════════════════════╝
  Tour: {nombre_tour}
  Precio por persona: S/ {precio_pp:.2f}
  Personas: {personas}
  ─────────────────────────────────────
  TOTAL: S/ {total:.2f}

  📅 PLAN DE PAGOS (30/30/40):
  ✅ Hoy (30%) — Asegura tu cupo:   S/ {primer_pago:.2f}
  📆 7 días antes (30%):             S/ {segundo_pago:.2f}
  🗓️  Día del tour (40%):            S/ {saldo_final:.2f}

  💳 MEDIOS DE PAGO:
  • Yape: {YAPE_NUMBER}
  • WhatsApp: wa.me/{WHATSAPP_NUMBER}
  • Web: {WEB_URL}

  ⚡ Reserva ahora → ¡Cupos limitados!
""".strip()


# ══════════════════════════════════════════════
# MOTOR DE RESPUESTA CON IA
# ══════════════════════════════════════════════
async def generar_respuesta_ventas(
    mensaje_cliente: str,
    contexto_rag: str,
    historial: list[dict]
) -> str:
    """Genera la respuesta del agente de ventas usando el LLM."""
    
    # Construir historial en formato Ollama
    mensajes_previos = ""
    for msg in historial[-6:]:  # últimos 6 turnos para no saturar el contexto
        rol    = "Cliente" if msg["rol"] == "user" else "LUCA"
        mensajes_previos += f"\n{rol}: {msg['mensaje']}"

    prompt_completo = f"""
{SALES_AGENT_PROMPT}

╔══ INFORMACIÓN DE TOURS (base de conocimiento RAG) ══╗
{contexto_rag}
╚════════════════════════════════════════════════════╝

HISTORIAL DE CONVERSACIÓN:
{mensajes_previos}

Cliente: {mensaje_cliente}

LUCA:"""

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            res = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model":  LLM_MODEL,
                    "prompt": prompt_completo,
                    "stream": False,
                    "options": {
                        "temperature": 0.65,
                        "top_p": 0.9,
                        "num_predict": 350
                    }
                }
            )
            if res.status_code == 200:
                return res.json().get("response", "").strip()
            return f"[Error {res.status_code} del LLM]"
    except Exception as e:
        return (
            f"¡Hola! 👋 Soy LUCA de Lifextreme. Estamos experimentando un problema técnico. "
            f"Por favor contáctanos directamente: wa.me/{WHATSAPP_NUMBER} o llama al {YAPE_NUMBER}. "
            f"¡Te ayudamos a reservar tu aventura en segundos! 🏔️"
        )


# ══════════════════════════════════════════════
# MOTOR PRINCIPAL DE CONVERSACIÓN
# ══════════════════════════════════════════════
async def procesar_mensaje_whatsapp(
    mensaje: str,
    telefono: str = "demo",
    nombre: str   = "Turista"
) -> dict:
    """
    Punto de entrada principal del agente.
    Recibe el mensaje del cliente y devuelve la respuesta del agente.

    Retorna:
        dict con keys: respuesta, lead_id, estado, cotizacion
    """
    # 1. Registrar lead
    lead_id = registrar_lead(telefono, nombre=nombre)
    guardar_mensaje(lead_id, "user", mensaje)

    # 2. Buscar información en RAG
    contexto = await buscar_tours_rag(mensaje)

    # 3. Recuperar historial reciente
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rol, mensaje FROM conversaciones WHERE lead_id=? ORDER BY id DESC LIMIT 8",
        (lead_id,)
    )
    historial_raw = cursor.fetchall()
    conn.close()
    historial = [{"rol": r[0], "mensaje": r[1]} for r in reversed(historial_raw)]

    # 4. Generar respuesta
    respuesta = await generar_respuesta_ventas(mensaje, contexto, historial)
    guardar_mensaje(lead_id, "assistant", respuesta)

    # 5. Detectar si hay intención de compra para actualizar estado del lead
    palabras_cierre = ["reservar", "quiero", "sí", "si", "cuánto", "precio", "pagar", "confirmar", "me interesa", "cupos"]
    estado = "CALIFICADO"
    if any(p in mensaje.lower() for p in palabras_cierre):
        estado = "COTIZADO"
        actualizar_estado_lead(lead_id, estado)

    # 6. Detectar si se generó cotización para incluirla por separado
    cotizacion = None
    if "s/" in respuesta.lower() or "soles" in respuesta.lower():
        estado = "COTIZADO"
        actualizar_estado_lead(lead_id, estado)

    return {
        "respuesta":  respuesta,
        "lead_id":    lead_id,
        "estado":     estado,
        "cotizacion": cotizacion
    }


# ══════════════════════════════════════════════
# MODO DEMO INTERACTIVO EN TERMINAL
# ══════════════════════════════════════════════
async def modo_demo():
    """Simula una conversación de WhatsApp en la terminal para pruebas."""
    print("=" * 60)
    print(" 📱 LIFEXTREME — AGENTE DE VENTAS B2C WHATSAPP (DEMO)")
    print(" Área: Atención al Cliente | Agente: LUCA")
    print("=" * 60)
    print(f" LLM: {LLM_MODEL} | RAG: Qdrant {COLLECTION}")
    print(f" DB Leads: {DB_PATH}")
    print("-" * 60)
    print(" Escribe como si fueras un turista por WhatsApp.")
    print(" Comandos especiales:")
    print("   /cotizar <tour> <precio> <personas>  → Genera cotización")
    print("   /leads                               → Ver leads en BD")
    print("   /salir                               → Terminar")
    print("=" * 60)

    init_leads_db()
    telefono_demo = f"+51{int(datetime.now().timestamp())}"[-12:]
    print(f"\n[Sistema] Sesión demo. Teléfono simulado: {telefono_demo}\n")

    # Mensaje de bienvenida automático
    bienvenida = (
        f"¡Hola! 👋 Soy LUCA, tu asesor de aventuras en Lifextreme Perú 🏔️\n"
        f"¿A qué destino increíble quieres viajar? Cuéntame tus fechas y cuántas personas son. "
        f"¡Te armo la mejor aventura de tu vida! ✨"
    )
    print(f"LUCA 🤖: {bienvenida}\n")

    while True:
        try:
            entrada = input("Tú 👤: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Sistema] Sesión terminada.")
            break

        if not entrada:
            continue

        # Comando: salir
        if entrada.lower() in ["/salir", "/exit", "q", "quit"]:
            print("[Sistema] ¡Hasta luego! 👋")
            break

        # Comando: ver leads
        if entrada.lower() == "/leads":
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, destino, estado, actualizado FROM leads ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            conn.close()
            print("\n[BD Leads]")
            print(f"{'ID':<5} {'Nombre':<15} {'Destino':<20} {'Estado':<12} {'Actualizado'}")
            print("-" * 70)
            for r in rows:
                print(f"{r[0]:<5} {(r[1] or ''):<15} {(r[2] or ''):<20} {(r[3] or ''):<12} {r[4]}")
            print()
            continue

        # Comando: generar cotización manual
        if entrada.lower().startswith("/cotizar"):
            partes = entrada.split(" ", 3)
            try:
                nombre_tour  = partes[1] if len(partes) > 1 else "Tour Personalizado"
                precio       = float(partes[2]) if len(partes) > 2 else 500.0
                personas     = int(partes[3]) if len(partes) > 3 else 1
                cot          = generar_cotizacion(nombre_tour, precio, personas)
                print(f"\n{cot}\n")
            except (IndexError, ValueError):
                print("[!] Uso: /cotizar <nombre_tour> <precio_persona> <personas>")
            continue

        # Procesar mensaje normal
        print("\n[LUCA está escribiendo...] ⌨️")
        resultado = await procesar_mensaje_whatsapp(
            mensaje=entrada,
            telefono=telefono_demo,
            nombre="Demo"
        )
        print(f"\nLUCA 🤖: {resultado['respuesta']}")
        print(f"   [Lead #{resultado['lead_id']} | Estado: {resultado['estado']}]\n")


# ══════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════
if __name__ == "__main__":
    asyncio.run(modo_demo())
