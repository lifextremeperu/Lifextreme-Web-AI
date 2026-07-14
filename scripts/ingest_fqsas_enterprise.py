import sys
import os
import csv
import json
import uuid
import time
import hashlib
import argparse
from pathlib import Path
import httpx
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

sys.stdout.reconfigure(encoding='utf-8')

# Constantes de los servicios locales
QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
OLLAMA_MODEL = "nomic-embed-text"
COLLECTION = "Lifextreme_Knowledge"
BATCH_SIZE = 100

def init_qdrant():
    qclient = QdrantClient(url=QDRANT_URL)
    if not qclient.collection_exists(collection_name=COLLECTION):
        print(f"[*] Creando colección {COLLECTION} en Qdrant...")
        qclient.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    return qclient

def get_embeddings_batch(texts):
    try:
        response = httpx.post(OLLAMA_EMBED_URL, json={
            "model": OLLAMA_MODEL,
            "input": texts
        }, timeout=120.0)
        
        if response.status_code == 200:
            data = response.json()
            # api/embed returns "embeddings" array
            return data.get("embeddings", [])
        else:
            print(f"[-] Error de Ollama: {response.text}")
            return []
    except Exception as e:
        print(f"[-] Error de conexión con Ollama: {e}")
        return []

def generate_stable_id(text):
    hash_obj = hashlib.md5(text.encode('utf-8'))
    return str(uuid.UUID(hash_obj.hexdigest()))

def upload_to_qdrant(qclient, points_batch):
    if not points_batch: return
    try:
        qclient.upsert(
            collection_name=COLLECTION,
            points=points_batch
        )
        print(f"    [+] Subidos {len(points_batch)} vectores únicos.")
    except Exception as e:
        print(f"    [-] Error subiendo batch: {e}")

def process_batch(qclient, current_batch):
    if not current_batch: return
    
    texts_to_embed = [item["text"] for item in current_batch]
    embeddings = get_embeddings_batch(texts_to_embed)
    
    if len(embeddings) == len(texts_to_embed):
        points = []
        for i, item in enumerate(current_batch):
            points.append(
                PointStruct(
                    id=item["id"],
                    vector=embeddings[i],
                    payload=item["payload"]
                )
            )
        upload_to_qdrant(qclient, points)
        time.sleep(0.5) # Pausa térmica
    else:
        print("    [-] El tamaño de embeddings no coincide con el batch.")

def run_ingestion():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    args = parser.parse_args()
    
    batch_limit = args.batch_size
    qclient = init_qdrant()
    current_batch = []
    total_injected = 0
    
    print("=========================================================")
    print(" 🚀 INYECTOR MAESTRO DE FQSAS (ENTERPRISE SEMANTIC BUNDLING) ")
    print("=========================================================")
    
    # 1. Procesar CSV de Cusco
    csv_path = "tours_faq.csv"
    if os.path.exists(csv_path):
        print(f"\n[*] Procesando CSV FQSA: {csv_path} (Cusco)...")
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        pregunta = row[0].strip()
                        respuesta = row[1].strip()
                        if not pregunta or not respuesta or pregunta.lower() == "pregunta":
                            continue
                        
                        text_content = f"PREGUNTA: {pregunta} \nRESPUESTA: {respuesta}"
                        stable_id = generate_stable_id(text_content)
                        
                        payload = {
                            "text_content": text_content,
                            "agencia_id": "lifextreme",
                            "tier": "tier_0",
                            "pais": "peru",
                            "departamento": "cusco",
                            "angulo_turistico": "0_Operativa_CSV",
                            "source": "tours_faq.csv"
                        }
                        
                        current_batch.append({"id": stable_id, "text": text_content, "payload": payload})
                        
                        if len(current_batch) >= batch_limit:
                            process_batch(qclient, current_batch)
                            total_injected += len(current_batch)
                            current_batch = []
            
            # Flush final del CSV
            if current_batch:
                process_batch(qclient, current_batch)
                total_injected += len(current_batch)
                current_batch = []
                
        except Exception as e:
            print(f"[-] Error leyendo {csv_path}: {e}")
    else:
        print("[-] No se encontró tours_faq.csv")
        
    # 2. Procesar Estructura Profunda (JSONs Minería)
    base_knowledge = Path("data/knowledge")
    print(f"\n[*] Recorriendo estructura de minería profunda: {base_knowledge}")
    
    countries = ["argentina", "bolivia", "chile", "colombia", "ecuador", "peru"]
    for country in countries:
        country_dir = base_knowledge / country
        if not country_dir.is_dir(): continue
        
        for dept_dir in country_dir.iterdir():
            if not dept_dir.is_dir(): continue
            departamento = dept_dir.name
            
            fqsas_deep_dir = dept_dir / "fqsas_deep"
            if not fqsas_deep_dir.is_dir(): continue
            
            print(f"    -> Procesando {country.upper()} / {departamento.upper()} ...")
            
            for json_file in fqsas_deep_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8', errors='replace') as f:
                        data = json.load(f)
                        fqsas_dict = data.get("fqsas", {})
                        
                        for angulo, preguntas in fqsas_dict.items():
                            if not isinstance(preguntas, list): continue
                            
                            for p in preguntas:
                                preg = str(p.get("pregunta", "")).strip()
                                resp = str(p.get("respuesta", "")).strip()
                                
                                if preg == "ERROR" or not preg or not resp:
                                    continue
                                
                                text_content = f"PREGUNTA: {preg} \nRESPUESTA: {resp}"
                                stable_id = generate_stable_id(text_content)
                                
                                payload = {
                                    "text_content": text_content,
                                    "agencia_id": "lifextreme",
                                    "tier": "tier_0",
                                    "pais": country,
                                    "departamento": departamento,
                                    "angulo_turistico": angulo,
                                    "source": json_file.name
                                }
                                
                                current_batch.append({"id": stable_id, "text": text_content, "payload": payload})
                                
                                if len(current_batch) >= batch_limit:
                                    process_batch(qclient, current_batch)
                                    total_injected += len(current_batch)
                                    current_batch = []
                except Exception as e:
                    pass
                    
    if current_batch:
        process_batch(qclient, current_batch)
        total_injected += len(current_batch)
        
    print(f"\n=========================================================")
    print(f" 🎉 ¡INYECCIÓN FINALIZADA! Total inyectados hoy: {total_injected}")
    print("=========================================================")

if __name__ == "__main__":
    run_ingestion()
