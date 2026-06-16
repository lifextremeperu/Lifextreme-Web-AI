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
BATCH_SIZE = 50
COOL_DOWN_SECONDS = 2.5 # Pausa de 2.5 seg por lote para no calentar la PC
CHECKPOINT_FILE = "data/revectorize_checkpoint.json"

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
    res_count = supabase.table('knowledge_chunks').select('id', count='exact').execute()
    total_records = res_count.count
    print(f" Total de registros a procesar: {total_records}")

    current_index = load_checkpoint()
    print(f" Reanudando desde el registro: {current_index}")
    print("=====================================================")

    while current_index < total_records:
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
        for chunk in chunks:
            text = chunk.get('content', '')
            if not text.strip():
                continue
                
            metadata = chunk.get('metadata', {})
            vector = get_nomic_embedding(text)
            
            if not vector:
                print(f"    [!] Error al vectorizar ID {chunk['id']}. Saltando.")
                continue

            # Mapeo a la nueva tabla knowledge_vectors
            new_row = {
                "vector_id": chunk['id'], # ID original como referencia
                "region": metadata.get('region', 'desconocido').lower(),
                "tier": metadata.get('categoria_turistica', 'desconocido'),
                "modulo_nombre": metadata.get('archivo_origen', 'Migracion Nomic'),
                "text_content": text,
                "embedding": vector
            }
            new_vectors_batch.append(new_row)

        # 3. Subir el nuevo lote ligero a Supabase
        if new_vectors_batch:
            print(f"    -> Subiendo {len(new_vectors_batch)} vectores ligeros a Supabase...")
            try:
                # Usamos upsert por si el script se repite
                supabase.table('knowledge_vectors').upsert(new_vectors_batch).execute()
            except Exception as e:
                print(f"    [ERROR FATAL] Al subir a Supabase: {str(e)}")
                # Si falla la subida, detenemos para no perder el tracking
                break

        # 4. Guardar progreso y enfriar
        current_index += len(chunks)
        save_checkpoint(current_index)
        
        porcentaje = (current_index / total_records) * 100
        print(f"[OK] Lote completado. Progreso Global: {porcentaje:.2f}% ({current_index}/{total_records})")
        
        print(f"⏳ Pausa térmica de {COOL_DOWN_SECONDS} segundos para no estresar tu CPU...")
        time.sleep(COOL_DOWN_SECONDS)

    print("\n=====================================================")
    print(" 🎉 PROCESO COMPLETADO O DETENIDO CORRECTAMENTE 🎉")
    print("=====================================================")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Detenido por el usuario. El progreso ha sido guardado.")
        print("Puedes volver a ejecutar este script y continuará exactamente donde se quedó.")
