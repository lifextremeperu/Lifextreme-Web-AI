import os
import requests

# TOKEN provisto por el usuario
TOKEN = "8988648097:AAGaEYNDHqQ4EbMCRBjUGypdhPDuPS-p2P4"
OFFSET_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "telegram_offset.txt")
CHAT_ID_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "telegram_chat_id.txt")

def get_last_offset():
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, "r") as f:
            content = f.read().strip()
            return int(content) if content else None
    return None

def set_last_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))

def save_chat_id(chat_id):
    with open(CHAT_ID_FILE, "w") as f:
        f.write(str(chat_id))

def send_telegram_reply(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def fetch_new_messages():
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 10}
    offset = get_last_offset()
    if offset:
        params["offset"] = offset

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("ok"):
            updates = data.get("result", [])
            for update in updates:
                update_id = update["update_id"]
                set_last_offset(update_id + 1) # Confirmar lectura
                
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")
                
                if chat_id:
                    save_chat_id(chat_id)
                
                if text:
                    print(f"NUEVO_COMANDO|{chat_id}|{text}")
                    # Enviar acuse de recibo inmediato
                    send_telegram_reply(chat_id, f"✅ *Antigravity recibió tu orden:* `{text}`. Ejecutando ahora...")
        else:
            print("Esperando mensajes o token inválido.")
    except Exception as e:
        print(f"Error de red: {e}")

if __name__ == "__main__":
    fetch_new_messages()
