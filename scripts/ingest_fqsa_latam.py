"""
INGESTA MASIVA FQSA → Lifextreme_FQSA_Knowledge
Procesa 702 archivos JSON | ~66,357 Q&A pairs | Peru + LATAM
"""
import json, os, sys, time, uuid, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

QDRANT = 'http://localhost:6333'
OLLAMA = 'http://localhost:11434'
COLLECTION = 'Lifextreme_FQSA_Knowledge'
BATCH_SIZE = 50
BASE_PATH = r'data\knowledge'

def embed(texto):
    payload = json.dumps({"model": "nomic-embed-text", "prompt": texto}).encode()
    req = urllib.request.Request(
        f'{OLLAMA}/api/embeddings', data=payload,
        headers={'Content-Type': 'application/json'}, method='POST'
    )
    r = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return r['embedding']

def upsert_batch(points):
    payload = json.dumps({"points": points}).encode()
    req = urllib.request.Request(
        f'{QDRANT}/collections/{COLLECTION}/points',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    urllib.request.urlopen(req, timeout=30)

# ── Recolectar todos los archivos FQSA
all_files = []
for pais in sorted(os.listdir(BASE_PATH)):
    pais_path = os.path.join(BASE_PATH, pais)
    if not os.path.isdir(pais_path):
        continue
    for root, dirs, files in os.walk(pais_path):
        if 'fqsa' not in root.lower():
            continue
        region = root.split(os.sep)[-2] if 'fqsa' in root.split(os.sep)[-1].lower() else root.split(os.sep)[-1]
        for fn in files:
            if fn.endswith('.json'):
                all_files.append({
                    'path': os.path.join(root, fn),
                    'pais': pais,
                    'region': region,
                    'filename': fn
                })

print(f"Archivos FQSA encontrados: {len(all_files)}")
print(f"Coleccion destino: {COLLECTION}")
print(f"Batch size: {BATCH_SIZE}")
print("=" * 60)

total_vectors = 0
total_errors = 0
batch = []
start_time = time.time()

for file_idx, file_info in enumerate(all_files):
    try:
        with open(file_info['path'], encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ERROR leyendo {file_info['filename']}: {e}")
        total_errors += 1
        continue

    if not isinstance(data, dict):
        continue

    destino_id = data.get('destino_id', file_info['filename'].replace('.json',''))
    modulo_ctx = data.get('modulo_contexto', '')
    fqsas_dict = data.get('fqsas', {})

    for categoria, qa_list in fqsas_dict.items():
        if not isinstance(qa_list, list):
            continue
        for qa in qa_list:
            if not isinstance(qa, dict):
                continue
            pregunta = qa.get('pregunta', '').strip()
            respuesta = qa.get('respuesta', '')
            if isinstance(respuesta, list):
                respuesta = ' '.join(str(r) for r in respuesta)
            respuesta = str(respuesta).strip()

            if not pregunta or not respuesta:
                continue

            # Texto combinado para embedding
            texto = f"P: {pregunta}\nR: {respuesta}"

            try:
                vector = embed(texto)
            except Exception as e:
                total_errors += 1
                continue

            point = {
                'id': str(uuid.uuid4()),
                'vector': vector,
                'payload': {
                    'text_content': texto,
                    'pregunta': pregunta,
                    'respuesta': respuesta[:1000],
                    'categoria': categoria,
                    'destino_id': destino_id,
                    'modulo_contexto': modulo_ctx[:200],
                    'pais': file_info['pais'],
                    'region': file_info['region'],
                    'source': file_info['filename'],
                    'area': 'fqsa',
                    'acceso': 'compartido'
                }
            }
            batch.append(point)
            total_vectors += 1

            if len(batch) >= BATCH_SIZE:
                try:
                    upsert_batch(batch)
                    batch = []
                except Exception as e:
                    print(f"  ERROR upsert: {e}")
                    total_errors += 1
                    batch = []

    # Progreso cada 20 archivos
    if (file_idx + 1) % 20 == 0:
        elapsed = time.time() - start_time
        rate = total_vectors / elapsed if elapsed > 0 else 0
        remaining = len(all_files) - file_idx - 1
        eta_files = remaining / max((file_idx+1)/elapsed, 0.01)
        print(f"[{file_idx+1:>4}/{len(all_files)}] Vectores: {total_vectors:>6,} | "
              f"Errores: {total_errors} | Rate: {rate:.1f} vec/s | "
              f"ETA: {eta_files/60:.1f} min")

# Flush batch final
if batch:
    try:
        upsert_batch(batch)
    except Exception as e:
        print(f"ERROR flush final: {e}")

elapsed = time.time() - start_time
print()
print("=" * 60)
print(f"INGESTA COMPLETADA")
print(f"  Vectores ingresados: {total_vectors:,}")
print(f"  Errores:             {total_errors}")
print(f"  Tiempo total:        {elapsed/60:.1f} minutos")
print(f"  Velocidad promedio:  {total_vectors/elapsed:.1f} vec/seg")
print("=" * 60)
