import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Error: No se encontró el Token o el Chat ID en el archivo .env")
    sys.exit(1)

def send_telegram_message(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Mensaje enviado exitosamente a Telegram!")
        else:
            print(f"❌ Error al enviar: {response.text}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

mensaje_prueba = """
🤖 *LIFEXTREME AI - CONEXIÓN ESTABLECIDA*

¡Hola! Soy tu Agente de Inteligencia Artificial.
Esta es una prueba del sistema de monitoreo en tiempo real.

📊 *Métricas Actuales:*
- Estado: En Línea
- Proyecto: Turismo Global LATAM
- Conexión IDE: *OK*

Preparado para enviar reportes de minería en vivo. 🚀
"""

send_telegram_message(mensaje_prueba)
