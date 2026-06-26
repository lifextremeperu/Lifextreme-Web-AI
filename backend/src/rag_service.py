"""
rag_service.py - Servicio RAG para MAX chatbot
Estrategia: NO requiere funcion RPC personalizada en Supabase.
Usa busqueda directa por similitud coseno via httpx + PostgREST.

Tabla: knowledge_vectors
Columnas: id, vector_id, region, tier, modulo_nombre, text_content, embedding (vector 768)
Embeddings: nomic-embed-text (Ollama local)
"""
import os
import httpx
import json
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL  = "nomic-embed-text"

# Headers comunes para Supabase REST
def _sb_headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


async def get_embedding(text: str) -> list[float]:
    """
    Genera embedding con nomic-embed-text via Ollama.
    Devuelve vector de 768 dimensiones.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]


async def search_knowledge_direct(
    query: str,
    limit: int = 5,
    region: Optional[str] = None
) -> list[dict]:
    """
    Busqueda vectorial en knowledge_vectors SIN funcion RPC.
    Usa la API REST de Supabase con filtros nativos de PostgREST.
    
    Nota: PostgREST no soporta ORDER BY vectorial nativo, entonces:
    1. Obtenemos los top-N candidatos filtrando por region (si aplica)
    2. Calculamos similitud en memoria (rapido para 5-20 candidatos)
    """
    import math

    # 1. Generar embedding de la consulta
    query_embedding = await get_embedding(query)

    # 2. Obtener muestra de la tabla (con filtro de region si aplica)
    # Limitamos a 500 registros para calculo en memoria (rapido)
    async with httpx.AsyncClient(timeout=30.0) as client:
        params = {
            "select": "id,vector_id,region,tier,modulo_nombre,text_content,embedding",
            "limit": "500",
            "order": "created_at.desc"
        }
        if region:
            params["region"] = f"ilike.{region}"

        resp = await client.get(
            f"{SUPABASE_URL}/rest/v1/knowledge_vectors",
            headers=_sb_headers(),
            params=params
        )
        resp.raise_for_status()
        rows = resp.json()

    if not rows:
        return []

    # 3. Calcular similitud coseno en memoria
    def cosine_similarity(a: list, b) -> float:
        if isinstance(b, str):
            # El embedding viene como string "[0.1, 0.2, ...]" o como lista
            b = json.loads(b)
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    # 4. Calcular similitud para cada fila
    scored = []
    for row in rows:
        emb = row.get("embedding")
        if emb is None:
            continue
        try:
            sim = cosine_similarity(query_embedding, emb)
            scored.append({
                "id": row["id"],
                "vector_id": row.get("vector_id", ""),
                "region": row.get("region", ""),
                "tier": row.get("tier", 0),
                "modulo_nombre": row.get("modulo_nombre", ""),
                "text_content": row.get("text_content", ""),
                "similarity": round(sim, 4)
            })
        except Exception:
            continue

    # 5. Ordenar por similitud y retornar top-N
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return [r for r in scored[:limit] if r["similarity"] > 0.3]


async def search_knowledge(
    query: str,
    limit: int = 5,
    region: Optional[str] = None,
    min_similarity: float = 0.3
) -> list[dict]:
    """
    Funcion principal de busqueda. Intenta primero via RPC (si existe),
    si falla usa busqueda directa en memoria.
    """
    # Intentar via RPC primero (si ya fue creada manualmente)
    try:
        embedding = await get_embedding(query)
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "query_embedding": embedding,
                "match_count": limit,
                "min_similarity": min_similarity
            }
            if region:
                payload["filter_region"] = region

            resp = await client.post(
                f"{SUPABASE_URL}/rest/v1/rpc/match_knowledge_vectors",
                headers=_sb_headers(),
                json=payload
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    return data
    except Exception:
        pass

    # Fallback: busqueda directa en memoria
    return await search_knowledge_direct(query, limit=limit, region=region)


def format_context(chunks: list[dict]) -> str:
    """
    Formatea los chunks como contexto para el LLM.
    """
    if not chunks:
        return "No encontre informacion especifica. Responde con lo que sabes de Lifextreme."

    parts = []
    for i, chunk in enumerate(chunks, 1):
        sim  = chunk.get("similarity", 0)
        mod  = chunk.get("modulo_nombre", "Tour")
        reg  = (chunk.get("region") or "Peru").capitalize()
        txt  = chunk.get("text_content", "").strip()

        parts.append(
            f"[Fuente {i} | {mod} | {reg} | relevancia: {sim:.0%}]\n{txt}"
        )

    return "\n\n---\n\n".join(parts)


async def get_rag_context(query: str, region: Optional[str] = None) -> str:
    """
    Funcion principal: query → contexto RAG formateado para el LLM.
    """
    chunks = await search_knowledge(query, limit=5, region=region)
    return format_context(chunks)
