import time
import os
import glob
import requests
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

def get_json_count(region):
    path = f"data/knowledge/{region}/fqsas_deep/*.json"
    return len(glob.glob(path))

def main():
    regiones = ["tacna", "apurimac", "moquegua", "madrededios"]
    notificadas = {r: False for r in regiones}
    
    print("Iniciando Monitor de Telegram para el Corredor Sur...")
    
    while not all(notificadas.values()):
        for region in regiones:
            if notificadas[region]:
                continue
                
            # Asumimos que si no hay cambios en la cantidad de archivos JSON 
            # durante 3 minutos, y hay al menos 1 archivo, la región terminó.
            # Una forma más sencilla: leer el reporte de inteligencia o chequear procesos.
            # Para este monitor simple, enviaremos cuando detecte > 0 json y pasen 5 mins sin cambios.
            # O mejor: El orquestador pausa 10 segs entre regiones.
            pass
            
        time.sleep(30)
