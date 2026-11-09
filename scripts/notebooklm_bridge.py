"""
notebooklm_bridge.py — Puente Vía B (NotebookLM <-> Qdrant `peru_ai_governance`)
Permite:
1. Extraer o consultar tu cuaderno privado de NotebookLM ("ARQUITECTURA Y GOBERNANZA IA")
   usando tu propia sesión de Chrome/Edge vía CDP (sin necesidad del botón 'Compartir').
2. Ingestar notas/respuestas copiadas o extraídas de NotebookLM directamente en Qdrant
   con `tier=1` (prioridad máxima 1.15x) para no depender del límite de cuota de NotebookLM.
"""
import sys
import uuid
import httpx
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

sys.stdout.reconfigure(encoding="utf-8")

QDRANT_URL = "http://localhost:6333"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
COLLECTION_NAME = "peru_ai_governance"
EMBED_MODEL = "nomic-embed-text"
NOTEBOOK_ID = "59cdb95f-0cdd-4c27-b69d-17073bb24228"
NOTEBOOK_URL = f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}"


def save_notebooklm_synthesis_to_qdrant(title: str, content: str, scope: str = "general") -> int:
    """
    Guarda cualquier respuesta, nota, tabla o informe generado por tu cuaderno
    'ARQUITECTURA Y GOBERNANZA IA' de NotebookLM directamente en Qdrant con Tier 1.
    """
    from ingest_peru_ai_governance import chunk_text, ensure_collection, get_embeddings_batch

    qclient = QdrantClient(url=QDRANT_URL, timeout=30.0)
    ensure_collection(qclient)

    chunks = chunk_text(content, max_chars=1200, overlap=200)
    if not chunks:
        return 0

    vectors = get_embeddings_batch(chunks)
    points = []
    for idx, (chunk_str, vec) in enumerate(zip(chunks, vectors)):
        point_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"notebooklm::{title}::{idx}"))
        payload = {
            "source_file": f"NotebookLM__{title}",
            "source": f"NotebookLM: {title}",
            "chunk_index": idx,
            "text": chunk_str,
            "text_content": chunk_str,
            "scope": scope,
            "area": "govtech_edu",
            "tier": 1,  # Máxima prioridad (1.15x boost en rag_service.py)
            "region": "peru",
            "modulo_nombre": f"NotebookLM Síntesis ({title})",
        }
        points.append(PointStruct(id=point_uuid, vector=vec, payload=payload))

    qclient.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Guardados {len(points)} fragmentos de NotebookLM ('{title}') en Qdrant con Tier 1.")
    return len(points)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        note_title = sys.argv[1]
        note_file = Path(sys.argv[2])
        if note_file.exists():
            text = note_file.read_text(encoding="utf-8", errors="ignore")
            save_notebooklm_synthesis_to_qdrant(note_title, text)
        else:
            save_notebooklm_synthesis_to_qdrant(note_title, sys.argv[2])
    else:
        print("Uso: python scripts/notebooklm_bridge.py <Titulo_Nota> <Ruta_Archivo_o_Texto>")
