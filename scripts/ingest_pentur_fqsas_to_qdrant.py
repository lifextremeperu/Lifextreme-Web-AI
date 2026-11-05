import os
import sys
import glob
import json
import uuid
import urllib.request
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embeddings")
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "Lifextreme_FQSA_Knowledge"

def get_ollama_embedding(text: str) -> list[float]:
    req_data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res["embedding"]

def ingest_pentur_fqsas():
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    pentur_dirs = [
        ("peru", "amazonas", "data/knowledge/peru/amazonas/fqsas_deep/*.json"),
        ("peru", "huancavelica", "data/knowledge/peru/huancavelica/fqsas_deep/*.json"),
        ("peru", "huanuco", "data/knowledge/peru/huanuco/fqsas_deep/*.json"),
        ("peru", "junin", "data/knowledge/peru/jun\u00edn/fqsas_deep/*.json"),
        ("peru", "lalibertad", "data/knowledge/peru/lalibertad/fqsas_deep/*.json"),
        ("peru", "loreto", "data/knowledge/peru/loreto/fqsas_deep/*.json"),
        ("peru", "piura", "data/knowledge/peru/piura/fqsas_deep/*.json"),
    ]
    
    all_qa_points = []
    
    for pais, reg, pattern in pentur_dirs:
        files = glob.glob(pattern)
        for filepath in files:
            with open(filepath, "r", encoding="utf-8") as f:
                doc = json.load(f)
                
            destino_id = doc.get("destino_id", "")
            modulo_contexto = doc.get("modulo_contexto", "")
            source_file = os.path.basename(filepath)
            
            fqsas = doc.get("fqsas", {})
            for cat_name, qa_list in fqsas.items():
                for item in qa_list:
                    pregunta = item.get("pregunta", "")
                    respuesta = item.get("respuesta", "")
                    text_content = f"P: {pregunta}\nR: {respuesta}"
                    
                    all_qa_points.append({
                        "text_content": text_content,
                        "pregunta": pregunta,
                        "respuesta": respuesta,
                        "categoria": cat_name,
                        "destino_id": destino_id,
                        "modulo_contexto": modulo_contexto,
                        "pais": pais,
                        "region": reg,
                        "source": source_file,
                        "area": "fqsa",
                        "acceso": "compartido"
                    })

    total_pts = len(all_qa_points)
    print(f"📦 Total de preguntas/respuestas PENTUR normalizadas a indexar: {total_pts}")
    
    batch = []
    batch_size = 10
    
    for idx, item in enumerate(all_qa_points, 1):
        if idx % 20 == 0 or idx == total_pts:
            print(f"  [{idx:03d}/{total_pts:03d}] Vectorizando con {EMBEDDING_MODEL} (Región: {item['region']})...")
            
        emb = get_ollama_embedding(item["text_content"])
        
        pt = PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload=item
        )
        batch.append(pt)
        
        if len(batch) >= batch_size or idx == total_pts:
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
            batch = []

    print(f"\n🎉 ¡Ingestión PENTUR exitosa! {total_pts} puntos agregados a '{COLLECTION_NAME}'.")
    
    # Smoke test en PENTUR
    print("\n🔍 Ejecutando Smoke Test en PENTUR...")
    test_query = "como llegar a kuelap o gocta en la region amazonas"
    test_vec = get_ollama_embedding(test_query)
    
    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=test_vec,
        query_filter=Filter(
            must=[
                FieldCondition(key="pais", match=MatchValue(value="peru")),
                FieldCondition(key="region", match=MatchValue(value="amazonas"))
            ]
        ),
        limit=2
    ).points
    
    for h in hits:
        print(f"  Top Match [Score: {h.score:.4f}]: {h.payload.get('modulo_contexto')}")
        print(f"    P: {h.payload.get('pregunta')}")

if __name__ == "__main__":
    ingest_pentur_fqsas()
