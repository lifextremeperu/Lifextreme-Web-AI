"""
governance_studio_server.py — Backend Interactivo tipo ChatGPT / Gemini Studio (Puerto 8090)
Conecta la interfaz conversacional `asesor-gobernanza.html` con:
  1. Agente 1 (Live Web Scraper): Analiza en tiempo real CUALQUIER URL ingresada en el chat.
  2. Agente 2 (Qdrant RAG `peru_ai_governance` - 18,932 vectores): Recupera leyes, multas y jurisprudencia.
  3. Agente 3 (Compilador PDF PyMuPDF): Genera al instante el archivo PDF A4 descargable para cualquier web.
"""
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

sys.stdout.reconfigure(encoding="utf-8")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.agents.governance_expediente_agent import GovernanceExpedienteAgent
from backend.src.rag_service import search_knowledge
from scripts.build_expediente_pdf import convert_md_to_pdf
from scripts.corporate_dossier_builder import build_corporate_expediente_markdown

app = FastAPI(title="Governance AI Studio — Antigravity + Qdrant 18.9K")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

gov_agent = GovernanceExpedienteAgent()


def _extract_url_from_text(text: str) -> Optional[str]:
    # Buscar URL explícita con http/https
    m = re.search(r"(https?://[^\s,;\"'<>]+)", text, re.IGNORECASE)
    if m:
        return m.group(1).rstrip(".,;)")
    # Buscar dominio tipo xxx.edu.pe, xxx.gob.pe, xxx.org.pe, xxx.com, xxx.org, xxx.pe
    m2 = re.search(r"\b([a-zA-Z0-9\-]+\.(?:edu\.pe|gob\.pe|org\.pe|com\.pe|edu|org|pe|com|net)(?:/[^\s]*)?)\b", text, re.IGNORECASE)
    if m2:
        return "https://" + m2.group(1).rstrip(".,;)")
    return None


def _slugify(text: str) -> str:
    clean = re.sub(r"https?://", "", text.lower().strip())
    clean = re.sub(r"[^a-z0-9]+", "_", clean).strip("_")
    return clean[:38] or "entidad"


async def _scrape_deep_details(url: str) -> dict:
    """Extrae programas/carreras, encabezados, enlaces clave y metadatos reales del HTML de cualquier URL."""
    headings = []
    programs = []
    meta_desc = ""
    emails = []
    phones = []
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, verify=False) as client:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Antigravity Governance AI Studio/2026)"})
            html = r.text[:80000]

            # Meta description
            md_m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
            if md_m:
                meta_desc = md_m.group(1).strip()

            # Correos y teléfonos
            emails = list(dict.fromkeys(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)))[:4]
            phones = list(dict.fromkeys(re.findall(r"(?:\+?51\s?)?9\d{2}[\s-]?\d{3}[\s-]?\d{3}", html)))[:4]

            # Encabezados H1, H2, H3, A
            for m in re.finditer(r"<(h1|h2|h3|a|li)[^>]*>(.*?)</\1>", html, re.I | re.S):
                txt = re.sub(r"<[^>]+>", " ", m.group(2))
                txt = re.sub(r"\s+", " ", txt).strip()
                if 6 <= len(txt) <= 110:
                    low = txt.lower()
                    if any(k in low for k in ["carrera", "programa", "ingenier", "enfermer", "contabil", "administrac", "arquitectura", "derecho", "educac", "medicina", "beca", "colegio", "primaria", "secundaria", "inicial", "posgrado", "maestr", "agropecuar", "turismo", "gastronom", "sistemas", "computac"]):
                        if txt not in programs:
                            programs.append(txt)
                    elif m.group(1).lower() in {"h1", "h2", "h3"} and txt not in headings:
                        headings.append(txt)
    except Exception:
        pass

    return {
        "meta_description": meta_desc,
        "headings": headings[:8],
        "programs_detected": programs[:10],
        "emails": emails,
        "phones": phones,
    }


@app.post("/api/governance/chat")
async def governance_chat_endpoint(req: Request):
    body = await req.json()
    prompt = (body.get("prompt") or "").strip()
    explicit_url = (body.get("url") or "").strip()

    target_url = explicit_url or _extract_url_from_text(prompt)

    # 1. Si hay una URL detectada, ejecutar el pipeline completo de 3 Agentes sobre esa web
    if target_url:
        profile = await gov_agent.profile_institution(target_url)
        deep = await _scrape_deep_details(profile.url)

        rag_query = (
            f"Gobernanza IA {profile.entity_type} {profile.sector} Ley 31814 DS 115-2025-PCM "
            f"DS 016-2024-JUS Directiva 002-2026-PCM ISO 42001 ISO 42005 OWASP ANPD {prompt}"
        )
        chunks = await search_knowledge(rag_query, limit=6, mode="govtech_edu")

        programs_str = ", ".join(deep["programs_detected"][:6]) if deep["programs_detected"] else ", ".join(deep["headings"][:4]) or "Programas académicos y administrativos generales"
        contacts_str = ", ".join(deep["emails"] + deep["phones"]) or "Portal web institucional"

        is_pub = profile.entity_type == "Pública"
        ticket_express = "S/ 18,500.00" if is_pub else ("S/ 5,800.00" if "K-12" in profile.sector else "S/ 6,500.00")
        ticket_integral = "S/ 36,800.00 (Contratación Directa <= 8 UIT)" if is_pub else ("S/ 8,500.00" if "K-12" in profile.sector else "S/ 12,800.00")
        per_member = "S/ 8,280.00 c/u" if is_pub else ("S/ 1,910.00 c/u" if "K-12" in profile.sector else "S/ 2,880.00 c/u")

        norma_clave = (
            "Directiva N° 002-2026-PCM/SGTD (Oficial de IA - OIA), Comité de Gobierno y Transformación Digital (CGTD), Interoperabilidad PIDE y Art. 31.1 D.S. N° 115-2025-PCM"
            if is_pub
            else "Ley N° 29733 y Nuevo Reglamento D.S. N° 016-2024-JUS (ANPD — Multas de 5 a 100 UIT = S/ 26,750 a S/ 535,000), Consentimiento Parental de Menores y Art. 31.1 D.S. N° 115-2025-PCM"
        )

        # Construir el Expediente Corporativo Completo (10 Capítulos estilo Big-4) para esta institución y compilarlo a PDF A4 real
        slug = _slugify(profile.institution_name or target_url)
        md_dir = PROJECT_ROOT / "reportes_b2b"
        md_dir.mkdir(parents=True, exist_ok=True)
        md_file = md_dir / f"Expediente_Tecnico_{slug}_2026.md"
        pdf_rel_name = f"reportes_b2b/Expediente_Tecnico_{slug}_2026.pdf"
        pdf_file = PROJECT_ROOT / pdf_rel_name

        expediente_md = build_corporate_expediente_markdown(
            institution_name=profile.institution_name,
            url=profile.url,
            entity_type=profile.entity_type,
            sector=profile.sector,
            programs_str=programs_str,
            digital_services=profile.digital_services,
            contacts_str=contacts_str,
            has_privacy_policy=profile.has_privacy_policy,
            slug=slug,
        )
        md_file.write_text(expediente_md, encoding="utf-8")
        convert_md_to_pdf(str(md_file), str(pdf_file), profile.brand_colors)

        return JSONResponse({
            "mode": "audit_url",
            "profile": profile.model_dump(),
            "deep_scrape": deep,
            "ticket_express": ticket_express,
            "ticket_integral": ticket_integral,
            "per_member": per_member,
            "pdf_url": f"/{pdf_rel_name}",
            "markdown": expediente_md,
            "rag_citations": [
                {
                    "source": c.get("modulo_nombre", "peru_ai_governance"),
                    "similarity": round(c.get("similarity", 0) * 100, 1),
                    "text": c.get("text_content", "")[:320]
                }
                for c in chunks
            ],
        })

    # 2. Si es una pregunta abierta o consulta normativa sin URL, consultar los 18,932 vectores de Qdrant
    chunks = await search_knowledge(prompt, limit=6, mode="govtech_edu")
    citations = [
        {
            "source": c.get("modulo_nombre", "peru_ai_governance"),
            "similarity": round(c.get("similarity", 0) * 100, 1),
            "text": c.get("text_content", "")[:420]
        }
        for c in chunks
    ]
    synthesized = (
        f"### Respuesta del Cerebro de Gobernanza IA (`peru_ai_governance` — 18,932 Vectores)\n\n"
        f"He consultado nuestra base vectorial unificada para: **\"{prompt}\"**.\n\n"
        f"**Evidencia Normativa y Técnica Recuperada (Top {len(citations)} fragmentos Tier 1):**\n\n"
        + "\n\n".join(
            f"- **[{i+1}] {c['source']} (Relevancia: {c['similarity']}%)**:\n  > {c['text']}"
            for i, c in enumerate(citations)
        )
        + "\n\n💡 *Tip: Pega cualquier URL institucional en el chat (ej. `https://urusayhua.edu.pe`, `https://khipu.edu.pe`, `https://cibertec.edu.pe`) para escanear su web en vivo y generar su Expediente Técnico en PDF A4 al instante.*"
    )
    return JSONResponse({
        "mode": "rag_query",
        "markdown": synthesized,
        "rag_citations": citations,
    })


# Servir archivos estáticos del proyecto en el mismo puerto 8090
app.mount("/", StaticFiles(directory=str(PROJECT_ROOT), html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8090, log_level="info")
