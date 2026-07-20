import os
import sys
import subprocess
import time
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = os.path.dirname(__file__)

TASKS = [
    {
        "id": "2",
        "name": "Minería e Inyección de Regulaciones TUPA (Cerebro B2B)",
        "script": "agent_tupa_downloader.py"
    },
    {
        "id": "3",
        "name": "Limpieza y Auditoría de la Base de Datos Master B2B",
        "script": "clean_b2b_database.py"
    },
    {
        "id": "4",
        "name": "Simulación de Guerra y Calibración RAG (Benchmark)",
        "script": "rag_benchmark.py"
    },
    {
        "id": "5",
        "name": "Caza-Bugs Autónomo (Optimización Web SEO)",
        "script": "audit_web_code.py"
    }
]

def run_task(task):
    script_path = os.path.join(SCRIPTS_DIR, task["script"])
    if not os.path.exists(script_path):
        print(f"\n[!] ERROR: El script {task['script']} no existe. Saltando tarea...")
        return False
        
    print(f"\n{'='*60}")
    print(f" ▶ INICIANDO TAREA {task['id']}: {task['name']}")
    print(f" 🕒 HORA: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        # Ejecutar y esperar
        result = subprocess.run([sys.executable, script_path], check=True, text=True)
        print(f"\n[✔] TAREA {task['id']} COMPLETADA CON ÉXITO.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[X] TAREA {task['id']} FALLÓ CON ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n[X] ERROR INESPERADO EN TAREA {task['id']}: {e}")
        return False

def main():
    print(r"""
    ========================================================
     ☀️  LIFEXTREME AI - ORQUESTADOR AUTÓNOMO MATUTINO ☀️ 
    ========================================================
    Tareas programadas para esta sesión:
    2. Minería TUPA
    3. Curación Base de Datos B2B
    4. Calibración RAG Benchmark
    5. Auditoría Web (Caza-Bugs)
    ========================================================
    """)
    
    time.sleep(3)
    
    for task in TASKS:
        run_task(task)
        
        # Guardado y Pausa entre tareas
        print("\n[⏳] Guardando estados y limpiando memoria RAM antes de la siguiente tarea...")
        time.sleep(10)
        
    print("\n" + "="*60)
    print(" 🎉 TODAS LAS TAREAS MATUTINAS HAN FINALIZADO 🎉")
    print("="*60)
    print("Ya puedes revisar los reportes y la base de datos limpia.")
    
    # Mantener la ventana abierta
    os.system('pause >nul')

if __name__ == "__main__":
    main()
