import subprocess
import httpx
import psutil
import os
import ast
import re
from pathlib import Path

# ─── Rutas del proyecto ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Extensiones de codigo que Argon analiza
CODE_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx"}
SKIP_DIRS  = {"node_modules", "__pycache__", ".git", "venv", "env", ".quartz", "data"}


def _iter_code_files(root: Path):
    """Generador de archivos de codigo del proyecto excluyendo carpetas pesadas."""
    for f in root.rglob("*"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        if f.suffix in CODE_EXTS and f.is_file():
            yield f


# ─── Herramientas SRE originales ─────────────────────────────────────────────

def check_ram_and_docker() -> str:
    """Revisa el consumo de RAM del host (Windows) y el estado de contenedores Docker."""
    try:
        mem = psutil.virtual_memory()
        ram_info = (
            f"Total : {mem.total / 1024**3:.1f} GB\n"
            f"Usado : {mem.used / 1024**3:.1f} GB\n"
            f"Libre : {mem.available / 1024**3:.1f} GB\n"
            f"Uso   : {mem.percent:.1f}%"
        )
        docker_cmd = subprocess.run(
            ["docker", "stats", "--no-stream", "--format",
             "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"],
            capture_output=True, text=True, timeout=10
        )
        docker_info = docker_cmd.stdout if docker_cmd.returncode == 0 else "Docker apagado o sin permisos."
        return f"=== MEMORIA DEL SISTEMA (Windows) ===\n{ram_info}\n\n=== CONTENEDORES DOCKER ===\n{docker_info}"
    except Exception as e:
        return f"Error al auditar recursos: {str(e)}"


def check_qdrant_vectors() -> str:
    """Verifica si Qdrant responde en localhost:6333 y lista las colecciones."""
    try:
        with httpx.Client(timeout=5.0) as client:
            res = client.get("http://localhost:6333/collections")
            if res.status_code == 200:
                data = res.json()
                colecciones = data.get("result", {}).get("collections", [])
                nombres = [c.get("name", "?") for c in colecciones]
                return (
                    f"Qdrant ONLINE (Puerto 6333)\n"
                    f"Colecciones ({len(nombres)}): {', '.join(nombres) if nombres else 'ninguna aun'}"
                )
            return f"Qdrant respondio con codigo: {res.status_code}"
    except Exception as e:
        return f"Qdrant OFFLINE en localhost:6333.\nDetalle: {str(e)}"


def audit_git_security() -> str:
    """Verifica el estado del repositorio y busca archivos sensibles no ignorados."""
    try:
        git_cmd = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True, text=True, timeout=5
        )
        archivos = git_cmd.stdout.strip()
        lineas = archivos.split("\n") if archivos else []
        peligros = [l for l in lineas if any(ext in l for ext in [".env", ".pem", ".key", ".secret"])]
        alerta = (
            "ALERTA - Archivos sensibles detectados:\n" + "\n".join(peligros)
            if peligros
            else "Sin archivos .env/.pem/.key expuestos en tracking."
        )
        estado = archivos if archivos else "Working tree limpio."
        return f"{alerta}\n\n=== ARCHIVOS MODIFICADOS ===\n{estado}"
    except Exception as e:
        return f"Error ejecutando auditoria Git: {str(e)}"


# ─── Nuevas herramientas de auditoria de CODIGO ──────────────────────────────

def audit_exposed_secrets() -> str:
    """
    Escanea el proyecto en busca de credenciales hardcodeadas en el codigo:
    API keys, tokens, passwords, connection strings.
    Solo lee archivos, no modifica nada.
    """
    # Patrones de secretos comunes en codigo
    PATTERNS = {
        "API Key hardcodeada": re.compile(
            r'(?:api[_-]?key|apikey)\s*[=:]\s*["\']([A-Za-z0-9_\-]{20,})["\']', re.IGNORECASE
        ),
        "Token JWT/Bearer": re.compile(
            r'(?:token|bearer|secret)\s*[=:]\s*["\']([A-Za-z0-9_\-\.]{30,})["\']', re.IGNORECASE
        ),
        "Password hardcodeada": re.compile(
            r'(?:password|passwd|pwd)\s*[=:]\s*["\']([^"\']{6,})["\']', re.IGNORECASE
        ),
        "Supabase URL con key": re.compile(
            r'supabase.*["\']eyJ[A-Za-z0-9_\-\.]+["\']', re.IGNORECASE
        ),
        "Connection string DB": re.compile(
            r'(?:postgresql|mysql|mongodb)\://[^\s"\'>]+', re.IGNORECASE
        ),
        "Google/GCP key": re.compile(
            r'AIza[0-9A-Za-z\-_]{35}', re.IGNORECASE
        ),
    }

    hallazgos = []
    archivos_revisados = 0

    for filepath in _iter_code_files(PROJECT_ROOT):
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            archivos_revisados += 1
            rel_path = filepath.relative_to(PROJECT_ROOT)

            for tipo, patron in PATTERNS.items():
                matches = patron.findall(content)
                if matches:
                    # Encontrar numero de linea
                    for i, line in enumerate(content.splitlines(), 1):
                        if patron.search(line):
                            hallazgos.append(
                                f"  [{tipo}] {rel_path}  (linea {i})"
                            )
                            break
        except Exception:
            continue

    resumen = f"Archivos escaneados: {archivos_revisados}\n"
    if hallazgos:
        return (
            f"ALERTA - Posibles secretos encontrados ({len(hallazgos)}):\n"
            + resumen
            + "\n".join(hallazgos)
        )
    return f"Sin secretos hardcodeados detectados.\n{resumen}"


def audit_broken_python_imports() -> str:
    """
    Analiza todos los archivos .py del proyecto y detecta:
    - Imports que apuntan a modulos inexistentes dentro del proyecto
    - Archivos con errores de sintaxis que no pueden parsear
    Solo lee, no modifica nada.
    """
    errores_sintaxis = []
    imports_rotos = []
    archivos_ok = 0

    # Construir set de modulos internos disponibles
    modulos_internos = set()
    for f in PROJECT_ROOT.rglob("*.py"):
        if any(skip in f.parts for skip in SKIP_DIRS):
            continue
        modulos_internos.add(f.stem)
        modulos_internos.add(f.name)

    for filepath in _iter_code_files(PROJECT_ROOT):
        if filepath.suffix != ".py":
            continue
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            rel_path = filepath.relative_to(PROJECT_ROOT)

            # Parsear AST para detectar errores de sintaxis
            try:
                tree = ast.parse(content)
                archivos_ok += 1

                # Revisar imports relativos que apunten a nada
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        modulo = node.module or ""
                        # Solo revisar imports relativos o del propio proyecto
                        if node.level > 0 or modulo.startswith("agents_core"):
                            partes = modulo.split(".")
                            # Verificar si el archivo existe en el proyecto
                            ruta_esperada = PROJECT_ROOT
                            existe = False
                            for parte in partes:
                                ruta_esperada = ruta_esperada / parte
                                if (ruta_esperada.with_suffix(".py")).exists() or ruta_esperada.is_dir():
                                    existe = True
                                    break
                            if not existe and modulo:
                                imports_rotos.append(
                                    f"  {rel_path} (linea {node.lineno}): 'from {modulo} import ...' -> no encontrado"
                                )

            except SyntaxError as se:
                errores_sintaxis.append(
                    f"  {rel_path} (linea {se.lineno}): {se.msg}"
                )

        except Exception as e:
            errores_sintaxis.append(f"  {filepath.name}: No se pudo leer - {str(e)}")

    lineas = [f"Archivos .py analizados: {archivos_ok + len(errores_sintaxis)}"]

    if errores_sintaxis:
        lineas.append(f"\nERRORES DE SINTAXIS ({len(errores_sintaxis)}):")
        lineas.extend(errores_sintaxis)
    else:
        lineas.append("\nSin errores de sintaxis.")

    if imports_rotos:
        lineas.append(f"\nIMPORTS ROTOS O SOSPECHOSOS ({len(imports_rotos)}):")
        lineas.extend(imports_rotos)
    else:
        lineas.append("Sin imports rotos detectados.")

    return "\n".join(lineas)


def audit_orphan_scripts() -> str:
    """
    Detecta scripts Python en la raiz del proyecto que parecen huerfanos:
    archivos test_*.py, generate_*.py, etc. que probablemente no son parte
    del sistema productivo y generan confusion.
    Solo analiza nombres y tamano, no ejecuta nada.
    """
    PREFIJOS_HUERFANOS = ["test_", "generate_", "inject_", "temp_", "get_", "move_", "setup_", "simulate_"]
    SUFIJOS_SOSPECHOSOS = ["_FIXED.txt", "_output.txt", "_output.md"]

    huerfanos_py  = []
    archivos_temp = []
    archivos_json_sueltos = []

    # Solo revisar la raiz del proyecto (sin recursion profunda)
    for f in PROJECT_ROOT.iterdir():
        if not f.is_file():
            continue
        nombre = f.name
        tamano_kb = f.stat().st_size / 1024

        # Scripts Python huerfanos en raiz
        if f.suffix == ".py":
            if any(nombre.startswith(p) for p in PREFIJOS_HUERFANOS):
                huerfanos_py.append(f"  {nombre} ({tamano_kb:.1f} KB)")

        # Archivos temporales/output sueltos
        if any(nombre.endswith(s) for s in SUFIJOS_SOSPECHOSOS):
            archivos_temp.append(f"  {nombre} ({tamano_kb:.1f} KB)")

        # JSON sensibles sueltos en raiz (credentials, service accounts)
        if f.suffix == ".json" and any(kw in nombre.lower() for kw in ["key", "credential", "service", "secret", "config"]):
            archivos_json_sueltos.append(f"  {nombre} ({tamano_kb:.1f} KB) <- SENSIBLE")

    lineas = ["=== AUDITORIA DE SCRIPTS HUERFANOS Y ARCHIVOS SUELTOS ===\n"]

    lineas.append(f"Scripts Python de utilidad/test en raiz ({len(huerfanos_py)}):")
    lineas.extend(huerfanos_py or ["  Ninguno"])

    lineas.append(f"\nArchivos de output/temp sueltos ({len(archivos_temp)}):")
    lineas.extend(archivos_temp or ["  Ninguno"])

    lineas.append(f"\nJSONs con nombres sensibles en raiz ({len(archivos_json_sueltos)}):")
    lineas.extend(archivos_json_sueltos or ["  Ninguno"])

    return "\n".join(lineas)
