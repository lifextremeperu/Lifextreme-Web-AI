import os
import subprocess
import time
import sys

DEPARTMENTS = [
    "Amazonas", "Apurimac", "Arequipa", "Ayacucho", "Cajamarca", 
    "Callao", "Huancavelica", "Huanuco", "Ica", "Junin", 
    "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", 
    "Moquegua", "Pasco", "Piura", "Puno", "San Martin", 
    "Tacna", "Tumbes", "Ucayali"
]

def main():
    # Force UTF-8 encoding for Windows CMD
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("="*60)
    print("🚀 INICIANDO EXPANSIÓN NACIONAL LIFEXTREME (V10)")
    print("="*60)
    print(f"Total departamentos a procesar: {len(DEPARTMENTS)}")
    print("="*60)

    current_id = 11

    # Fix paths to work correctly regardless of where the script is called from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_script = os.path.join(script_dir, "expand_tours_agents.py")

    for dept in DEPARTMENTS:
        print(f"\n➤ Procesando: {dept} (IDs: {current_id} a {current_id + 4})")
        
        cmd = [
            sys.executable,
            "-u",
            agent_script, 
            "--dept", dept, 
            "--start_id", str(current_id)
        ]
        
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        try:
            result = subprocess.run(cmd, check=True, env=env)
            print(f"✅ Departamento {dept} completado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al procesar {dept}. Saltando al siguiente.")
            continue
            
        current_id += 5
        time.sleep(2) # Pausa breve para no saturar Ollama/Supabase

    print("\n" + "="*60)
    print("🎉 EXPANSIÓN MASIVA FINALIZADA.")
    print("El siguiente paso es ejecutar 'python scripts/auto_inject_tours.py'")
    print("="*60)

if __name__ == "__main__":
    main()
