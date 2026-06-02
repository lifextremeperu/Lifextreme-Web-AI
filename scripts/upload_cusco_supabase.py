import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
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

def generate_local_embeddings(texts):
    """Genera embeddings usando Ollama (nomic-embed-text) localmente."""
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
    print(" >>> INICIANDO MIGRACIÓN DE CUSCO A SUPABASE (OLLAMA LOCAL) ")
    print("===================================================================")
    
    supabase = init_supabase()
    jsonl_path = Path("data/cixtur_knowledge.jsonl")
    
    if not jsonl_path.exists():
        print(f"[-] Archivo no encontrado: {jsonl_path}")
        sys.exit(1)
        
    print("[+] Leyendo y formateando los datos de Cusco...")
    
    all_datapoints = []
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if not line.strip():
                continue
            
            data = json.loads(line)
            source = data.get("source", "GENERAL").strip()
            prompt = data.get("prompt", "").strip()
            completion = data.get("completion", "").strip()
            
            # Limpiar source para usarlo en el ID (sin espacios especiales ni mayusculas innecesarias)
            safe_source = source.replace(" ", "_").replace("/", "_").lower()
            vector_id = f"cusco_cixtur_{safe_source}_{idx}"
            
            text_content = f"Región: Cusco. Módulo: {source}. Pregunta: {prompt} Respuesta: {completion}"
            
            datapoint = {
                "vector_id": vector_id,
                "region": "cusco",
                "tier": 1,
                "modulo_nombre": source,
                "text_content": text_content,
            }
            all_datapoints.append(datapoint)
            
    print(f"[+] Total de registros de Cusco a vectorizar: {len(all_datapoints)}")
    
    if len(all_datapoints) == 0:
        print("[-] No hay datos para subir. Saliendo.")
        sys.exit(0)
        
    print("[+] Generando Embeddings (LOCAL OLLAMA) y subiendo a Supabase...")
    
    # Lotes de 50 para evitar OOM (Out Of Memory) en la PC del usuario
    BATCH_SIZE = 50
    total_batches = (len(all_datapoints) // BATCH_SIZE) + 1
    vectores_subidos = 0
    
    for i in range(0, len(all_datapoints), BATCH_SIZE):
        batch = all_datapoints[i:i+BATCH_SIZE]
        texts = [dp["text_content"] for dp in batch]
        
        print(f"    -> Lote {i//BATCH_SIZE + 1}/{total_batches} ({len(batch)} vectores)...")
        
        try:
            embeddings = generate_local_embeddings(texts)
            
            supabase_records = []
            for idx, emb in enumerate(embeddings):
                record = batch[idx]
                record["embedding"] = emb
                supabase_records.append(record)
                
            res = supabase.table("knowledge_vectors").upsert(supabase_records, on_conflict="vector_id").execute()
            
            vectores_subidos += len(supabase_records)
            
        except Exception as e:
            print(f"    [-] Error en el lote {i//BATCH_SIZE + 1}: {e}")
            time.sleep(2)
            
    print("===================================================================")
    print(f" ✅ MIGRACIÓN DE CUSCO COMPLETADA EXITOSAMENTE.")
    print(f" ✅ Total Vectores de Cusco Guardados en Supabase: {vectores_subidos}")
    print("===================================================================")

if __name__ == "__main__":
    main()
