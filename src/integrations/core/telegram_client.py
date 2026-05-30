import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
    def send_alert(self, message: str):
        if not self.bot_token or not self.chat_id:
            print("[TELEGRAM] ⚠️ No se encontró Token o Chat ID en .env.")
            return False
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                print("[TELEGRAM] 🚀 Alerta enviada exitosamente al equipo.")
                return True
            else:
                print(f"[TELEGRAM] ❌ Error enviando alerta: {response.text}")
                return False
        except Exception as e:
            print(f"[TELEGRAM] ❌ Error de conexión: {e}")
            return False

# Para usar en toda la app
telegram_bot = TelegramNotifier()
