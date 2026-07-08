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
        return
        
    path = f"data/knowledge/{region}/fqsas_deep/*.json"
    modulos_completados = len(glob.glob(path))
    
    texto = (
        f"🚀 *Lifextreme OS - REPORTE NACIONAL*\n\n"
        f"✅ Extracción B2C completada: *{region.upper()}*\n"
        f"📂 Módulos Generados (FQSAs): {modulos_completados}\n\n"
        f"Avanzando al siguiente departamento del Perú..."
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[-] Error enviando telegram: {e}")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print(" >>> INICIANDO ORQUESTACIÓN NACIONAL: TODO EL PERÚ")
    print("==================================================")
    
    # Lista maestra de departamentos pendientes (Excluyendo los ya listos o en proceso: 
    # Cusco, Arequipa, Puno, Ancash, Tacna, Apurímac, Moquegua)
    regiones_restantes = [
        "madrededios", "amazonas", "ayacucho", "cajamarca", "callao", 
        "huancavelica", "huanuco", "ica", "junin", 
        "lalibertad", "lambayeque", "lima", "loreto", 
        "pasco", "piura", "sanmartin", "tumbes", "ucayali"
    ]
    
    print(f"[+] Total de regiones en la cola nacional: {len(regiones_restantes)}\n")
    
    for region in regiones_restantes:
        print(f"==================================================")
        print(f"[>>>] PROCESANDO REGIÓN: {region.upper()}")
        print(f"==================================================")
        
        # Validar si ya existe data minada para no duplicar trabajo
        check_path = f"data/knowledge/{region}/fqsas_deep/*.json"
        if len(glob.glob(check_path)) > 0:
            print(f"[!] La región {region.upper()} ya tiene archivos JSON. Saltando para evitar duplicados...\n")
            continue
            
        try:
            print(f"  -> Fase 1: Cartógrafo ({region})...")
            subprocess.run([sys.executable, "scripts/run_cartographer.py", region])
            time.sleep(5)
                
            print(f"  -> Fase 2: Minero Profundo ({region})...")
            subprocess.run([sys.executable, "scripts/run_miner_latam.py", region])
            
            # Enviar notificación y hacer enfriamiento largo
            send_telegram_report(region)
            print(f"  [+] Notificación enviada. Enfriando motores 30 segundos...\n")
            time.sleep(30)
            
        except Exception as e:
            print(f"[-] Ocurrió un error en la región {region}: {e}")
            time.sleep(10)
        
    print("\n==================================================")
    print(" 🇵🇪 BASE DE DATOS NACIONAL 100% COMPLETADA.")
    print("==================================================")
    
    # Notificación final
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
            "chat_id": chat_id,
            "text": "🌟 *Lifextreme OS:* ¡LA EXTRACCIÓN NACIONAL HA TERMINADO! Todo el Perú está vectorizado."
        })

if __name__ == "__main__":
    main()
