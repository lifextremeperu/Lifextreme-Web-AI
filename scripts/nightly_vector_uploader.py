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
    
    # Init Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        print("[-] Faltan credenciales de Supabase en el .env")
        sys.exit(1)
    
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase

def get_peru_tourism_jsons():
    base_dir = Path("data/knowledge/peru")
    json_files = []
    
    if not base_dir.exists():
        print(f"[-] El directorio {base_dir} no existe.")
        return json_files
        
    for region_dir in base_dir.iterdir():
        if region_dir.is_dir():
            deep_dir = region_dir / "fqsas_deep"
            if deep_dir.exists():
                for json_file in glob.glob(str(deep_dir / "*.json")):
                    json_files.append((region_dir.name, json_file))
                    
    return json_files

def extract_fqsas_from_json(json_path, region_name):
    fqsas = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modulo_id = data.get("destino_id", data.get("modulo_id", "UNKNOWN"))
        modulo_nombre = data.get("modulo_contexto", data.get("modulo_nombre", ""))
        tier = data.get("_meta", {}).get("tier", 3)
        
        fqsas_dict = data.get("fqsas", {})
        
        for angle_name, qa_list in fqsas_dict.items():
            if isinstance(qa_list, list):
                for idx, fqsa in enumerate(qa_list):
                    q = fqsa.get('pregunta', fqsa.get('Q', ''))
                    a = fqsa.get('respuesta', fqsa.get('A', ''))
                    
                    text_content = f"Región: {region_name.capitalize()}. Módulo: {modulo_nombre}. Pregunta: {q} Respuesta: {a}"
                    vector_id = f"{region_name}_{modulo_id}_{angle_name}_{idx}"
                    
                    datapoint = {
                        "vector_id": vector_id,
                        "region": region_name.lower(),
                        "tier": int(tier) if str(tier).isdigit() else 3,
                        "modulo_nombre": modulo_nombre,
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
    print(" >>> INICIANDO MOTOR DE INGESTA A SUPABASE (LOCAL OLLAMA + PERÚ) ")
    print("===================================================================")
    
    supabase = init_supabase()
    
    print("[+] Escaneando Módulos B2C (JSONs) de PERÚ...")
    all_files = get_peru_tourism_jsons()
    print(f"[+] Se encontraron {len(all_files)} archivos JSON.")
    
    print("[+] Extrayendo FQSAs (Conocimiento Atómico)...")
    all_datapoints = []
    for region, file_path in all_files:
        all_datapoints.extend(extract_fqsas_from_json(file_path, region))
        
    print(f"[+] Total de FQSAs a vectorizar para Perú: {len(all_datapoints)}")
    
    if len(all_datapoints) == 0:
        print("[-] No hay datos para subir. Saliendo.")
        sys.exit(0)
        
    print("[+] Generando Embeddings (LOCAL OLLAMA) y subiendo a Supabase...")
    
    # Procesar de a 50 textos para no saturar la memoria RAM local
    BATCH_SIZE = 50
    total_batches = (len(all_datapoints) // BATCH_SIZE) + 1
    vectores_subidos = 0
    
    for i in range(0, len(all_datapoints), BATCH_SIZE):
        batch = all_datapoints[i:i+BATCH_SIZE]
        texts = [dp["text_content"] for dp in batch]
        
        print(f"    -> Lote {i//BATCH_SIZE + 1}/{total_batches} ({len(batch)} vectores)...")
        
        try:
            # 1. Generar vectores matemáticos (Ollama local)
            embeddings = generate_local_embeddings(texts)
            
            # 2. Preparar payload para Supabase
            supabase_records = []
            for idx, emb in enumerate(embeddings):
                record = batch[idx]
                record["embedding"] = emb
                supabase_records.append(record)
                
            # 3. Insertar en Supabase
            res = supabase.table("knowledge_vectors").upsert(supabase_records, on_conflict="vector_id").execute()
            
            vectores_subidos += len(supabase_records)
            
        except Exception as e:
            print(f"    [-] Error en el lote {i//BATCH_SIZE + 1}: {e}")
            time.sleep(2)
            
    print("===================================================================")
    print(f" ✅ INGESTA A SUPABASE COMPLETADA (USANDO OLLAMA LOCAL).")
    print(f" ✅ Total Vectores Guardados en Supabase: {vectores_subidos}")
    print("===================================================================")

if __name__ == "__main__":
    main()
