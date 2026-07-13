import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8')

def run_script(script_name):
    print(f"\n=======================================================")
    print(f" ⚙️ EJECUTANDO: {script_name}")
    print(f"=======================================================")
    
    # Usamos subprocess.Popen para transmitir el output en vivo a la consola
    process = subprocess.Popen(
        [sys.executable, f"scripts/{script_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    output_lines = []
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            clean_line = line.strip()
            print(clean_line)
            output_lines.append(clean_line)
            
    rc = process.poll()
    return rc, output_lines

def main():
    print("===================================================================")
    print(" 🌙 LIFEXTREME BRAIN: MODO INGESTA NOCTURNA (BUCLE CONTINUO) 🌙")
    print("===================================================================")
    print("Este script procesará TODOS los archivos en lotes de 100.")
    print("Puedes dejar la computadora encendida. Terminaremos automáticamente.\n")
    
    # 1. Escanear discos para capturar INV DE MERCADO y archivos nuevos
    run_script("smart_drive_scanner_v2.py")
    
    ciclo = 1
    while True:
        print(f"\n\n=======================================================")
        print(f" 🔄 INICIANDO CICLO DE INGESTA #{ciclo} ")
        print(f"=======================================================")
        
        # 2. Extraer 100 archivos
        rc, out_lines = run_script("run_smart_ingestion.py")
        
        # Verificar si ya terminamos todo
        finished = False
        for line in out_lines:
            if "Archivos procesados y encolados: 0" in line:
                finished = True
                break
                
        if finished:
            print("\n===================================================================")
            print(" 🎉 ¡MODO NOCTURNO COMPLETADO! Todos los archivos fueron ingeridos. ")
            print("===================================================================")
            break
            
        # 3. Vaciar la cola en Qdrant
        run_script("queue_to_qdrant.py")
        
        print(f"\n[+] Ciclo #{ciclo} completado. Iniciando el siguiente en 5 segundos...")
        time.sleep(5)
        ciclo += 1

if __name__ == "__main__":
    main()
