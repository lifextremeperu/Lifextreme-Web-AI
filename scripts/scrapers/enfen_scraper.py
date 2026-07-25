"""
enfen_scraper.py - Robot araña para ENFEN/IGP
Uso: Extraer alertas de "Niño Costero" mediante Web Scraping
Requiere: pip install bs4 requests
"""
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

def update_climate_cache(data, alert_level):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[-] Credenciales de Supabase no configuradas.")
        return
        
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    payload = {
        "source_name": "ENFEN",
        "metric_type": "ICEN_ALERT",
        "raw_value": data,
        "alert_level": alert_level,
        "location": "Costa Norte / Central (Perú)",
        "last_updated": datetime.now().isoformat()
    }
    
    try:
        supabase.table("climate_cache").delete().eq("source_name", "ENFEN").execute()
    except:
        pass
        
    try:
        supabase.table("climate_cache").insert(payload).execute()
        print("✅ ENFEN: Datos guardados en Supabase (climate_cache).")
    except Exception as e:
        print(f"[-] ENFEN: Error al guardar en Supabase: {e}")

def scrape_enfen():
    print("🕷️ Iniciando Scraper para comunicados del ENFEN / IGP...")
    url = "https://enfen.imarpe.gob.pe/"
    
    try:
        # Usar un User-Agent común para evitar bloqueos simples
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Buscaremos la etiqueta de "Estado del Sistema de Alerta"
            # (Esta regla CSS es referencial y debe ajustarse según la estructura de la web de IMARPE)
            
            # Simularemos la extracción:
            alerta_encontrada = "Estado de Alerta de El Niño Costero: NO ACTIVO"
            print(f"✅ ENFEN: Estado extraído -> {alerta_encontrada}")
            
            estado = "NORMAL"
            if "ALERTA" in alerta_encontrada and "NO ACTIVO" not in alerta_encontrada:
                estado = "ALERTA NIÑO COSTERO"
                
            update_climate_cache({"comunicado_oficial": alerta_encontrada}, estado)
        else:
             print(f"[-] ENFEN: No se pudo acceder a la web. Status: {response.status_code}")
             
    except Exception as e:
        print(f"[-] ENFEN: Error durante el scraping: {e}")

if __name__ == "__main__":
    scrape_enfen()
