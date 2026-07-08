import subprocess
import sys
import time

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================")
    print(" >>> INICIANDO ORQUESTACIÓN: CORREDOR SUR PERÚ")
    print("==================================================")
    
    # Tacna ya pasó por el Cartógrafo, solo necesita el Minero.
    # El resto necesita ambas fases.
    regiones = [
        {"nombre": "tacna", "fase1_done": True},
        {"nombre": "apurimac", "fase1_done": False},
        {"nombre": "moquegua", "fase1_done": False},
        {"nombre": "madrededios", "fase1_done": False}
    ]
    
    for r in regiones:
        region = r["nombre"]
        print(f"\n[>>>] PROCESANDO REGIÓN: {region.upper()}")
        
        if not r["fase1_done"]:
            print(f"  -> Iniciando Fase 1: Cartógrafo ({region})...")
            subprocess.run([sys.executable, "scripts/run_cartographer.py", region])
            time.sleep(5) # Pausa entre fases
        else:
            print(f"  -> Fase 1 ya completada para {region}. Saltando Cartógrafo.")
            
        print(f"  -> Iniciando Fase 2: Minero Profundo ({region})...")
        subprocess.run([sys.executable, "scripts/run_miner_latam.py", region])
        time.sleep(10) # Pausa de enfriamiento entre regiones
        
    print("\n==================================================")
    print(" ✅ CORREDOR SUR PERÚ 100% COMPLETADO.")
    print("==================================================")

if __name__ == "__main__":
    main()
