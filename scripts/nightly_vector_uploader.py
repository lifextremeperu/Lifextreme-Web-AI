import os
import sys
import json
import glob
import time
from pathlib import Path
from dotenv import load_dotenv

# SDK Nativo de Google GenAI (Usa REST/HTTPS por defecto, evita el gRPC Firewall 503)
from google import genai
from google.genai.types import HttpOptions

def init_gcp():
    load_dotenv()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "lifextreme-arequipa-agent")
    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    index_endpoint_id = os.getenv("VECTOR_SEARCH_ENDPOINT_ID")
    
    if not project_id or not index_endpoint_id:
        print("[-] Faltan credenciales de Google Cloud en el .env")
        sys.exit(1)
        
    os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
    os.environ['GOOGLE_CLOUD_LOCATION'] = location
    os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'
    
    try:
        client = genai.Client(http_options=HttpOptions(api_version='v1'))
        return client, index_endpoint_id
    except Exception as e:
        print(f"[-] Error fatal de conexión con Vertex AI Nativo: {e}")
        sys.exit(1)

def get_all_tourism_jsons():
    base_dir = Path("data/knowledge")
    json_files = []
    
    # Buscar en todas las regiones (arequipa, puno, ancash, cusco, etc)
    for region_dir in base_dir.iterdir():
        if region_dir.is_dir():
            deep_dir = region_dir / "fqsas_deep"
            if deep_dir.exists():
                for json_file in glob.glob(str(deep_dir / "*.json")):
                    json_files.append((region_dir.name, json_file))
                    
    return json_files

def extract_fqsas_from_json(json_path, region_name):
    # Lee el LifextremeSchema y extrae las preguntas y respuestas
    fqsas = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        modulo_id = data.get("destino_id", data.get("modulo_id", "UNKNOWN"))
        modulo_nombre = data.get("modulo_contexto", data.get("modulo_nombre", ""))
        
        fqsas_dict = data.get("fqsas", {})
        
        # Iterar sobre los 10 ángulos
        for angle_name, qa_list in fqsas_dict.items():
            if isinstance(qa_list, list):
                for idx, fqsa in enumerate(qa_list):
                    q = fqsa.get('pregunta', fqsa.get('Q', ''))
                    a = fqsa.get('respuesta', fqsa.get('A', ''))
                    
                    # Concatenar Pregunta + Respuesta para el embedding
                    text_content = f"Región: {region_name.capitalize()}. Módulo: {modulo_nombre}. Pregunta: {q} Respuesta: {a}"
                    
                    vector_id = f"{region_name}_{modulo_id}_{angle_name}_{idx}"
                    
                    # Estructura requerida por Vertex Vector Search
                    datapoint = {
                        "datapoint_id": vector_id,
                        "text": text_content, # Lo usamos solo para generar el vector
                        "restricts": [
                            {"namespace": "region", "allow": [region_name.lower()]},
                            {"namespace": "tier", "allow": [str(data.get("_meta", {}).get("tier", "3"))]}
                        ]
                    }
                    fqsas.append(datapoint)
    except Exception as e:
        print(f"[-] Error leyendo {json_path}: {e}")
        
    return fqsas

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("===================================================================")
    print(" >>> INICIANDO MOTOR DE INGESTA NOCTURNA (NIGHTLY VECTOR UPLOADER) ")
    print("===================================================================")
    
    client, index_endpoint_id = init_gcp()
    
    print("[+] Escaneando el Disco Duro Local en busca de Módulos B2C (JSONs)...")
    all_files = get_all_tourism_jsons()
    print(f"[+] Se encontraron {len(all_files)} archivos JSON maestros.")
    
    print("[+] Extrayendo FQSAs (Conocimiento Atómico)...")
    all_datapoints = []
    for region, file_path in all_files:
        all_datapoints.extend(extract_fqsas_from_json(file_path, region))
        
    print(f"[+] Extracción completa. Total de FQSAs a vectorizar: {len(all_datapoints)}")
    
    if len(all_datapoints) == 0:
        print("[-] No hay datos para subir. Saliendo.")
        sys.exit(0)
        
    print("[+] Cargando Modelo de Embeddings (text-embedding-004)...")
    
    # Procesar en Lotes de 100 para no romper la cuota de la API
    BATCH_SIZE = 100
    total_batches = (len(all_datapoints) // BATCH_SIZE) + 1
    
    print(f"\n[>>>] GENERANDO EMBEDDINGS VIA REST (Total lotes: {total_batches})")
    
    # Crear archivo maestro local
    backup_file = open("data/knowledge/master_vectors_to_upload.jsonl", "w", encoding="utf-8")
    
    vectores_subidos = 0
    for i in range(0, len(all_datapoints), BATCH_SIZE):
        batch = all_datapoints[i:i+BATCH_SIZE]
        texts = [dp["text"] for dp in batch]
        
        print(f"    -> Procesando Lote {i//BATCH_SIZE + 1}/{total_batches} ({len(batch)} vectores)...")
        
        try:
            # 1. Generar vectores matemáticos (Embeddings)
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=texts
            )
            
            for idx, embedding in enumerate(response.embeddings):
                # Guardar backup local en formato Vertex AI Batch
                backup_record = {
                    "id": batch[idx]["datapoint_id"],
                    "embedding": embedding.values,
                    "restricts": batch[idx]["restricts"]
                }
                backup_file.write(json.dumps(backup_record) + "\n")
                
            vectores_subidos += len(response.embeddings)
            time.sleep(2) # Pausa anti-saturación de Google Cloud
            
        except Exception as e:
            print(f"    [-] Error en el lote {i//BATCH_SIZE + 1}: {e}")
            time.sleep(10) # Enfriamiento si hay error
            
    backup_file.close()
    
    print("===================================================================")
    print(f" ✅ INGESTA NOCTURNA COMPLETADA (Generación de JSONL Master).")
    print(f" ✅ Total Vectores Guardados listos para Vertex AI: {vectores_subidos}")
    print("===================================================================")

if __name__ == "__main__":
    main()

