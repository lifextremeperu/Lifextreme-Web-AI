# LX NeuroMap

El cerebro vivo de Lifextreme: dibuja Qdrant (un punto por documento) y muestra en tiempo real
qué documentos consultan los agentes de inteligencia de negocios.

## Uso rápido
1. Enciende Docker (Qdrant) y Ollama.
2. Doble clic en `abrir-cerebro.bat` (indexa la primera vez y abre http://localhost:8765).
3. Para el video: `.venv\Scripts\python.exe neuromap\demo.py` (consultas reales, agentes simulados).
4. Para trazar un agente real: `.venv\Scripts\python.exe neuromap\run.py scripts\agent_cfo.py`

Reindexar tras ingestar documentos nuevos: `.venv\Scripts\python.exe neuromap\indexer.py`

## Piezas
| Archivo | Función |
|---|---|
| `lx_trace.py` | Registra búsquedas en Qdrant, llamadas a Ollama y errores (sin tocar los agentes) |
| `run.py` | Lanza cualquier script con trazas |
| `indexer.py` | Qdrant → `data/brain.json` (neuronas, sinapsis, duplicados) |
| `engine.py` | Aprendizaje (vida media 14 días), médico del RAG, freno de gasto |
| `server.py` | Servidor local con eventos en vivo (sin dependencias) |
| `web/` | Visor |
| `agents.json` | Agentes de BI monitoreados |

Los eventos viven en `data/events.jsonl`. Los datos son locales y no se publican.
