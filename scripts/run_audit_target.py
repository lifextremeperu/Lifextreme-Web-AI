"""
run_audit_target.py — Ejecuta Agente 1 (Scraper/Profiler) + Agente 2 (Consulta Qdrant `peru_ai_governance`)
para una URL institucional dada y devuelve el perfil real + fragmentos normativos recuperados.
"""
import asyncio
import json
import re
import sys
from pathlib import Path
import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend.src.agents.governance_expediente_agent import GovernanceExpedienteAgent, ExpedienteRequest
from backend.src.rag_service import search_knowledge

sys.stdout.reconfigure(encoding="utf-8")


async def inspect_institution(url: str):
    agent = GovernanceExpedienteAgent()
    profile = await agent.profile_institution(url)

    # Extraer texto adicional de la home de la institución para identificar carreras, sede, RUC, etc.
    raw_text_snippets = []
    links_found = []
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True, verify=False) as client:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Antigravity Governance Auditor/2026.1)"})
            html = r.text
            # Extraer encabezados h1, h2, h3, p
            for m in re.finditer(r"<(h1|h2|h3|p|li|a)[^>]*>(.*?)</\1>", html, re.IGNORECASE | re.DOTALL):
                clean = re.sub(r"<[^>]+>", " ", m.group(2))
                clean = re.sub(r"\s+", " ", clean).strip()
                if 15 <= len(clean) <= 220 and clean not in raw_text_snippets:
                    raw_text_snippets.append(clean)
            for m in re.finditer(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
                href = m.group(1)
                if any(k in href.lower() for k in ["virtual", "aula", "admision", "transparencia", "tramite", "mesa", "biblioteca", "programa", "carrera", "nosotros"]):
                    if href not in links_found:
                        links_found.append(href)
    except Exception as e:
        raw_text_snippets.append(f"Error scraping extra: {e}")

    # Consultas específicas a Qdrant (`peru_ai_governance`)
    queries = [
        "Instituto de Educación Superior Tecnológico IESTP Ley 31814 DS 115-2025-PCM Oficial de IA Directiva 002-2026-PCM",
        "DS 016-2024-JUS ANPD protección de datos personales estudiantes educación superior sanciones UIT",
        "Registro Técnico de Sistemas de IA Art 31.1 DS 115-2025-PCM ISO 42001 ISO 42005",
        "Presupuesto implementación gobernanza IA instituto educación superior semanas TDR Soles",
    ]
    rag_hits = []
    seen_ids = set()
    for q in queries:
        chunks = await search_knowledge(q, limit=5, mode="govtech_edu")
        for c in chunks:
            if c["id"] not in seen_ids:
                seen_ids.add(c["id"])
                rag_hits.append(c)

    out = {
        "profile": profile.model_dump(),
        "web_snippets": raw_text_snippets[:35],
        "key_links": links_found[:20],
        "rag_hits_count": len(rag_hits),
        "rag_top_chunks": rag_hits[:12],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://urusayhua.edu.pe/"
    asyncio.run(inspect_institution(target))
