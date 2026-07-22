"""
perurail_scraper.py - Robot araña para perurail.com
Uso: Extraer disponibilidad y horarios de trenes a Machu Picchu Pueblo.
"""
import os
import asyncio
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def scrape_perurail_availability():
    print("🚂 Iniciando Robot Araña: PeruRail.com")
    
    # ---------------------------------------------------------
    # En producción: Usar Playwright o una API no documentada 
    # de PeruRail para consultar rutas (Ollantaytambo -> Mapi).
    # ---------------------------------------------------------
    
    print("⏳ Simulando extracción de cupos de trenes...")
    await asyncio.sleep(1.5)
    
    # MOCK DATA
    extracted_data = [
        {
            "destino": "tren_perurail_vistadome",
            "fecha_recorrido": datetime.now().strftime("%Y-%m-%d"),
            "cupos_disponibles": 12, # Quedan pocos
            "ultima_actualizacion": datetime.now().isoformat()
        },
        {
            "destino": "tren_perurail_expedition",
            "fecha_recorrido": datetime.now().strftime("%Y-%m-%d"),
            "cupos_disponibles": 0, # Agotado hoy
            "ultima_actualizacion": datetime.now().isoformat()
        }
    ]
    
    try:
        supabase.table("realtime_availability").upsert(
            extracted_data, 
            on_conflict="destino, fecha_recorrido"
        ).execute()
        print("✅ Caché de PeruRail actualizado exitosamente.")
    except Exception as e:
        print("[-] Error guardando en Supabase:", e)

if __name__ == "__main__":
    asyncio.run(scrape_perurail_availability())
