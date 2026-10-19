"""
Lanzador con trazas:   python neuromap/run.py scripts/agent_cfo.py [argumentos...]

Ejecuta el agente tal cual, pero registrando en NeuroMap sus búsquedas en Qdrant,
llamadas a Ollama y errores. No requiere modificar el script del agente.
"""
import os
import pathlib
import runpy
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main():
    if len(sys.argv) < 2:
        print("Uso: python neuromap/run.py <script_del_agente.py> [args...]")
        return 2
    script = pathlib.Path(sys.argv[1]).resolve()
    if not script.exists():
        print("No existe:", script)
        return 2
    os.environ["LX_AGENT"] = script.stem
    from neuromap import lx_trace
    lx_trace.auto(script.stem)
    sys.argv = [str(script)] + sys.argv[2:]
    sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    sys.exit(main())
