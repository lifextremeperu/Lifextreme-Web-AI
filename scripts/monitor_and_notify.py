import time
import os
import requests
import psutil
from dotenv import load_dotenv

def send_message(text):
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error enviando telegram: {e}")

def is_uploader_running():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['cmdline'] and 'nightly_vector_uploader.py' in ' '.join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

if __name__ == "__main__":
    print("Iniciando monitor de Telegram...")
    # send_message("⚙️ *Lifextreme OS:* Monitoreando la Ingesta Nocturna. Te avisaré cuando el Motor Gecko termine de procesar los vectores.")
    
    # Esperar hasta que el proceso desaparezca
    running = True
    while running:
        if not is_uploader_running():
            running = False
        else:
            time.sleep(30)
            
    send_message("✅ *Lifextreme OS - REPORTE NOCTURNO:* \n\n¡La Fase 1 ha finalizado! El archivo maestro `master_vectors_to_upload.jsonl` está listo con miles de vectores B2C. \n\nBuenas noches, CEO.")
    print("Notificación enviada.")
