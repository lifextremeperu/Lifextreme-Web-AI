"""
generar_expediente.py — Consola Interactiva del Asesor de Arquitectura y Gobernanza IA (DIR-AG-QDRANT-2026-001)
Recibe cualquier URL institucional del Perú (Colegio, IESTP, Universidad o Entidad Pública),
consulta los 18,932 vectores de `peru_ai_governance` en Qdrant y compila el Expediente Técnico en PDF A4 listo para imprimir.
"""
import asyncio
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.agents.governance_expediente_agent import GovernanceExpedienteAgent, ExpedienteRequest
from scripts.build_expediente_pdf import convert_md_to_pdf


def _slugify(text: str) -> str:
    clean = re.sub(r"https?://", "", text.lower().strip())
    clean = re.sub(r"[^a-z0-9]+", "_", clean).strip("_")
    return clean[:40] or "institucion"


async def run_pipeline(url: str, name: str | None = None):
    print(f"\n[1/3] Ejecutando Agente 1 (Profiler Web) sobre: {url} ...")
    agent = GovernanceExpedienteAgent()
    res = await agent.generate_expediente_package(
        ExpedienteRequest(institution_url=url, institution_name=name)
    )
    prof = res.profile
    print(f"      -> Institución detectada : {prof.institution_name}")
    print(f"      -> Naturaleza / Sector   : Entidad {prof.entity_type} | {prof.sector}")
    print(f"      -> Servicios Digitales   : {', '.join(prof.digital_services)}")
    print(f"      -> Paleta CSS            : Primaria {prof.brand_colors['primary']} | Secundaria {prof.brand_colors['secondary']}")

    print(f"\n[2/3] Ejecutando Agente 2 (Legal RAG en Qdrant `peru_ai_governance` - 18,932 vectores)...")
    print(f"      -> Fragmentos normativos recuperados (Tier 1): {res.rag_chunks_retrieved}")

    slug = _slugify(name or prof.institution_name or url)
    out_dir = PROJECT_ROOT / "reportes_b2b"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"Expediente_Tecnico_{slug}_2026.md"
    pdf_path = PROJECT_ROOT / f"Expediente_Tecnico_{slug}_2026.pdf"

    # Enriquecer el Markdown con la evidencia normativa recuperada de Qdrant y la firma de los 4 especialistas
    full_md = (
        res.markdown_template
        + "\n\n---\n\n## ANEXO A: EVIDENCIA NORMATIVA RECUPERADA DEL CEREBRO QDRANT (`peru_ai_governance`)\n\n"
        + res.rag_context_preview
        + "\n\n---\n\n### FIRMAS DEL COMITÉ CONSULTOR MULTIDISCIPLINARIO (CUSCO, PERÚ)\n"
        + "* **Ing. Engelberth Egoavil** — *Director de Arquitectura IA, RAG & Ciberseguridad (OWASP / Art. 31.1)*\n"
        + "* **Magíster en Psicología** — *Directora de Evaluación de Impacto Cognitivo y Protección de Menores (ISO/IEC 42005)*\n"
        + "* **Magíster en Educación (Directora Educativa)** — *Directora de Gestión Pedagógica y Adecuación MINEDU*\n"
        + "* **Magíster en Antropología** — *Director de Equidad Intercultural, Pueblos Originarios y Enfoque Territorial*\n"
    )
    md_path.write_text(full_md, encoding="utf-8")

    print(f"\n[3/3] Ejecutando Agente 3 (Publisher PDF A4 de Imprenta)...")
    convert_md_to_pdf(str(md_path), str(pdf_path), prof.brand_colors)
    print(f"\n==================================================================")
    print(f"EXPEDIENTE LISTO PARA IMPRIMIR:")
    print(f"  -> Markdown : {md_path}")
    print(f"  -> PDF A4   : {pdf_path}")
    print(f"==================================================================\n")

    try:
        os.startfile(str(pdf_path))
    except Exception:
        pass


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        u = sys.argv[1]
        n = sys.argv[2] if len(sys.argv) >= 3 else None
    else:
        print("==================================================================")
        print("  ASESOR SENIOR DE ARQUITECTURA Y GOBERNANZA IA (QDRANT 18.9K)    ")
        print("==================================================================")
        u = input("Ingresa la URL de la institucion (ej. https://urusayhua.edu.pe): ").strip()
        n = input("Nombre de la institucion (opcional, Enter para autodetectar): ").strip() or None

    if u:
        asyncio.run(run_pipeline(u, n))
