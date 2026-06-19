import os
import time
import json
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# =====================================================================
# SCRIPT DE RE-VECTORIZACIÓN (NOMIC-EMBED-TEXT)
# Diseñado para no calentar la CPU de 8GB RAM y guardar progreso.
# =====================================================================

# Configuración Inicial
load_dotenv('.env')
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"
BATCH_SIZE = 10
COOL_DOWN_SECONDS = 2.5 # Pausa de 2.5 seg por lote para no calentar la PC
CHECKPOINT_FILE = "data/revectorize_checkpoint.json"
MAX_RECORDS_PER_RUN = 40000 # Límite diario/por ejecución para no saturar Supabase ni la PC

def get_nomic_embedding(text: str) -> list:
    """Obtiene el vector usando la API HTTP local de Ollama (muy rápida y ligera)"""
    payload = {
        "model": MODEL_NAME,
        "prompt": text
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("embedding", [])
    else:
        print(f"Error Ollama: {response.text}")
        return []

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_index", 0)
    return 0

def save_checkpoint(index):
    # Asegurar que existe la carpeta
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_index": index}, f)

def main():
    print("=====================================================")
    print(" INICIANDO MIGRACIÓN A VECTORES LIGEROS (NOMIC)")
    print("=====================================================")
    
    # Obtener el total de registros para saber cuánto falta
    # (Evitamos count='exact' porque tarda más de 1 minuto en la tabla pesada de 32k)
    total_records = 32149
    print(f" Total de registros a procesar: aprox {total_records}")

    current_index = load_checkpoint()
    print(f" Reanudando desde el registro: {current_index}")
    print(f" Límite configurado para esta sesión: {MAX_RECORDS_PER_RUN} registros.")
    print("=====================================================")

    records_processed_this_run = 0

    while current_index < total_records and records_processed_this_run < MAX_RECORDS_PER_RUN:
        start_idx = current_index
        end_idx = current_index + BATCH_SIZE - 1

        print(f"\n[+] Descargando Lote: {start_idx} al {end_idx}...")
        
        # 1. Extraer lote pesado
        res = supabase.table('knowledge_chunks').select('*').range(start_idx, end_idx).execute()
        chunks = res.data

        if not chunks:
            print("No se encontraron más registros. Finalizando.")
            break

        new_vectors_batch = []
        
        # 2. Re-vectorizar cada chunk con el modelo ligero
        print(f"    -> Transformando {len(chunks)} textos a matemática de 768 dimensiones...")
        
        for idx, chunk in enumerate(chunks, 1):
            text = chunk.get('content', '')
            if not text.strip():
                continue
                
            metadata = chunk.get('metadata', {})
            
            # Print para calmar la ansiedad del usuario
            print(f"       [{idx}/{len(chunks)}] Generando vector para ID {chunk['id'][:8]}...", end=" ", flush=True)
            
            vector = get_nomic_embedding(text)
            
            if not vector:
                print("❌ ERROR")
                continue
                
            print("✅ OK")

            # Parseo seguro del nivel de importancia (tier) a entero
            raw_tier = metadata.get('categoria_turistica', 3)
            try:
                tier_val = int(raw_tier)
            except (ValueError, TypeError):
                tier_val = 3 # Nivel 3 (General) por defecto si es texto como "desconocido"

            # Mapeo a la nueva tabla knowledge_vectors
            new_row = {
                "vector_id": chunk['id'], # ID original como referencia
                "region": metadata.get('region', 'desconocido').lower(),
                "tier": tier_val,
                "modulo_nombre": metadata.get('archivo_origen', 'Migracion Nomic'),
                "text_content": text,
                "embedding": vector
            }
            new_vectors_batch.append(new_row)

        # 3. Subir el nuevo lote ligero a Supabase (Con reintentos antibloqueo)
        if new_vectors_batch:
            print(f"    -> Subiendo {len(new_vectors_batch)} vectores ligeros a Supabase...")
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    supabase.table('knowledge_vectors').upsert(new_vectors_batch, on_conflict='vector_id').execute()
                    break # Éxito, salimos del reintento
                except Exception as e:
                    print(f"    [AVISO] Intento {attempt + 1} falló: {str(e)}")
                    if attempt == max_retries - 1:
                        print("    [ERROR FATAL] No se pudo subir a Supabase tras varios intentos.")
                        return # Abortar función
                    time.sleep(5) # Esperar antes de reintentar

        # 4. Guardar progreso y enfriar
        current_index += len(chunks)
        records_processed_this_run += len(chunks)
        save_checkpoint(current_index)
        
        porcentaje = (current_index / total_records) * 100
        print(f"[OK] Lote completado. Progreso Global: {porcentaje:.2f}% ({current_index}/{total_records})")
        
        print(f"⏳ Pausa térmica de {COOL_DOWN_SECONDS} segundos para no estresar tu CPU...")
        time.sleep(COOL_DOWN_SECONDS)

    print("\n=====================================================")
    if records_processed_this_run >= MAX_RECORDS_PER_RUN:
        print(f" 🛑 META DIARIA ALCANZADA ({MAX_RECORDS_PER_RUN} registros). PROGRAMADO PARA DETENERSE.")
    else:
        print(" 🎉 PROCESO COMPLETADO O DETENIDO CORRECTAMENTE 🎉")
    print("=====================================================")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Detenido por el usuario. El progreso ha sido guardado.")
        print("Puedes volver a ejecutar este script y continuará exactamente donde se quedó.")
