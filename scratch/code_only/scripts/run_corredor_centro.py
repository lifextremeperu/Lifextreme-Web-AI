import subprocess
import sys
import time
import os
import glob
import requests
from dotenv import load_dotenv

def send_telegram_report(region):
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        print("[-] Credenciales de Telegram no configuradas. Omitiendo notificación.")
        return
        
    # Contar módulos minados
    path = f"data/knowledge/{region}/fqsas_deep/*.json"
    modulos_completados = len(glob.glob(path))
    
    texto = (
        f"🚀 *Lifextreme OS - REPORTE DE EXTRACCIÓN*\n\n"
        f"✅ Misión completada para la región: *{region.upper()}*\n"
        f"📂 Módulos B2C Generados (FQSAs): {modulos_completados}\n\n"
        f"El Cerebro sigue expandiéndose al siguiente destino..."
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
        print(f"[+] Notificación de Telegram enviada para {region.upper()}")
    except Exception as e:
        print(f"[-] Error enviando telegram: {e}")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print(" >>> INICIANDO ORQUESTACIÓN: CORREDOR CENTRO PERÚ")
    print("==================================================")
    
    regiones = ["junin", "pasco", "huanuco", "huancavelica", "ica"]
    
    for region in regiones:
        print(f"\n[>>>] PROCESANDO REGIÓN: {region.upper()}")
        
        print(f"  -> Iniciando Fase 1: Cartógrafo ({region})...")
        subprocess.run([sys.executable, "scripts/run_cartographer.py", region])
        time.sleep(5) # Pausa de seguridad
            
        print(f"  -> Iniciando Fase 2: Minero Profundo ({region})...")
        subprocess.run([sys.executable, "scripts/run_miner_latam.py", region])
        
        # Enviar reporte directo a Telegram
        send_telegram_report(region)
        
        time.sleep(10) # Enfriamiento antes del siguiente departamento
        
    print("\n==================================================")
    print(" ✅ CORREDOR CENTRO PERÚ 100% COMPLETADO.")
    print("==================================================")

if __name__ == "__main__":
    main()
