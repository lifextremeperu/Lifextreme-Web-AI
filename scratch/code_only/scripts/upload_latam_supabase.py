import os
import sys
import json
import glob
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Supabase Client
from supabase import create_client, Client

def init_supabase():
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        print("[-] Faltan credenciales de Supabase en el .env")
        sys.exit(1)
    
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def get_latam_tourism_jsons():
    base_dir = Path("data/knowledge")
    target_countries = ["argentina", "bolivia", "chile", "colombia", "ecuador"]
    json_files = []
    
    if not base_dir.exists():
        print(f"[-] El directorio {base_dir} no existe.")
        return json_files
        
    for country in target_countries:
        country_dir = base_dir / country
        if country_dir.exists() and country_dir.is_dir():
            print(f"[+] Escaneando país: {country.upper()}")
            for region_dir in country_dir.iterdir():
                if region_dir.is_dir():
                    deep_dir = region_dir / "fqsas_deep"
                    if deep_dir.exists():
                        for json_file in glob.glob(str(deep_dir / "*.json")):
                            json_files.append((country, region_dir.name, json_file))
                            
    return json_files

def extract_fqsas_from_json(json_path, country_name, region_name):
    fqsas = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modulo_id = data.get("destino_id", data.get("modulo_id", "UNKNOWN"))
        modulo_nombre = data.get("modulo_contexto", data.get("modulo_nombre", ""))
        tier = data.get("_meta", {}).get("tier", 2)
        
        fqsas_dict = data.get("fqsas", {})
        
        for angle_name, qa_list in fqsas_dict.items():
            if isinstance(qa_list, list):
                for idx, fqsa in enumerate(qa_list):
                    q = fqsa.get('pregunta', fqsa.get('Q', ''))
                    a = fqsa.get('respuesta', fqsa.get('A', ''))
                    
                    text_content = f"País: {country_name.capitalize()}. Región: {region_name.capitalize()}. Módulo: {modulo_nombre}. Pregunta: {q} Respuesta: {a}"
                    vector_id = f"{country_name}_{region_name}_{modulo_id}_{angle_name}_{idx}"
                    
                    datapoint = {
                        "vector_id": vector_id,
                        "region": region_name.lower(), # Usamos region para mantener la compatibilidad con el esquema
                        "tier": int(tier) if str(tier).isdigit() else 2,
                        "modulo_nombre": f"{country_name.capitalize()} - {modulo_nombre}",
                        "text_content": text_content,
                    }
                    fqsas.append(datapoint)
    except Exception as e:
        print(f"[-] Error leyendo {json_path}: {e}")
        
    return fqsas

def generate_local_embeddings(texts):
    # Llama a Ollama localmente (nomic-embed-text)
    url = "http://localhost:11434/api/embed"
    payload = {
        "model": "nomic-embed-text",
        "input": texts
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get("embeddings", [])

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("===================================================================")
    print(" >>> INICIANDO EXPANSIÓN LATAM A SUPABASE (LOCAL OLLAMA) ")
    print("===================================================================")
    
    supabase = init_supabase()
    
    print("[+] Escaneando Módulos B2C (JSONs) de SUDAMÉRICA...")
    all_files = get_latam_tourism_jsons()
    print(f"[+] Se encontraron {len(all_files)} archivos JSON de destinos en LATAM.")
    
    print("[+] Extrayendo FQSAs (Conocimiento Atómico)...")
    all_datapoints = []
    for country, region, file_path in all_files:
        all_datapoints.extend(extract_fqsas_from_json(file_path, country, region))
        
    print(f"[+] Total de FQSAs a vectorizar para LATAM: {len(all_datapoints)}")
    
    if len(all_datapoints) == 0:
        print("[-] No hay datos para subir. Saliendo.")
        sys.exit(0)
        
    # Cortar los primeros 19900 vectores (Lotes 1 al 398 que ya subieron bien)
    print("[+] Saltando los primeros 19900 vectores ya procesados...")
    all_datapoints = all_datapoints[19900:]
    
    print("[+] Generando Embeddings (LOCAL OLLAMA) y subiendo a Supabase...")
    
    # Procesar de a 25 textos para evitar Timeout en Supabase
    BATCH_SIZE = 25
    total_batches = (len(all_datapoints) // BATCH_SIZE) + 1
    vectores_subidos = 0
    
    for i in range(0, len(all_datapoints), BATCH_SIZE):
        batch = all_datapoints[i:i+BATCH_SIZE]
        texts = [dp["text_content"] for dp in batch]
        
        print(f"    -> Lote {i//BATCH_SIZE + 1}/{total_batches} ({len(batch)} vectores)...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                embeddings = generate_local_embeddings(texts)
                
                supabase_records = []
                for idx, emb in enumerate(embeddings):
                    record = batch[idx]
                    record["embedding"] = emb
                    supabase_records.append(record)
                    
                res = supabase.table("knowledge_vectors").upsert(supabase_records, on_conflict="vector_id").execute()
                vectores_subidos += len(supabase_records)
                
                # Pausa para que Supabase respire
                time.sleep(1)
                break # Éxito, salir del loop de reintentos
                
            except Exception as e:
                print(f"    [-] Error en el lote {i//BATCH_SIZE + 1} (Intento {attempt+1}/{max_retries}): {e}")
                time.sleep(5) # Esperar más tiempo si falla antes de reintentar
            
    print("===================================================================")
    print(f" ✅ EXPANSIÓN LATAM COMPLETADA (USANDO OLLAMA LOCAL).")
    print(f" ✅ Total Vectores Guardados en Supabase: {vectores_subidos}")
    print("===================================================================")

if __name__ == "__main__":
    main()
