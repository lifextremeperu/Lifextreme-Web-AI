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


if __name__ == "__main__":
    mcp.run()
