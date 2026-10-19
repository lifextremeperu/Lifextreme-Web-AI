"""
LX NeuroMap · Demo para grabar video
====================================
Las CONSULTAS son reales: cada paso embebe el texto con Ollama (nomic-embed-text) y busca en
Qdrant (Lifextreme_Knowledge), así que los documentos que se iluminan son los verdaderos.
Lo SIMULADO es solo el disparo de los agentes (no se ejecutan sus scripts, para no enviar
mensajes ni escribir datos). Todos los eventos llevan la marca demo=true y el visor lo indica.

Uso:  .venv\\Scripts\\python.exe neuromap\\demo.py [--loops 2] [--fast]
"""
import argparse
import json
import os
import random
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neuromap import lx_trace as T  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

QDRANT = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
OLLAMA = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
COLL = "Lifextreme_Knowledge"

GUION = {
    "agent_cfo": ["IGV exportación de servicios turísticos SUNAT", "margen de utilidad y costos de operación de tours",
                  "flujo de caja y capital de trabajo para agencias de viajes"],
    "agent_b2b_outreach": ["agencias de viajes operadores turísticos Cusco alianzas", "tendencias del turismo de aventura en Perú",
                           "propuesta de valor logística para agencias"],
    "agent_pyme_advisor": ["formalización de pymes turísticas licencias y registro", "normas de seguridad en turismo de aventura",
                           "buenas prácticas de atención al viajero extranjero"],
    "quantum_timesfm_pricing": ["estacionalidad temporada alta turismo Cusco", "precios dinámicos y demanda de tours",
                                "afluencia de visitantes Machu Picchu aforo"],
    "agent_intel": ["competencia agencias de turismo online", "estrategias de marketing digital para turismo",
                    "comportamiento del consumidor viajero"],
    "b2b_financial_agent": ["estados financieros y rentabilidad empresas de turismo", "financiamiento y fondos para pymes de turismo"],
}


def post(url, payload, timeout=60):
    req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def paso(agent, query, pausa):
    T._AGENT["name"] = agent
    t0 = time.time()
    emb = post(OLLAMA + "/api/embeddings", {"model": "nomic-embed-text", "prompt": query})["embedding"]
    T.emit("llm_call", op="embed", model="nomic-embed-text", ms=int((time.time() - t0) * 1000), tokens=len(query.split()), demo=True)
    t1 = time.time()
    pts = post("%s/collections/%s/points/query" % (QDRANT, COLL),
               {"query": emb, "limit": 14, "with_payload": ["source"]})["result"]["points"]
    docs, seen = [], set()
    for p in pts:
        s = (p.get("payload") or {}).get("source")
        if s and s not in seen:
            seen.add(s)
            docs.append({"s": s, "sc": round(p.get("score", 0), 3)})
    T.emit("qdrant_search", collection=COLL, op="query_points", ms=int((time.time() - t1) * 1000),
           query=query, docs=docs, demo=True)
    print("  %-26s %-58s %2d docs" % (agent, query[:58], len(docs)))
    time.sleep(pausa)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loops", type=int, default=1)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    pausa = 0.8 if a.fast else 2.2
    print("Demo de NeuroMap: consultas reales a Qdrant, agentes simulados.\n")
    for _ in range(a.loops):
        orden = list(GUION)
        random.shuffle(orden)
        for ag in orden:
            T._AGENT["name"] = ag
            T.emit("agent_start", demo=True)
            for q in GUION[ag]:
                paso(ag, q, pausa)
            T._AGENT["name"] = ag
            T.emit("agent_end", seconds=round(len(GUION[ag]) * pausa, 1), demo=True)
            time.sleep(pausa / 2)
    print("\nListo.")


if __name__ == "__main__":
    main()
