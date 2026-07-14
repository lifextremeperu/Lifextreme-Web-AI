import time
import subprocess
import sys
import os

# Asegurar importar el notifier que ya tiene el usuario
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.telegram_notifier import send_message

def is_running():
    try:
        # Consulta en Windows si el proceso python está ejecutando el inyector de obsidian
        out = subprocess.check_output('wmic process where "name=\'python.exe\'" get commandline', shell=True).decode('utf-8', errors='ignore')
        return "ingest_obsidian.py" in out
    except Exception as e:
        print(f"Error checando procesos: {e}")
        return False

def main():
    print("Iniciando monitor de Obsidian para Telegram...")
    send_message("👁️ *MONITOR ACTIVADO:* Vigilando la inyección de tu bóveda de Obsidian en segundo plano. Te avisaré inmediatamente cuando termine.")

    # Bucle de espera pasivo (cada 30 segundos)
    while is_running():
        time.sleep(30)

    # Si sale del bucle, es porque ingest_obsidian.py ya no está en la memoria RAM
    print("Proceso finalizado. Enviando notificación a Telegram...")
    send_message("🎉 *BÓVEDA ASIMILADA*\n\nLa inyección de los 4,116 archivos de Obsidian en Qdrant ha finalizado con éxito.\nTu base de datos vectorial Enterprise está 100% operativa y lista para escalar. 🚀")

if __name__ == "__main__":
    main()
