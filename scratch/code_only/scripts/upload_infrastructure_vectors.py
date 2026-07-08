import os
import sys
import json
import time
import requests
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

def extract_infrastructure_data(json_path):
    datapoints = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for idx, item in enumerate(data):
            # Parsear datos
            region_name = item.get("ubicacion", {}).get("departamento", "Perú")
            nombre = item.get("nombre_oficial", "")
            cat = item.get("tipo_categoria", "")
            desc = item.get("descripcion_corta", "")
            operador = item.get("operador_responsable", "")
            
            # Formatear contenido textual para RAG
            text_content = f"Infraestructura de Aventura en {region_name}. Nombre: {nombre}. Categoría: {cat}. Operador: {operador}. Descripción: {desc}."
            vector_id = f"infra_{region_name.lower().replace(' ', '')}_{item.get('id_infraestructura', f'idx{idx}')}"
            
            datapoint = {
                "vector_id": vector_id,
                "region": region_name.lower(),
                "tier": 1, # Tier alto para infraestructura
                "modulo_nombre": "InfraestructuraAventura",
                "text_content": text_content,
            }
            datapoints.append(datapoint)
    except Exception as e:
        print(f"[-] Error leyendo {json_path}: {e}")
        
    return datapoints

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
    print(" >>> INICIANDO VECTORIZACIÓN DE INFRAESTRUCTURA (LOCAL OLLAMA) ")
    print("===================================================================")
    
    supabase = init_supabase()
    json_path = "data/knowledge/infraestructura_seed.json"
    
    print("[+] Leyendo infraestructura_seed.json...")
    datapoints = extract_infrastructure_data(json_path)
    print(f"[+] Total de registros a vectorizar: {len(datapoints)}")
    
    if len(datapoints) == 0:
        print("[-] No hay datos para subir. Saliendo.")
        sys.exit(0)
        
    print("[+] Generando Embeddings y subiendo a Supabase `knowledge_vectors`...")
    
    BATCH_SIZE = 50
    total_batches = (len(datapoints) // BATCH_SIZE) + 1
    vectores_subidos = 0
    
    for i in range(0, len(datapoints), BATCH_SIZE):
        batch = datapoints[i:i+BATCH_SIZE]
        texts = [dp["text_content"] for dp in batch]
        
        print(f"    -> Lote {i//BATCH_SIZE + 1}/{total_batches} ({len(batch)} vectores)...")
        
        try:
            # 1. Generar vectores matemáticos
            embeddings = generate_local_embeddings(texts)
            
            # 2. Preparar payload
            supabase_records = []
            for idx, emb in enumerate(embeddings):
                record = batch[idx]
                record["embedding"] = emb
                supabase_records.append(record)
                
            # 3. Insertar
            res = supabase.table("knowledge_vectors").upsert(supabase_records, on_conflict="vector_id").execute()
            vectores_subidos += len(supabase_records)
            
        except requests.exceptions.ConnectionError:
            print("    [-] ERROR: No se pudo conectar a Ollama en http://localhost:11434. Asegúrate de que Ollama esté corriendo (ollama run nomic-embed-text).")
            sys.exit(1)
        except Exception as e:
            print(f"    [-] Error en el lote {i//BATCH_SIZE + 1}: {e}")
            
    print("===================================================================")
    print(f" ✅ INGESTA DE VECTORES COMPLETADA.")
    print(f" ✅ Total Vectores Guardados: {vectores_subidos}")
    print("===================================================================")

if __name__ == "__main__":
    main()
