"""
rag_service.py - Servicio RAG para MAX chatbot
Estrategia: Búsqueda vectorial ultra rápida 100% local usando Qdrant.

Colección: Lifextreme_Knowledge
Embeddings: nomic-embed-text (Ollama local, 768 dimensiones)
"""
import os
import httpx
from dotenv import load_dotenv
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

load_dotenv()

QDRANT_URL   = "http://localhost:6333"
OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL  = "nomic-embed-text"
COLLECTION   = "Lifextreme_Knowledge"

# Cliente asíncrono de Qdrant para integrarse perfectamente con FastAPI
qdrant_client = AsyncQdrantClient(url=QDRANT_URL)


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


async def search_knowledge(
    query: str,
    limit: int = 5,
    region: Optional[str] = None,
    min_similarity: float = 0.3
) -> list[dict]:
    """
    Búsqueda vectorial nativa en Qdrant.
    Mucho más rápida y exacta que el cálculo manual en Python.
    """
    try:
        # 1. Generar vector de la pregunta
        query_vector = await get_embedding(query)
        
        # 2. Configurar filtro si se provee la región
        query_filter = None
        if region:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="region",
                        match=MatchValue(value=region.lower())
                    )
                ]
            )

        # 3. Buscar similitud en Qdrant
        search_result = await qdrant_client.search(
            collection_name=COLLECTION,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=min_similarity
        )
        
        # 4. Formatear la respuesta para el agente y aplicar Boosting por Tier
        results = []
        for scored_point in search_result:
            payload = scored_point.payload or {}
            tier = payload.get("tier", 3)
            
            # Mathematical Boosting
            multiplier = 1.0
            if tier == 1:
                multiplier = 1.15
            elif tier == 2:
                multiplier = 1.00
            elif tier >= 3:
                multiplier = 0.85
                
            boosted_score = scored_point.score * multiplier
            
            results.append({
                "id": scored_point.id,
                "region": payload.get("region", ""),
                "tier": tier,
                "modulo_nombre": payload.get("modulo_nombre", ""),
                "text_content": payload.get("text_content", ""),
                "similarity": round(boosted_score, 4),
                "raw_score": round(scored_point.score, 4)
            })
            
        # Reordenar por el score boosteado
        results.sort(key=lambda x: x["similarity"], reverse=True)
            
        return results

    except Exception as e:
        print(f"[-] Error en Qdrant RAG: {e}")
        return []


def format_context(chunks: list[dict]) -> str:
    """
    Formatea los chunks como contexto para el LLM.
    """
    if not chunks:
        return "No encontré información específica. Responde con lo que sabes de Lifextreme."

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
    Función principal: query → contexto RAG formateado para el LLM.
    """
    chunks = await search_knowledge(query, limit=5, region=region)
    return format_context(chunks)

