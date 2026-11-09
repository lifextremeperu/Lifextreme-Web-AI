import sys
import os

# Asegurar que el proyecto raiz este en el path para imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from mcp.server.fastmcp import FastMCP
from agents_core.argon.sre_controller import (
    check_ram_and_docker,
    check_qdrant_vectors,
    audit_git_security,
    audit_exposed_secrets,
    audit_broken_python_imports,
    audit_orphan_scripts,
)

# Servidor MCP exclusivo de 4 Argon
mcp = FastMCP("Argon_CTO_SRE")


# ─── Tools SRE ────────────────────────────────────────────────────────────────

@mcp.tool()
def argon_auditar_recursos() -> str:
    """Verifica cuanta RAM queda libre en el sistema Windows y que contenedores Docker estan corriendo."""
    return check_ram_and_docker()


@mcp.tool()
def argon_estado_qdrant() -> str:
    """Comprueba si la base vectorial Qdrant esta encendida en localhost:6333 y lista sus colecciones."""
    return check_qdrant_vectors()


@mcp.tool()
def argon_auditoria_git() -> str:
    """Revisa que archivos han cambiado en el repositorio y alerta si hay archivos sensibles sin ignorar."""
    return audit_git_security()


# ─── Tools de Auditoria de Codigo ─────────────────────────────────────────────

@mcp.tool()
def argon_secretos_expuestos() -> str:
    """
    Escanea TODO el codigo del proyecto buscando credenciales hardcodeadas:
    API keys, tokens JWT, passwords, connection strings de base de datos, y claves de GCP/Google.
    Solo lee archivos, no modifica nada. Ideal para auditar antes de un deploy.
    """
    return audit_exposed_secrets()


@mcp.tool()
def argon_imports_rotos() -> str:
    """
    Analiza todos los archivos .py del proyecto y detecta errores de sintaxis
    e imports que apuntan a modulos inexistentes dentro del proyecto.
    Util para encontrar scripts que fallaran en produccion sin ejecutarlos.
    """
    return audit_broken_python_imports()


@mcp.tool()
def argon_scripts_huerfanos() -> str:
    """
    Detecta scripts de utilidad, archivos temporales y JSONs sensibles sueltos
    en la raiz del proyecto que no forman parte del sistema productivo.
    Ayuda a mantener el proyecto limpio y seguro.
    """
    return audit_orphan_scripts()


# ─── Tools de Gobernanza IA & Puente NotebookLM (DIR-AG-QDRANT-2026-001) ──────

@mcp.tool()
def argon_ingestar_gobernanza_ia(
    carpeta: str = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\ARQUITECTURA Y GOBERNANZA AI"
) -> str:
    """
    Ingesta y vectoriza todos los PDFs, DOCX y notas de NotebookLM de la carpeta
    'ARQUITECTURA Y GOBERNANZA AI' dentro de la colección `peru_ai_governance` en Qdrant (localhost:6333)
    usando `nomic-embed-text` (mismo cerebro que Lifextreme, aislado de turismo B2C).
    """
    try:
        from scripts.ingest_peru_ai_governance import populate_knowledge_base
        populate_knowledge_base(carpeta)
        return f"✅ Ingesta completada desde '{carpeta}' hacia la colección Qdrant `peru_ai_governance`."
    except Exception as e:
        return f"[-] Error en ingesta de Gobernanza IA: {e}"


@mcp.tool()
def argon_guardar_nota_notebooklm(titulo: str, contenido: str, scope: str = "general") -> str:
    """
    Puente MCP NotebookLM -> Qdrant: Guarda cualquier investigación, informe, tabla o síntesis
    del cuaderno 'ARQUITECTURA Y GOBERNANZA IA' de NotebookLM en `peru_ai_governance` con Tier 1 (1.15x boost).
    """
    try:
        from scripts.notebooklm_bridge import save_notebooklm_synthesis_to_qdrant
        n = save_notebooklm_synthesis_to_qdrant(titulo, contenido, scope)
        return f"✅ Se vectorizaron {n} fragmentos de NotebookLM ('{titulo}') en `peru_ai_governance` (Tier 1)."
    except Exception as e:
        return f"[-] Error guardando síntesis de NotebookLM en Qdrant: {e}"


@mcp.tool()
async def argon_generar_expediente_institucion(url_institucion: str, nombre_institucion: str = "") -> str:
    """
    Ejecuta la Directiva DIR-AG-QDRANT-2026-001 (Agente 1 Profiler + Agente 2 Legal RAG + Agente 3 Publisher)
    para cualquier URL educativa o institucional del Perú (ej. istta.edu.pe, pukllasunchis.org, unsaac.edu.pe).
    """
    try:
        from backend.src.agents.governance_expediente_agent import GovernanceExpedienteAgent, ExpedienteRequest
        agent = GovernanceExpedienteAgent()
        res = await agent.generate_expediente_package(
            ExpedienteRequest(institution_url=url_institucion, institution_name=nombre_institucion or None)
        )
        return (
            f"✅ Expediente generado para {res.profile.institution_name} ({res.profile.entity_type} - {res.profile.sector})\n"
            f"Colores detectados: {res.profile.brand_colors}\n"
            f"Vectores recuperados: {res.rag_chunks_retrieved}\n\n"
            f"{res.markdown_template}\n\n"
            f"--- CONTEXTO RAG RECUPERADO ---\n{res.rag_context_preview}"
        )
    except Exception as e:
        return f"[-] Error generando expediente técnico: {e}"


if __name__ == "__main__":
    mcp.run()
