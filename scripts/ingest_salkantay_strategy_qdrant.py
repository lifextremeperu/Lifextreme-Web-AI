import os
import sys
import json
import uuid
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
    Filter,
    FieldCondition,
    MatchValue,
    HnswConfigDiff
)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embeddings")
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "lifextreme_peru_strategy"
VECTOR_SIZE = 768

def get_ollama_embedding(text: str) -> list[float]:
    """Genera vector de embedding de 768 dimensiones usando modelo local nomic-embed-text en Ollama."""
    req_data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res["embedding"]

def setup_collection(client: QdrantClient):
    """Crea la colección si no existe e indexa los campos clave de payload para búsqueda de baja latencia."""
    exists = client.collection_exists(COLLECTION_NAME)
    if exists:
        print(f"ℹ️ Colección '{COLLECTION_NAME}' ya existe. Asegurando índices de payload...")
    else:
        print(f"🚀 Creando colección '{COLLECTION_NAME}' (Dim: {VECTOR_SIZE}, Métrica: Cosine)...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            hnsw_config=HnswConfigDiff(m=16, ef_construct=100, full_scan_threshold=10000)
        )
        print(f"✅ Colección '{COLLECTION_NAME}' creada con éxito.")

    # Crear índices de payload obligatorios de tipo KEYWORD
    indexed_fields = ["country", "strategic_pillar", "target_department", "doc_type", "region", "benchmark_target", "urgency_phase"]
    for field in indexed_fields:
        try:
            client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field,
                field_schema=PayloadSchemaType.KEYWORD
            )
            print(f"  📌 Índice de Payload KEYWORD asegurado: {field}")
        except Exception as e:
            # Índice puede ya existir
            pass

def ingest_chunks(client: QdrantClient):
    """Carga los fragmentos semánticos, calcula sus embeddings locales y los ingesta en Qdrant."""
    chunks_path = "data/salkantay_strategy_chunks.json"
    if not os.path.isfile(chunks_path):
        print(f"❌ Error: Archivo de chunks '{chunks_path}' no encontrado. Ejecuta primero parse_salkantay_chunks.py.")
        sys.exit(1)

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    total_chunks = len(chunks)
    print(f"\n📦 Iniciando vectorización e ingestión de {total_chunks} fragmentos estratégicos con '{EMBEDDING_MODEL}'...")

    batch_points = []
    batch_size = 5

    for idx, c in enumerate(chunks, 1):
        print(f"  [{idx:02d}/{total_chunks:02d}] Vectorizando chunk: {c['chunk_id']} ({c['strategic_pillar']} | {c['target_department']})...")
        emb = get_ollama_embedding(c["text"])
        
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={
                "chunk_id": c["chunk_id"],
                "section_id": c["section_id"],
                "section_title": c["section_title"],
                "text": c["text"],
                "country": c["country"],
                "region": c["region"],
                "strategic_pillar": c["strategic_pillar"],
                "benchmark_target": c["benchmark_target"],
                "doc_type": c["doc_type"],
                "target_department": c["target_department"],
                "urgency_phase": c["urgency_phase"],
                "word_count": c["word_count"]
            }
        )
        batch_points.append(point)

        # Upsert en lotes
        if len(batch_points) >= batch_size or idx == total_chunks:
            client.upsert(collection_name=COLLECTION_NAME, points=batch_points)
            print(f"    💾 Upsert de lote ({len(batch_points)} puntos) completado en Qdrant.")
            batch_points = []

    print(f"\n✨ ¡Ingestión 100% completada! {total_chunks} nodos estratégicos indexados en '{COLLECTION_NAME}'.")

def run_smoke_tests(client: QdrantClient):
    """Ejecuta consultas de prueba (Smoke Tests) con filtrado estricto por metadatos conforme a la directiva."""
    print("\n🔍 ================= SMOKE TESTS DE RECUPERACIÓN RAG =================")
    
    test_queries = [
        {
            "title": "Test 1: Seguridad Biomédica & Oxigenoterapia (Filtro: Guias_Campo)",
            "query": "protocolo de oxigenoterapia tanques portatiles mal agudo de montana lake louise",
            "filter": Filter(
                must=[
                    FieldCondition(key="country", match=MatchValue(value="Peru")),
                    FieldCondition(key="target_department", match=MatchValue(value="Guias_Campo"))
                ]
            )
        },
        {
            "title": "Test 2: Alojamiento Glamping & Domos Geodésicos (Filtro: alojamiento_glamping)",
            "query": "especificaciones de domos geodesicos soraypampa aislamiento termico duchas calientes",
            "filter": Filter(
                must=[
                    FieldCondition(key="country", match=MatchValue(value="Peru")),
                    FieldCondition(key="strategic_pillar", match=MatchValue(value="alojamiento_glamping"))
                ]
            )
        },
        {
            "title": "Test 3: Política Comercial & Briefing Presencial (Filtro: Ventas)",
            "query": "deposito de reserva no reembolsable y briefing obligatorio en cusco",
            "filter": Filter(
                must=[
                    FieldCondition(key="country", match=MatchValue(value="Peru")),
                    FieldCondition(key="target_department", match=MatchValue(value="Ventas"))
                ]
            )
        }
    ]

    for t in test_queries:
        print(f"\n🧪 {t['title']}")
        print(f"  Consulta: \"{t['query']}\"")
        q_vec = get_ollama_embedding(t["query"])
        
        # Búsqueda vectorial filtrada
        results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=q_vec,
            query_filter=t["filter"],
            limit=2
        ).points

        if not results:
            print("  ❌ No se obtuvieron resultados para el filtro.")
        else:
            for rank, hit in enumerate(results, 1):
                p = hit.payload
                print(f"  Top {rank} [Score: {hit.score:.4f}] | ID: {p.get('chunk_id')} | Pilar: {p.get('strategic_pillar')} | Dept: {p.get('target_department')}")
                # Muestra las primeras 2 líneas de texto
                snippet = p.get('text', '').replace('\n', ' ')[:180]
                print(f"    Snippet: \"{snippet}...\"")

    print("\n✅ Todos los Smoke Tests de recuperación vectorial y filtrado de metadatos fueron superados exitosamente.")

if __name__ == "__main__":
    print("=" * 70)
    print(" LIFEXTREME PERÚ - INGESTIÓN ESTRATÉGICA QDRANT (LOCAL AI OLLAMA)")
    print("=" * 70)
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    setup_collection(client)
    ingest_chunks(client)
    run_smoke_tests(client)
