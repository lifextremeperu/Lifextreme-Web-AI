import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Cargar Variables de Entorno
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[-] ERROR: Faltan credenciales de Supabase en el archivo .env")
    exit(1)

# 2. Inicializar Cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_seed_data():
    json_path = "data/knowledge/infraestructura_seed.json"
    
    print("==================================================")
    print(" INICIANDO INGESTA DE INFRAESTRUCTURA A SUPABASE")
    print("==================================================")
    
    if not os.path.exists(json_path):
        print(f"[-] ERROR: No se encontró el archivo {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"[>] Se encontraron {len(data)} registros para inyectar.")
    
    # Inyectar uno por uno o en batch
    exitos = 0
    errores = 0
    
    for item in data:
        try:
            # Usar upsert para evitar duplicados si se corre varias veces (basado en id_infraestructura que es unique)
            response = supabase.table("infrastructure").upsert(
                item, 
                on_conflict="id_infraestructura"
            ).execute()
            
            print(f"    [+] OK: {item['id_infraestructura']} - {item['nombre_oficial']}")
            exitos += 1
        except Exception as e:
            print(f"    [-] ERROR en {item['id_infraestructura']}: {e}")
            errores += 1
            
    print("\n==================================================")
    print(f" RESUMEN DE INGESTA")
    print(f" - Éxitos: {exitos}")
    print(f" - Errores: {errores}")
    print("==================================================")

if __name__ == "__main__":
    upload_seed_data()
