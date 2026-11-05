import os
import sys
import json
import time
import asyncio
import urllib.request
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath("."))
load_dotenv(override=True)

from backend.src.max_agent import process_message

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
USER_PHONE = "+51958050928"
BOOKING_CODE = "LX-958050"

# Historial por chat_id
CHAT_HISTORIES = {}


def tg_request(method: str, payload: dict = None) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=35) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_tg_reply(chat_id: int, text: str):
    try:
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })
    except Exception:
        tg_request("sendMessage", {
            "chat_id": chat_id,
            "text": text.replace("*", "").replace("_", ""),
            "disable_web_page_preview": True
        })


async def poll_loop():
    print("🤖 [Telegram Bot Daemon] Escuchando mensajes en vivo para Lifextreme Multiagent Mesh...")
    offset = 0
    # Descartar updates viejos al arrancar
    try:
        init_updates = tg_request("getUpdates", {"timeout": 1})
        for u in init_updates.get("result", []):
            offset = max(offset, u["update_id"] + 1)
    except Exception as e:
        print(f"Aviso inicial getUpdates: {e}")

    while True:
        try:
            updates = tg_request("getUpdates", {"offset": offset, "timeout": 20})
            for u in updates.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message") or {}
                chat_id = msg.get("chat", {}).get("id")
                text = (msg.get("text") or "").strip()
                if not chat_id or not text:
                    continue

                sender_name = msg.get("from", {}).get("first_name", "Viajero")
                print(f"📥 [Telegram #{chat_id} - {sender_name}]: {text}")

                # Enviar indicador "escribiendo..."
                try:
                    tg_request("sendChatAction", {"chat_id": chat_id, "action": "typing"})
                except Exception:
                    pass

                hist = CHAT_HISTORIES.get(chat_id, [])

                # Si escribe /visitante simulamos visitante nuevo; por defecto usamos su teléfono +51958050928 con reserva activa
                if text.lower().startswith("/visitante"):
                    clean_text = text[len("/visitante"):].strip() or "Hola, quiero información de tours en Cusco"
                    profile = {}
                else:
                    clean_text = text
                    profile = {
                        "phone": USER_PHONE,
                        "booking_code": BOOKING_CODE,
                        "passenger_name": sender_name
                    }

                res = await process_message(clean_text, history=hist, user_data=profile)
                reply_text = res.get("mensaje", "Listo.") if isinstance(res, dict) else str(res)

                # Limpiar etiquetas internas de carrito web si existen
                import re
                reply_text = re.sub(r"\[CARR[^\]]*\]?", "", reply_text, flags=re.IGNORECASE).strip()

                send_tg_reply(chat_id, reply_text)
                print(f"📤 [Respuesta enviada a #{chat_id}]")

                hist.append({"role": "user", "content": clean_text})
                hist.append({"role": "assistant", "content": reply_text})
                CHAT_HISTORIES[chat_id] = hist[-12:]

        except Exception as e:
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(poll_loop())
