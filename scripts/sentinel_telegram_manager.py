"""
LIFEXTREME SENTINEL VIP: GESTOR DE ENLACES Y ACCESO TELEGRAM (CLI & UTILITY)
Permite generar enlaces de invitación de un solo uso, probar conectividad del bot,
y enviar mensajes de prueba al canal o grupo VIP.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# Ensure UTF-8 console output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_VIP_ID") or os.getenv("TELEGRAM_CHAT_ID")


def _telegram_api_call(method: str, payload: dict = None) -> dict:
    if not BOT_TOKEN:
        raise ValueError("Error: TELEGRAM_BOT_TOKEN no configurado en el archivo .env")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode('utf-8') if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {}
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def probar_conexion_bot():
    """Verifica si el bot de Telegram responde correctamente"""
    print("\n🔍 Verificando conexión con Telegram Bot API...")
    try:
        res = _telegram_api_call("getMe")
        if res.get("ok"):
            bot = res["result"]
            print(f"✅ BOT CONECTADO: @{bot.get('username')} (ID: {bot.get('id')})")
            print(f"   Nombre: {bot.get('first_name')}")
            return True
        else:
            print(f"❌ Error en respuesta de Telegram: {res}")
            return False
    except Exception as e:
        print(f"⚠️  No se pudo conectar a Telegram: {e}")
        return False


def crear_enlace_un_solo_uso(chat_id: str = None, nombre_cliente: str = "Agencia-VIP", expiracion_horas: int = 48) -> str:
    """Crea un enlace con límite de 1 solo miembro que expira tras su uso"""
    target_chat = chat_id or DEFAULT_CHAT_ID
    if not target_chat:
        raise ValueError("Error: Se requiere chat_id o TELEGRAM_CHANNEL_VIP_ID.")

    expire_ts = int(datetime.now().timestamp()) + (expiracion_horas * 3600)
    payload = {
        "chat_id": target_chat,
        "name": f"VIP-{nombre_cliente}"[:32],
        "member_limit": 1,
        "expire_date": expire_ts
    }

    print(f"\n🔐 Generando enlace de 1 solo uso para {nombre_cliente} en {target_chat}...")
    res = _telegram_api_call("createChatInviteLink", payload)
    if res.get("ok"):
        link = res["result"]["invite_link"]
        print(f"🎉 Enlace creado con éxito:")
        print(f"   👉 {link}")
        print(f"   ⏳ Vigencia: {expiracion_horas} horas | Límite: 1 usuario")
        return link
    else:
        print(f"❌ Error al crear enlace: {res}")
        return ""


def expulsar_usuario(chat_id: str, user_id: int):
    """Expulsa a un usuario si cancela su suscripción"""
    payload = {"chat_id": chat_id, "user_id": user_id}
    print(f"\n🚫 Revocando acceso a usuario {user_id} en canal {chat_id}...")
    _telegram_api_call("banChatMember", payload)
    _telegram_api_call("unbanChatMember", {"chat_id": chat_id, "user_id": user_id, "only_if_banned": True})
    print(f"✅ Acceso revocado.")


def enviar_mensaje(chat_id: str, texto_html: str):
    """Envía un mensaje con formato HTML"""
    payload = {
        "chat_id": chat_id or DEFAULT_CHAT_ID,
        "text": texto_html,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    return _telegram_api_call("sendMessage", payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lifextreme Sentinel VIP Telegram Manager")
    parser.add_argument("--test-bot", action="store_true", help="Probar conectividad con el bot")
    parser.add_argument("--invite", type=str, help="Generar enlace de 1 solo uso con nombre de agencia")
    parser.add_argument("--chat-id", type=str, help="ID del canal o grupo VIP")
    parser.add_argument("--kick", type=int, help="ID numérico de Telegram a expulsar")
    args = parser.parse_args()

    if args.test_bot:
        probar_conexion_bot()
    elif args.invite:
        crear_enlace_un_solo_uso(chat_id=args.chat_id, nombre_cliente=args.invite)
    elif args.kick and args.chat_id:
        expulsar_usuario(args.chat_id, args.kick)
    else:
        parser.print_help()
