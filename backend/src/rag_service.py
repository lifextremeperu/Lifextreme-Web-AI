"""
rag_service.py - Buscador Hibrido: Catalogo Oficial Web (js/data.js) + Qdrant (336,869 vectores)
Combina en tiempo real:
  1. Catalogo exacto publicado en www.lifextreme.store (40 Tours, 28 Eventos Running/Trail, 164 Parques de Aventura, 4 Guias, 15 Equipos).
  2. Conocimiento profundo vectorial en Qdrant (Lifextreme_Knowledge + Lifextreme_FQSA_Knowledge).
"""
import os
import json
import asyncio
import unicodedata
import httpx
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

load_dotenv(override=True)

QDRANT_URL  = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL  = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"

qdrant_client = AsyncQdrantClient(url=QDRANT_URL, timeout=5.0)
_http_client  = httpx.AsyncClient(timeout=15.0)

# Cargar catalogo oficial de la web (extraido de js/data.js)
_CATALOG_PATH = Path(__file__).parent / "web_catalog.json"
WEB_CATALOG = {"tours": [], "events": [], "parks": [], "guides": [], "equips": []}
if _CATALOG_PATH.exists():
    try:
        WEB_CATALOG = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[-] Error cargando web_catalog.json: {e}")


def _norm(text: str) -> str:
    """Normaliza texto sin tildes y en minusculas para cruce rapido."""
    if not text:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", str(text).lower())
        if unicodedata.category(c) != "Mn"
    )


def search_web_catalog(query: str) -> str:
    """
    Busca instantaneamente en el catalogo oficial publicado en www.lifextreme.store:
    - 40 Tours oficiales
    - 28 Eventos (Trail Running, Maratones, Festivales)
    - 164 Parques de Aventura verificados en Peru
    - Guias y Equipos
    """
    q = _norm(query)
    sections = []

    # Detectar region mencionada (incluyendo sinonimos como selva -> iquitos/amazonas)
    REGION_MAP = {
        "cusco": ["cusco", "cuzco", "machu", "salkantay", "inca", "ausangate", "choquequirao", "valle sagrado", "humantay", "vinicunca", "colores", "quellccaya", "lares"],
        "huaraz": ["huaraz", "ancash", "cordillera blanca", "huascaran", "santa cruz", "laguna 69", "pastoruri", "ishinca", "escalada"],
        "iquitos": ["iquitos", "selva", "amazonas", "amazonia", "pacaya", "samiria", "caimanes", "ayahuasca", "jungle", "manu"],
        "arequipa": ["arequipa", "colca", "misti", "chachani", "chili"],
        "ica": ["ica", "paracas", "huacachina", "nazca", "buggies", "sandboard"],
        "piura": ["piura", "mancora", "organos", "cabo blanco", "sechura", "kitesurf", "surf"],
        "puno": ["puno", "titicaca", "sillustani", "llachon", "juli"],
        "lima": ["lima", "molina", "pachacamac", "lunahuana", "marcahuasi"],
    }
    detected_depts = set()
    for dept, kws in REGION_MAP.items():
        if any(kw in q for kw in kws):
            detected_depts.add(dept)

    # 1. ¿Pregunta por Eventos / Running / Trail / Competencias / Maratones?
    is_event_query = any(w in q for w in ["evento", "running", "trail", "maraton", "carrera", "competencia", "festival", "calendario"])
    if is_event_query or "evento" in q:
        ev_list = WEB_CATALOG.get("events", [])
        matched_ev = [
            e for e in ev_list
            if not detected_depts or _norm(e.get("dept", "")) in detected_depts
        ]
        if not matched_ev:
            matched_ev = ev_list[:8]
        ev_lines = [
            f"  • {e['title']} ({e.get('dept')}) — Fecha: {e.get('date')} {e.get('month')} 2026 | Categoría: {e.get('cat')} | Inscripción: S/ {e.get('price')} | {e.get('detail', '')}"
            for e in matched_ev[:8]
        ]
        if ev_lines:
            sections.append("EVENTOS OFICIALES PUBLICADOS EN WWW.LIFEXTREME.STORE (SECCIÓN EVENTOS):\n" + "\n".join(ev_lines))

    # 2. ¿Pregunta por Parques de Aventura / Escalada en Roca / Zipline / Canopy / Via Ferrata?
    is_park_query = any(w in q for w in ["parque", "escalada", "roca", "tirolesa", "zipline", "canopy", "ferrata", "puente", "rapel", "infraestructura"])
    if is_park_query:
        parks = WEB_CATALOG.get("parks", [])
        matched_parks = []
        for p in parks:
            p_text = _norm(f"{p.get('nombre_infraestructura','')} {p.get('region','')} {p.get('tipo','')} {p.get('descripcion','')}")
            if detected_depts and not any(d in p_text for d in detected_depts):
                continue
            matched_parks.append(p)
        if not matched_parks:
            matched_parks = parks[:8]
        p_lines = [
            f"  • {p.get('nombre_infraestructura')} ({p.get('region')}) — Tipo: {p.get('tipo')} | Dificultad: {p.get('nivel_dificultad')} | Precio est.: S/ {p.get('precio_estimado')} | {p.get('descripcion', '')[:140]}"
            for p in matched_parks[:7]
        ]
        if p_lines:
            sections.append("PARQUES DE AVENTURA VERIFICADOS EN PERÚ (DIRECTORIO LIFEXTREME):\n" + "\n".join(p_lines))

    # 3. Tours Oficiales del Catalogo Web (filtrados por region o palabras clave, o resumen general)
    tours = WEB_CATALOG.get("tours", [])
    matched_tours = []
    q_words = [w for w in q.split() if len(w) >= 4 and w not in {"para", "como", "cual", "quiero", "busco", "tour", "tours", "peru", "reservar", "precio", "cuanto"}]

    for t in tours:
        t_norm = _norm(f"{t.get('title','')} {t.get('dept','')} {t.get('detail','')}")
        dept_norm = _norm(t.get("dept", ""))
        if detected_depts and dept_norm in detected_depts:
            matched_tours.append(t)
        elif any(w in t_norm for w in q_words):
            matched_tours.append(t)

    if not matched_tours:
        # Si no filtro region especifica, mostrar los principales de cada region
        matched_tours = tours[:15]

    t_lines = [
        f"  • [ID {t['id']}] {t['title']} ({t['dept']}) — Precio: S/ {t['price']} por persona | Duración: {t.get('duration')} | Dificultad: {t.get('difficulty')} | {t.get('detail')}"
        for t in matched_tours[:12]
    ]
    if t_lines:
        sections.append("CATÁLOGO OFICIAL DE TOURS EN WWW.LIFEXTREME.STORE:\n" + "\n".join(t_lines))

    return "\n\n".join(sections)


def find_matching_catalog_item(text: str) -> Optional[dict]:
    """
    Busca si en el texto de respuesta o consulta se menciona un Tour o Evento oficial
    para adjuntar su boton de carrito garantizado.
    """
    t_norm = _norm(text)
    for t in WEB_CATALOG.get("tours", []):
        title_norm = _norm(t["title"])
        # Coincidencia por titulo completo o palabras clave principales del titulo
        key_parts = [w for w in title_norm.split() if len(w) >= 5 and w not in {"trekking", "expedicion", "circuito", "ascenso"}]
        if title_norm in t_norm or (key_parts and all(kp in t_norm for kp in key_parts[:2])):
            return {"tour": t["title"], "price_per_pax": int(t["price"])}
    for e in WEB_CATALOG.get("events", []):
        title_norm = _norm(e["title"])
        if title_norm in t_norm:
            return {"tour": f"Evento: {e['title']}", "price_per_pax": int(e["price"])}
    return None


async def get_embedding(text: str) -> list[float]:
    response = await _http_client.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text, "keep_alive": -1}
    )
    response.raise_for_status()
    return response.json()["embedding"]


async def _query_single_collection(
    collection: str,
    query_vector: list[float],
    query_filter: Optional[Filter],
    limit: int,
    min_similarity: float
) -> list[dict]:
    try:
        search_result = await qdrant_client.query_points(
            collection_name=collection,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            score_threshold=min_similarity
        )
        items = []
        for scored_point in search_result.points:
            payload = scored_point.payload or {}
            tier = int(payload.get("tier", 2))
            multiplier = 1.15 if tier == 1 else (1.0 if tier == 2 else 0.85)
            boosted_score = scored_point.score * multiplier

            raw_text = (
                payload.get("text_content")
                or payload.get("respuesta")
                or payload.get("content")
                or payload.get("text")
                or ""
            ).strip()
            if not raw_text:
                continue

            compact_text = raw_text[:550] + ("..." if len(raw_text) > 550 else "")
            items.append({
                "id": scored_point.id,
                "collection": collection,
                "region": payload.get("region", ""),
                "tier": tier,
                "modulo_nombre": payload.get("modulo_nombre") or payload.get("categoria") or collection,
                "text_content": compact_text,
                "similarity": round(boosted_score, 4),
            })
        return items
    except Exception:
        return []


async def search_knowledge(
    query: str,
    limit: int = 3,
    region: Optional[str] = None,
    min_similarity: float = 0.32,
    collection: str = "Lifextreme_Knowledge"
) -> list[dict]:
    try:
        query_vector = await get_embedding(query)
        query_filter = None
        if region:
            query_filter = Filter(
                must=[FieldCondition(key="region", match=MatchValue(value=region.lower()))]
            )

        main_task = _query_single_collection("Lifextreme_Knowledge", query_vector, query_filter, limit, min_similarity)
        fqsa_task = _query_single_collection("Lifextreme_FQSA_Knowledge", query_vector, None, 2, min_similarity)

        main_res, fqsa_res = await asyncio.gather(main_task, fqsa_task)
        combined = main_res + fqsa_res
        combined.sort(key=lambda x: x["similarity"], reverse=True)
        return combined[:limit]
    except Exception as e:
        print(f"[-] Error en Qdrant RAG: {e}")
        return []


async def get_rag_context(query: str, region: Optional[str] = None, collection: str = "Lifextreme_Knowledge") -> str:
    """
    Combina el Catalogo Oficial de www.lifextreme.store (0ms) + Busqueda Vectorial en Qdrant (~80ms).
    """
    catalog_context = search_web_catalog(query)
    chunks = await search_knowledge(query, limit=3, region=region, collection=collection)

    qdrant_parts = []
    for i, chunk in enumerate(chunks, 1):
        sim = chunk.get("similarity", 0)
        mod = chunk.get("modulo_nombre", "Conocimiento Lifextreme")
        reg = (chunk.get("region") or "Peru").capitalize()
        txt = chunk.get("text_content", "").strip()
        qdrant_parts.append(f"[Qdrant {i} | {mod} ({reg}) | {sim:.0%}]\n{txt}")

    qdrant_str = "\n\n".join(qdrant_parts) if qdrant_parts else "Usa los datos del Catálogo Oficial de arriba."
    return f"{catalog_context}\n\n=== CONOCIMIENTO TÉCNICO Y OPERATIVO EN QDRANT (336K VECTORES) ===\n{qdrant_str}"
