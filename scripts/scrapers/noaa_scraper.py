"""
noaa_scraper.py - Extractor de datos de la NOAA (Súper Niño)
Uso: Extraer datos de la Anomalía de la Temperatura de la Superficie del Mar (SST)
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

# TODO: Obtener token en https://www.ncdc.noaa.gov/cdo-web/token y ponerlo aquí o en tu .env
NOAA_TOKEN = os.getenv("NOAA_TOKEN", "TU_TOKEN_NOAA_AQUI")

def update_climate_cache(data, alert_level):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[-] Credenciales de Supabase no configuradas.")
        return
        
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    payload = {
        "source_name": "NOAA",
        "metric_type": "SST_ANOMALY",
        "raw_value": data,
        "alert_level": alert_level,
        "location": "Niño 3.4",
        "last_updated": datetime.now().isoformat()
    }
    
    # Primero intentamos eliminar el registro anterior de NOAA para mantener la tabla limpia
    try:
        supabase.table("climate_cache").delete().eq("source_name", "NOAA").execute()
    except:
        pass
        
    # Insertar el nuevo
    try:
        supabase.table("climate_cache").insert(payload).execute()
        print("✅ NOAA: Datos guardados en Supabase (climate_cache).")
    except Exception as e:
        print(f"[-] NOAA: Error al guardar en Supabase: {e}")

def fetch_noaa_data():
    print("🌊 Iniciando conexión a la API de NOAA (Súper Niño)...")
    
    # Ejemplo genérico: Obtenemos datos de la base de datos de NOAA (CDO API).
    # Como el endpoint exacto del índice ENSO 3.4 cambia (muchas veces la gente descarga CSV desde NCEP),
    # usaremos una estructura base para conectarse a NOAA CDO API usando requests.
    
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets"
    headers = {
        "token": NOAA_TOKEN
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ NOAA: Conexión exitosa a la API.")
            
            # TODO: Una vez que tengas el token, cambiaremos el URL para apuntar
            # específicamente a los datos de boyas/satélite del Pacífico Ecuatorial (SST).
            
            # Por ahora simulamos la data procesada
            simulated_sst_anomaly = 1.2 # grados
            
            alert_level = "NORMAL"
            if simulated_sst_anomaly >= 0.5 and simulated_sst_anomaly < 1.5:
                alert_level = "EL NIÑO DÉBIL"
            elif simulated_sst_anomaly >= 1.5:
                alert_level = "SÚPER NIÑO (ALERTA ROJA)"
                
            update_climate_cache({"sst_anomaly_celsius": simulated_sst_anomaly}, alert_level)
        else:
            print(f"[-] NOAA: Error en la API (Código: {response.status_code}). ¿Pusiste el token válido?")
    except Exception as e:
        print(f"[-] NOAA: Error de conexión: {e}")

if __name__ == "__main__":
    fetch_noaa_data()
