"""
ingest_peru_ai_governance.py — DIRECTIVA DIR-AG-QDRANT-2026-001
Ingesta y Vectorización en Qdrant (Colección: `peru_ai_governance`)
Unificado con el Cerebro de Lifextreme (`nomic-embed-text` 768-dim vía Ollama)
para permitir consultas híbridas sin afectar el RAG de Turismo (B2C).
"""
import os
import sys
import uuid
import httpx
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from pypdf import PdfReader
import docx

sys.stdout.reconfigure(encoding="utf-8")

# 1. Configuración de Qdrant y Ollama (Mismo motor que Lifextreme_Knowledge)
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://localhost:11434/api/embed")
COLLECTION_NAME = "peru_ai_governance"
EMBED_MODEL = "nomic-embed-text"
VECTOR_DIM = 768

# Carpeta oficial de Arquitectura y Gobernanza AI (incluye exportaciones de NotebookLM)
DEFAULT_KNOWLEDGE_FOLDER = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\ARQUITECTURA Y GOBERNANZA AI"
EXTRA_DOWNLOAD_FILES = [
    r"C:\Users\ASUS\Downloads\base_datos_instituciones_peru.csv",
    r"C:\Users\ASUS\Downloads\Expediente_de_Gobernanza_de_IA_Khipu.pptx",
    r"C:\Users\ASUS\Downloads\Gobernanza_de_IA_para_Instituto_Khipu.pptx",
    r"C:\Users\ASUS\Downloads\IIA.pdf",
]
VALID_EXTS = {".pdf", ".docx", ".md", ".txt", ".csv", ".pptx", ".html", ".json"}


def ensure_collection(qclient: QdrantClient):
    """Crea la colección `peru_ai_governance` (768-dim Cosine) si no existe."""
    collections = [c.name for c in qclient.get_collections().collections]
    if COLLECTION_NAME not in collections:
        qclient.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
        )
        print(f"[+] Colección '{COLLECTION_NAME}' creada ({VECTOR_DIM} dims, Cosine).")
    else:
        print(f"[*] Colección '{COLLECTION_NAME}' ya existe. Se actualizarán/agregarán puntos (upsert).")


def clean_text_for_embedding(text: str) -> str:
    """Elimina bytes nulos, cadenas base64 largas y caracteres de control que causan HTTP 400 en Ollama."""
    import re
    if not text:
        return ""
    # Eliminar bloques data:image/... base64
    text = re.sub(r"data:[^;]+;base64,[A-Za-z0-9+/=]+", " ", text)
    # Eliminar caracteres nulos y de control
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    # Colapsar espacios múltiples
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk_text(text: str, max_chars: int = 900, overlap: int = 150) -> list[str]:
    """Segmentación semántica con solapamiento para textos normativos, leyes y notas de NotebookLM."""
    clean = clean_text_for_embedding(text)
    if not clean:
        return []
    chunks = []
    start = 0
    while start < len(clean):
        end = start + max_chars
        chunk = clean[start:end].strip()
        if len(chunk) > 40:
            chunks.append(chunk)
        start += max_chars - overlap
    return chunks


def extract_text_from_file(filepath: Path) -> str:
    import re
    ext = filepath.suffix.lower()
    if ext == ".pdf":
        text = []
        try:
            reader = PdfReader(str(filepath))
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
        except Exception as e:
            print(f"[-] Error leyendo PDF {filepath.name}: {e}")
        return "\n".join(text)
    elif ext == ".docx":
        try:
            doc = docx.Document(str(filepath))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            print(f"[-] Error leyendo DOCX {filepath.name}: {e}")
            return ""
    elif ext == ".pptx":
        try:
            import zipfile
            slides_text = []
            with zipfile.ZipFile(filepath, "r") as z:
                slide_files = sorted([f for f in z.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml")])
                for sf in slide_files:
                    xml_bytes = z.read(sf).decode("utf-8", errors="ignore")
                    matches = re.findall(r"<a:t[^>]*>(.*?)</a:t>", xml_bytes)
                    if matches:
                        slides_text.append(" ".join(matches))
            return "\n\n".join(slides_text)
        except Exception as e:
            print(f"[-] Error leyendo PPTX {filepath.name}: {e}")
            return ""
    elif ext == ".html":
        try:
            raw_html = filepath.read_text(encoding="utf-8", errors="ignore")
            raw_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw_html, flags=re.DOTALL | re.IGNORECASE)
            text_only = re.sub(r"<[^>]+>", " ", raw_html)
            return text_only
        except Exception as e:
            print(f"[-] Error leyendo HTML {filepath.name}: {e}")
            return ""
    else:
        try:
            return filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"[-] Error leyendo texto {filepath.name}: {e}")
            return ""


def detect_scope_and_tier(filename: str, text_sample: str) -> tuple[str, int, str]:
    """
    Detecta el alcance normativo ('public', 'private_edu', 'general') y el tier (1 para NotebookLM/Leyes clave).
    """
    upper_name = filename.upper()
    upper_sample = text_sample[:600].upper()

    # Si proviene de NotebookLM o es una ley/decreto rector, darle Tier 1 (Boost 1.15x en rag_service.py)
    is_tier_1 = any(
        k in upper_name
        for k in ["NOTEBOOK", "31814", "115-2025", "016-2024", "002-2026", "42001", "42005", "OWASP", "DIRECTIVA"]
    )
    tier = 1 if is_tier_1 else 2

    if any(k in upper_name or k in upper_sample for k in ["SGTD", "PCM", "PIDE", "002-2026", "ENTIDAD PUBLICA", "ESTADO"]):
        scope = "public"
        modulo = "Gobernanza IA Sector Público (PCM/SGTD/PIDE)"
    elif any(k in upper_name or k in upper_sample for k in ["ANPD", "016-2024", "COLEGIO", "K-12", "MENORES", "UNIVERSIDAD", "IESTP", "EDUCACION"]):
        scope = "private_edu"
        modulo = "Cumplimiento Educativo & Protección de Datos (ANPD/MINEDU)"
    else:
        scope = "general"
        modulo = "Arquitectura & Estándares IA (ISO 42001 / OWASP / Ley 31814)"

    return scope, tier, modulo


def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    try:
        response = httpx.post(
            OLLAMA_EMBED_URL,
            json={"model": EMBED_MODEL, "input": texts},
            timeout=120.0,
        )
        if response.status_code == 200:
            return response.json().get("embeddings", [])
    except Exception:
        pass

    # Fallback individual resiliente (usa /api/embeddings con recorte seguro si algún fragmento excede tokens)
    single_url = OLLAMA_EMBED_URL.replace("/api/embed", "/api/embeddings")
    vectors = []
    for t in texts:
        safe_t = t[:700] if len(t) > 700 else t
        try:
            r = httpx.post(
                single_url,
                json={"model": EMBED_MODEL, "prompt": safe_t},
                timeout=60.0,
            )
            if r.status_code == 200 and "embedding" in r.json():
                vectors.append(r.json()["embedding"])
            else:
                r2 = httpx.post(
                    single_url,
                    json={"model": EMBED_MODEL, "prompt": safe_t[:350]},
                    timeout=60.0,
                )
                vectors.append(r2.json().get("embedding", [0.0] * VECTOR_DIM))
        except Exception:
            vectors.append([0.0] * VECTOR_DIM)
    return vectors


def get_existing_point_ids(qclient: QdrantClient) -> set[str]:
    existing = set()
    offset = None
    while True:
        try:
            records, next_offset = qclient.scroll(
                collection_name=COLLECTION_NAME,
                limit=2000,
                with_payload=False,
                with_vectors=False,
                offset=offset,
            )
            for rec in records:
                existing.add(str(rec.id))
            if not next_offset:
                break
            offset = next_offset
        except Exception:
            break
    return existing


def populate_knowledge_base(knowledge_folder: str = DEFAULT_KNOWLEDGE_FOLDER):
    folder_path = Path(knowledge_folder)
    if not folder_path.exists():
        print(f"[-] La carpeta no existe o no es accesible: {folder_path}")
        return

    qclient = QdrantClient(url=QDRANT_URL, timeout=120.0)
    ensure_collection(qclient)
    existing_ids = get_existing_point_ids(qclient)
    print(f"[*] {len(existing_ids)} vectores ya existentes en '{COLLECTION_NAME}' (se omitirán duplicados).")

    # Si hay un archivo takeout*.zip en Downloads y aún no se ha descomprimido, extraerlo
    downloads_dir = Path(r"C:\Users\ASUS\Downloads")
    extract_target = folder_path / "NotebookLM_Takeout"
    if downloads_dir.exists() and not extract_target.exists():
        import zipfile
        for zpath in sorted(downloads_dir.glob("takeout*.zip"))[:1]:
            try:
                extract_target.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(zpath, "r") as zf:
                    zf.extractall(extract_target)
                print(f"[+] Google Takeout detectado y descomprimido: {zpath.name}")
            except Exception as e:
                print(f"[-] Error descomprimiendo {zpath.name}: {e}")

    files = [
        p for p in folder_path.rglob("*")
        if p.is_file()
        and p.suffix.lower() in VALID_EXTS
        and not p.name.lower().endswith(("metadata.json", "metadata(1).json", "metadata(2).json"))
        and "(1)." not in p.name
        and "(2)." not in p.name
    ]
    for extra in EXTRA_DOWNLOAD_FILES:
        ep = Path(extra)
        if ep.exists() and ep not in files:
            files.append(ep)

    print(f"[*] Encontrados {len(files)} documentos en total...")

    total_chunks = 0
    skipped_chunks = 0
    batch_size = 16

    for filepath in files:
        content = extract_text_from_file(filepath)
        chunks = chunk_text(content)
        if not chunks:
            continue

        # Filtrar fragmentos que ya están en Qdrant
        pending_items = []
        for idx, ch in enumerate(chunks):
            pid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"peru_ai_gov::{filepath.name}::{idx}"))
            if pid in existing_ids:
                skipped_chunks += 1
            else:
                pending_items.append((idx, pid, ch))

        if not pending_items:
            continue

        is_from_notebook = "NotebookLM_Takeout" in str(filepath) or "Khipu" in filepath.name
        scope, tier, modulo_nombre = detect_scope_and_tier(filepath.name, pending_items[0][2])
        if is_from_notebook:
            tier = 1
            modulo_nombre = f"NotebookLM Takeout ({modulo_nombre})"

        print(f"  -> Vectorizando '{filepath.name}' ({len(pending_items)} fragmentos nuevos | scope={scope} | tier={tier})...")

        for i in range(0, len(pending_items), batch_size):
            batch = pending_items[i : i + batch_size]
            batch_texts = [item[2] for item in batch]
            vectors = get_embeddings_batch(batch_texts)

            points = []
            for (global_idx, point_uuid, chunk_str), vec in zip(batch, vectors):
                payload = {
                    "source_file": filepath.name,
                    "source": filepath.name,
                    "chunk_index": global_idx,
                    "text": chunk_str,
                    "text_content": chunk_str,
                    "scope": scope,
                    "area": "govtech_edu",
                    "tier": tier,
                    "region": "peru",
                    "modulo_nombre": modulo_nombre,
                }
                points.append(PointStruct(id=point_uuid, vector=vec, payload=payload))
                existing_ids.add(point_uuid)

            for attempt in range(3):
                try:
                    qclient.upsert(collection_name=COLLECTION_NAME, points=points)
                    total_chunks += len(points)
                    break
                except Exception as e:
                    if attempt == 2:
                        print(f"    [-] Timeout en upsert tras 3 intentos: {e}")

    print(
        f"\n✅ Ingesta finalizada: {total_chunks} fragmentos nuevos vectorizados "
        f"({skipped_chunks} ya existían). Total en '{COLLECTION_NAME}': {len(existing_ids)} vectores."
    )


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_KNOWLEDGE_FOLDER
    populate_knowledge_base(target_dir)
