"""
governance_expediente_agent.py — DIRECTIVA DIR-AG-QDRANT-2026-001
Orquestador de los 3 Agentes Autónomos (Profiler -> Legal_RAG -> Publisher)
conectado al Cerebro Unificado de Lifextreme en modo `govtech_edu`.
"""
import re
import httpx
from pydantic import BaseModel, Field
from typing import Optional
from ..rag_service import get_rag_context, search_knowledge

MASTER_SYSTEM_PROMPT = """Eres el Asesor Senior en Arquitectura y Gobernanza de Inteligencia Artificial en el Perú.
Tu objetivo es redactar Expedientes Técnicos Institucionales completos, rigurosos y listos para impresión PDF.

PROCESO DE GENERACIÓN:
1. Recibes los datos del Agente Profiler (scraping web de la institución).
2. Consultas el vector store de Qdrant (colección `peru_ai_governance` + sinergia legal de `Lifextreme_Knowledge`) para recuperar:
   - Artículos específicos aplicables del D.S. 115-2025-PCM y D.S. 016-2024-JUS.
   - Si es Entidad Pública: Exigencias del Oficial de IA (Directiva N° 002-2026-PCM/SGTD), CGTD e Interoperabilidad PIDE.
   - Si es Entidad Privada / Colegio: Protocolo de consentimiento parental y sanciones ANPD de hasta 100 UIT.
   - Criterios de ISO/IEC 42001, ISO 42005 y OWASP Agentic Top 10 (2026).

ESTRUCTURA DEL EXPEDIENTE TÉCNICO (ENTREGABLE IMPRESO):
- Carátula Institucional: Nombre de la Institución, Paleta Visual, Fecha y Firma de Consultoría (Ing. Engelberth Egoavil).
- Módulo 1: Diagnóstico de Urgencia Legal y Mapeo de Brechas (ANPD / PCM / INDECOPI).
- Módulo 2: Registro Técnico Vivo de Sistemas de IA (Art. 31.1 D.S. 115).
- Módulo 3: Política Institucional y Semáforo Académico / Operativo.
- Módulo 4: Evaluaciones de Impacto Algorítmico (ISO 42005) y Ciberseguridad Agéntica (OWASP).
- Módulo 5: Plan de Implementación de 5 Semanas y Términos de Referencia / Presupuesto en Soles.

REGLA DE FORMATO:
- Genera código Markdown limpio estructurado con saltos de página CSS (`<div style="page-break-after: always;"></div>`).
- Sin muletillas ni lenguaje coloquial; tono ejecutivo, riguroso y legalmente inexpugnable.
"""


class ExpedienteRequest(BaseModel):
    institution_url: str = Field(..., description="URL institucional (ej: https://istta.edu.pe, https://unsaac.edu.pe)")
    institution_name: Optional[str] = Field(None, description="Nombre opcional de la institución")
    custom_query: Optional[str] = Field(None, description="Enfoque adicional o requerimiento específico")


class InstitutionProfile(BaseModel):
    url: str
    institution_name: str
    entity_type: str  # "Pública" | "Privada"
    sector: str       # "Universidad" | "IESTP" | "K-12 / Colegio" | "ONG / Asociación" | "Corporativo"
    digital_services: list[str]
    has_privacy_policy: bool
    brand_colors: dict[str, str]


class ExpedienteResponse(BaseModel):
    directive_code: str = "DIR-AG-QDRANT-2026-001"
    profile: InstitutionProfile
    rag_chunks_retrieved: int
    rag_context_preview: str
    system_prompt: str
    markdown_template: str


class GovernanceExpedienteAgent:
    """Ejecuta el pipeline de 3 Agentes (Profiler -> Legal_RAG -> Publisher Template)."""

    async def profile_institution(self, url: str, fallback_name: Optional[str] = None) -> InstitutionProfile:
        clean_url = url.strip()
        if not clean_url.startswith(("http://", "https://")):
            clean_url = f"https://{clean_url}"

        html_text = ""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, verify=False) as client:
                resp = await client.get(clean_url, headers={"User-Agent": "Mozilla/5.0 (Antigravity Governance Profiler/2026.1)"})
                html_text = resp.text[:40000]
        except Exception:
            html_text = ""

        lower_html = html_text.lower()
        lower_url = clean_url.lower()

        # Extraer <title>
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
        extracted_title = title_match.group(1).strip() if title_match else (fallback_name or clean_url)
        extracted_title = re.sub(r"\s+", " ", extracted_title)[:120]

        # Determinar tipo de entidad (Pública vs Privada)
        is_public = any(
            k in lower_url or k in lower_html
            for k in [".gob.pe", "nacional", "unsaac", "istta", "público", "publico", "estado peruano", "portal de transparencia"]
        )
        entity_type = "Pública" if is_public else "Privada"

        # Determinar sector educativo
        if any(k in lower_url or k in lower_html for k in ["universidad", "unsaac", "unmsm", "uni.edu", "pucp"]):
            sector = "Universidad"
        elif any(k in lower_url or k in lower_html for k in ["iestp", "instituto", "istta", "tecnológico", "tecnologico", "pedagógico"]):
            sector = "IESTP / Instituto Superior"
        elif any(k in lower_url or k in lower_html for k in ["colegio", "k-12", "escolar", "inicial", "primaria", "secundaria", "pukllasunchis"]):
            sector = "K-12 / Colegio / Educación Básica"
        else:
            sector = "Institución Educativa / Organizacional"

        # Detectar servicios digitales activos
        services = []
        service_map = {
            "Aula Virtual / Moodle / LMS": ["moodle", "aula virtual", "campus virtual", "blackboard", "canvas", "classroom"],
            "Mesa de Partes Virtual / Trámites": ["mesa de partes", "tramite", "trámite", "fut", "sgd"],
            "Admisión / Matrícula en Línea": ["admision", "admisión", "matricula", "matrícula", "inscripcion"],
            "Biblioteca Digital / Repositorio": ["repositorio", "biblioteca", "dspace", "alicia"],
            "Chatbot / Atención WhatsApp": ["whatsapp", "wa.me", "chatbot", "asistente virtual"],
            "Intranet / Sistema Académico (ERP/SIGA)": ["intranet", "siga", "erp", "sieWeb", "cubicol", "intranet académica"],
        }
        for label, kws in service_map.items():
            if any(kw in lower_html for kw in kws):
                services.append(label)
        if not services:
            services = ["Portal Web Institucional", "Correo Institucional", "Formulario de Contacto"]

        has_privacy = any(k in lower_html for k in ["política de privacidad", "politica de privacidad", "protección de datos", "29733", "016-2024"])

        # Extraer colores hexadecimales dominantes del CSS/HTML
        hex_colors = re.findall(r"#(?:[0-9a-fA-F]{6})\b", html_text)
        filtered_colors = [c.upper() for c in hex_colors if c.upper() not in {"#FFFFFF", "#000000", "#CCCCCC", "#EEEEEE", "#333333", "#666666", "#999999", "#F5F5F5"}]
        primary_color = filtered_colors[0] if filtered_colors else "#1B4D3E"
        secondary_color = filtered_colors[1] if len(filtered_colors) > 1 else "#D4AF37"

        return InstitutionProfile(
            url=clean_url,
            institution_name=fallback_name or extracted_title,
            entity_type=entity_type,
            sector=sector,
            digital_services=services,
            has_privacy_policy=has_privacy,
            brand_colors={"primary": primary_color, "secondary": secondary_color},
        )

    async def generate_expediente_package(self, req: ExpedienteRequest) -> ExpedienteResponse:
        # 1. Agente 1: Profiler
        profile = await self.profile_institution(req.institution_url, req.institution_name)

        # 2. Agente 2: Legal RAG (consulta Qdrant en modo govtech_edu)
        rag_query = (
            f"Gobernanza IA {profile.entity_type} {profile.sector} Ley 31814 DS 115-2025-PCM "
            f"DS 016-2024-JUS Directiva 002-2026-PCM ISO 42001 ISO 42005 OWASP ANPD INDECOPI {req.custom_query or ''}"
        ).strip()
        chunks = await search_knowledge(rag_query, limit=8, mode="govtech_edu")
        rag_context = await get_rag_context(rag_query, mode="govtech_edu")

        # 3. Agente 3: Estructura base Markdown lista para enriquecimiento o compilación PDF
        normativa_foco = (
            "Directiva N° 002-2026-PCM/SGTD (Oficial de IA), CGTD, Interoperabilidad PIDE y Art. 31.1 D.S. 115-2025-PCM"
            if profile.entity_type == "Pública"
            else "Protocolo de Consentimiento Parental, D.S. 016-2024-JUS (ANPD, sanciones hasta 100 UIT) y D.S. 115-2025-PCM"
        )
        md_template = f"""# EXPEDIENTE TÉCNICO DE GOBERNANZA DE IA E INTEGRIDAD DIGITAL
**Institución:** {profile.institution_name} (`{profile.url}`)  
**Naturaleza Jurídica:** Entidad {profile.entity_type} — Sector: {profile.sector}  
**Paleta Institucional Detectada:** Primaria `{profile.brand_colors['primary']}` | Secundaria `{profile.brand_colors['secondary']}`  
**Política de Privacidad Visible en Web:** {"Sí detectada" if profile.has_privacy_policy else "No detectada / Crítico (Brecha D.S. 016-2024-JUS)"}  
**Servicios Digitales Auditados:** {", ".join(profile.digital_services)}  
**Consultoría Responsable:** Ing. Engelberth Egoavil — Directiva `DIR-AG-QDRANT-2026-001`

<div style="page-break-after: always;"></div>

## Módulo 1: Diagnóstico de Urgencia Legal y Mapeo de Brechas (ANPD / PCM / INDECOPI)
- **Marco Rector Aplicable:** Ley N° 31814, D.S. N° 115-2025-PCM, D.S. N° 016-2024-JUS y {normativa_foco}.

## Módulo 2: Registro Técnico Vivo de Sistemas de IA (Art. 31.1 D.S. 115-2025-PCM)
- Inventario de activos algorítmicos y servicios digitales detectados: {", ".join(profile.digital_services)}.

<div style="page-break-after: always;"></div>

## Módulo 3: Política Institucional y Semáforo Académico / Operativo
- Clasificación de usos permitidos (Verde), supervisados (Ámbar) y prohibidos (Rojo) para docentes, administrativos y estudiantes.

## Módulo 4: Evaluaciones de Impacto Algorítmico (ISO 42005) y Ciberseguridad Agéntica (OWASP Top 10 2026)
- Controles ISO/IEC 42001, evaluación de sesgos e inyección de prompts en plataformas académicas.

<div style="page-break-after: always;"></div>

## Módulo 5: Plan de Implementación de 5 Semanas y Términos de Referencia / Presupuesto (S/)
- Hoja de ruta ejecutable en 5 semanas y estructura presupuestal en Soles (S/).
"""

        return ExpedienteResponse(
            profile=profile,
            rag_chunks_retrieved=len(chunks),
            rag_context_preview=rag_context[:2500],
            system_prompt=MASTER_SYSTEM_PROMPT,
            markdown_template=md_template,
        )
