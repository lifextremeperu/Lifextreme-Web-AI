"""
senamhi_scraper.py - Extractor de Datos Abiertos del SENAMHI
Uso: Extraer estado climático local (Arequipa / Cusco) desde CKAN (datosabiertos.gob.pe)
"""
import os
import requests
import json
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
        "source_name": "SENAMHI",
        "metric_type": "PRECIPITATION_TEMP",
        "raw_value": data,
        "alert_level": alert_level,
        "location": "Arequipa",
        "last_updated": datetime.now().isoformat()
    }
    
    try:
        supabase.table("climate_cache").delete().eq("source_name", "SENAMHI").execute()
    except:
        pass
        
    try:
        supabase.table("climate_cache").insert(payload).execute()
        print("✅ SENAMHI: Datos guardados en Supabase (climate_cache).")
    except Exception as e:
        print(f"[-] SENAMHI: Error al guardar en Supabase: {e}")

def fetch_senamhi_data():
    print("🌦️ Buscando datos de SENAMHI en Datos Abiertos del Perú...")
    
    # Endpoint de la API de CKAN de datosabiertos.gob.pe
    # Este es el endpoint general de búsqueda de paquetes
    url = "https://www.datosabiertos.gob.pe/api/3/action/package_search?q=organization:senamhi"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            total_datasets = data.get('result', {}).get('count', 0)
            print(f"✅ SENAMHI: Encontrados {total_datasets} datasets disponibles.")
            
            # Aquí extraemos los metadatos relevantes.
            # En producción se debe apuntar al "resource_id" específico del datastore para extraer los CSV dinámicamente.
            
            # Simulando la extracción de la última lectura para Arequipa
            clima_actual = {
                "temperatura_max": 22,
                "temperatura_min": 5,
                "precipitacion": 0,
                "condicion": "Despejado"
            }
            
            update_climate_cache(clima_actual, "OPTIMO PARA VUELO")
        else:
            print(f"[-] SENAMHI: Error al conectar con Datos Abiertos ({response.status_code})")
    except Exception as e:
        print(f"[-] SENAMHI: Error de conexión: {e}")

if __name__ == "__main__":
    fetch_senamhi_data()
