import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Crear bucket sin kwargs deprecados
try:
    supabase.storage.create_bucket("event_flyers", options={"public": True})
    print("[OK] Bucket 'event_flyers' creado exitosamente con acceso publico.")
except Exception as e:
    if "already exists" in str(e).lower() or "Duplicate" in str(e):
        print("[INFO] El bucket 'event_flyers' ya existe. Listo para usar.")
    else:
        print(f"[ERROR] {e}")
