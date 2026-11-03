"""
scripts/promptfoo_provider.py - Conector de MAX AI para Promptfoo
Ejecuta la llamada a process_message de backend/src/max_agent.py
usando el RAG híbrido real (Catálogo Oficial Web + Qdrant 337k vectores).
"""
import sys
import json
import asyncio
from pathlib import Path

# Forzar codificación UTF-8 en stdout y stderr en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT_DIR / "backend" / "src"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

try:
    from backend.src.max_agent import process_message
except ImportError:
    from max_agent import process_message


def call_api(prompt: str, options=None, context=None):
    """
    Función consumida nativamente por Promptfoo como Custom Python Provider.
    """
    try:
        res = asyncio.run(process_message(prompt=prompt))
        mensaje = res.get("mensaje", "")
        return {
            "output": mensaje
        }
    except Exception as e:
        return {
            "error": f"Error ejecutando MAX AI: {str(e)}"
        }


if __name__ == "__main__":
    # Modo CLI para llamadas tipo 'exec:python ...'
    prompt_input = ""
    if len(sys.argv) > 1:
        prompt_input = " ".join(sys.argv[1:])
    else:
        # Si se pasa por stdin
        try:
            prompt_input = sys.stdin.read().strip()
        except Exception:
            pass

    if not prompt_input:
        prompt_input = "¿Cuál es la dificultad de la ruta Salkantay?"

    result = call_api(prompt_input)
    if "output" in result:
        print(result["output"])
    else:
        print(json.dumps(result))
