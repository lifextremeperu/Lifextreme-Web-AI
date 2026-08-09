"""
evolution_bridge.py — Puente entre Evolution API y el Agente LUCA
Lifextreme.store | Área: Atención al Cliente

FUNCIÓN:
  Servidor FastAPI que actúa como PUENTE entre Evolution API (WhatsApp)
  y el Agente de Ventas LUCA (agent_whatsapp_sales.py).

  Flujo completo:
    1. Cliente escribe al +51 958050928
    2. Evolution API envía el mensaje a este webhook (puerto 8081)
    3. Este bridge extrae el texto y el número del cliente
    4. Llama a LUCA para generar la respuesta inteligente
    5. Envía la respuesta de vuelta via Evolution API con delay humano
    6. LUCA registra el lead en SQLite automáticamente

CONFIGURACIÓN:
  Puerto: 8081 (Evolution API apunta aquí)
  Evolution API: http://localhost:8080
  API Key: lifextreme_evo_2026
  Instancia: lifextreme_principal

EJECUTAR:
  python evolution_bridge.py

AUTOR: Lifextreme AI Team | v1.0.0
"""

import os
import sys
import asyncio
import random
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════
EVOLUTION_URL      = "http://localhost:8090"
EVOLUTION_API_KEY  = "lifextreme_evo_2026"
EVOLUTION_INSTANCE = "lifextreme_principal"

# Puerto donde escucha este bridge
BRIDGE_PORT = 8081

# Delays humanos anti-ban (en segundos)
DELAY_MIN = 2.0   # Mínimo 2 segundos antes de responder
DELAY_MAX = 5.0   # Máximo 5 segundos (simula que alguien escribe)

# Números bloqueados (evitar responder a sí mismo)
NUMEROS_IGNORAR = [
    "51958050928",  # Número propio de Lifextreme
    "status",       # Status de WhatsApp
]

app = FastAPI(title="Lifextreme — Evolution Bridge (LUCA)", version="1.0.0")


# ══════════════════════════════════════════════
# ENVIAR MENSAJE VIA EVOLUTION API
# ══════════════════════════════════════════════
async def enviar_mensaje_whatsapp(numero: str, mensaje: str) -> bool:
    """
    Envía un mensaje de respuesta via Evolution API.
    Incluye delay humano para evitar detección de bot.
    """
    # ── Delay humano ANTES de enviar (anti-ban crítico)
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    print(f"   [⌛] Simulando escritura humana ({delay:.1f}s)...")
    await asyncio.sleep(delay)

    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": numero,
        "text": mensaje,
        "delay": int(delay * 1000)  # Evolution también aplica delay adicional (ms)
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=payload, headers=headers)
            if res.status_code in [200, 201]:
                print(f"   [✓] Mensaje enviado a {numero}")
                return True
            else:
                print(f"   [!] Error Evolution API: {res.status_code} — {res.text[:200]}")
                return False
    except Exception as e:
        print(f"   [!] Error de conexión con Evolution: {e}")
        return False


# ══════════════════════════════════════════════
# WEBHOOK PRINCIPAL — RECIBE MENSAJES DE EVOLUTION
# ══════════════════════════════════════════════
@app.post("/webhook/evolution")
async def recibir_webhook(request: Request):
    """
    Endpoint que recibe todos los eventos de Evolution API.
    Filtra solo mensajes de texto entrantes y los pasa a LUCA.
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON inválido")

    evento = data.get("event", "")
    print(f"\n[📨] Evento recibido: {evento}")

    # ── Solo procesar mensajes nuevos entrantes
    if evento != "messages.upsert":
        return JSONResponse({"status": "ignorado", "evento": evento})

    # ── Extraer datos del mensaje
    try:
        mensaje_data = data.get("data", {})
        key          = mensaje_data.get("key", {})
        from_me      = key.get("fromMe", False)
        remote_jid   = key.get("remoteJid", "")  # Ej: "51987654321@s.whatsapp.net"
        numero_raw   = remote_jid.replace("@s.whatsapp.net", "").replace("@g.us", "")

        # ── Ignorar mensajes propios y grupos
        if from_me:
            print(f"   [→] Mensaje propio ignorado.")
            return JSONResponse({"status": "ignorado", "razon": "fromMe"})

        if "@g.us" in remote_jid:
            print(f"   [→] Mensaje de grupo ignorado.")
            return JSONResponse({"status": "ignorado", "razon": "grupo"})

        if numero_raw in NUMEROS_IGNORAR:
            print(f"   [→] Número en lista de ignorados: {numero_raw}")
            return JSONResponse({"status": "ignorado", "razon": "numero_bloqueado"})

        # ── Extraer texto del mensaje
        message = mensaje_data.get("message", {})
        texto = (
            message.get("conversation")
            or message.get("extendedTextMessage", {}).get("text")
            or message.get("imageMessage", {}).get("caption")
            or ""
        ).strip()

        if not texto:
            print(f"   [→] Mensaje sin texto (imagen/audio/sticker) — ignorado.")
            return JSONResponse({"status": "ignorado", "razon": "sin_texto"})

        # ── Extraer nombre del contacto (si disponible)
        push_name = mensaje_data.get("pushName", "Turista")

        print(f"   [👤] De: {numero_raw} ({push_name})")
        print(f"   [💬] Mensaje: {texto[:100]}")

    except Exception as e:
        print(f"   [!] Error extrayendo datos del webhook: {e}")
        return JSONResponse({"status": "error", "detalle": str(e)})

    # ── Llamar a LUCA de forma asíncrona
    asyncio.create_task(
        procesar_con_luca(numero_raw, texto, push_name)
    )

    # Responder rápido a Evolution para no hacer timeout
    return JSONResponse({"status": "procesando", "numero": numero_raw})


async def procesar_con_luca(numero: str, texto: str, nombre: str):
    """Llama a LUCA y envía la respuesta por WhatsApp."""
    try:
        # Importar LUCA dinámicamente
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
        from agent_whatsapp_sales import procesar_mensaje_whatsapp

        print(f"   [🤖] LUCA procesando mensaje de {nombre}...")
        resultado = await procesar_mensaje_whatsapp(
            mensaje=texto,
            telefono=numero,
            nombre=nombre
        )

        respuesta  = resultado.get("respuesta", "")
        lead_id    = resultado.get("lead_id", 0)
        estado     = resultado.get("estado", "NUEVO")

        print(f"   [📋] Lead #{lead_id} | Estado: {estado}")
        print(f"   [💡] Respuesta LUCA: {respuesta[:120]}...")

        if respuesta:
            await enviar_mensaje_whatsapp(numero, respuesta)
        else:
            print("   [!] LUCA no generó respuesta.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"   [!] Error en LUCA: {e}")
        # Fallback humano si LUCA falla
        fallback = (
            "¡Hola! 👋 Gracias por escribirnos. Soy del equipo Lifextreme Perú 🏔️\n"
            "En este momento estamos procesando tu consulta. "
            "Te respondemos en breve. También puedes llamarnos: 958 050 928"
        )
        await enviar_mensaje_whatsapp(numero, fallback)


# ══════════════════════════════════════════════
# ENDPOINT DE SALUD
# ══════════════════════════════════════════════
@app.get("/health")
def health():
    return {
        "status":    "🟢 LUCA Bridge activo",
        "evolution": EVOLUTION_URL,
        "instancia": EVOLUTION_INSTANCE,
        "puerto":    BRIDGE_PORT,
        "agente":    "LUCA — Asesor de Ventas B2C 24/7"
    }


@app.get("/")
def root():
    return {
        "nombre":    "Lifextreme Evolution Bridge",
        "version":   "1.0.0",
        "webhook":   f"http://localhost:{BRIDGE_PORT}/webhook/evolution",
        "health":    f"http://localhost:{BRIDGE_PORT}/health"
    }


# ══════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  🌉 LIFEXTREME — EVOLUTION BRIDGE")
    print("  LUCA conectado a WhatsApp Business")
    print("=" * 60)
    print(f"  Puerto Bridge:    {BRIDGE_PORT}")
    print(f"  Evolution API:    {EVOLUTION_URL}")
    print(f"  Instancia:        {EVOLUTION_INSTANCE}")
    print(f"  Delay anti-ban:   {DELAY_MIN}s – {DELAY_MAX}s")
    print(f"  Webhook URL:      http://localhost:{BRIDGE_PORT}/webhook/evolution")
    print("=" * 60)
    print("\n  ✅ Pasos completados antes de arrancar:")
    print("  1. Evolution API corriendo (docker compose up)")
    print("  2. Instancia creada y QR escaneado")
    print("  3. WhatsApp Web CERRADO en el navegador")
    print("\n  Escribe desde OTRO número al +51 958050928 para probar 🎯")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=BRIDGE_PORT, log_level="warning")
