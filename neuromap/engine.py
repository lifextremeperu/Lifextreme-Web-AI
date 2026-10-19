"""
LX NeuroMap · Motor
===================
 * Lectura del registro de eventos (events.jsonl)
 * Aprendizaje: lo que se usa junto se conecta y lo que no se repite se olvida
   (vida media de 14 días, igual que Neuromapa)
 * Médico del RAG: revisa la salud del cerebro y de los agentes
 * Freno: alerta cuando un agente gasta demasiadas llamadas o tokens por hora
"""
import json
import os
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.environ.get("LX_EVENTS_FILE", os.path.join(HERE, "data", "events.jsonl"))
BRAIN_FILE = os.path.join(HERE, "data", "brain.json")
AGENTS_FILE = os.path.join(HERE, "agents.json")

HALF_LIFE_DAYS = 14.0
LIMITE_TOKENS_HORA = int(os.environ.get("LX_LIMIT_TOKENS_HOUR", "200000"))
LIMITE_LLAMADAS_HORA = int(os.environ.get("LX_LIMIT_CALLS_HOUR", "300"))


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def read_events(since=0.0, max_events=200000):
    out = []
    try:
        with open(EVENTS_FILE, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                if ev.get("t", 0) >= since:
                    out.append(ev)
        return out[-max_events:]
    except FileNotFoundError:
        return []


def decay(age_seconds):
    return 0.5 ** (age_seconds / (HALF_LIFE_DAYS * 86400.0))


# ───────────────────────── Aprendizaje ─────────────────────────
def learned(brain, top=60):
    """Conexiones aprendidas: (agente → documento) y (documento ↔ documento que aparecen juntos)."""
    index = {(n["c"], n["s"]): i for i, n in enumerate(brain.get("nodes", []))}
    now = time.time()
    ad = defaultdict(float)     # (agente, nodo) -> peso
    dd = defaultdict(float)     # (nodo, nodo) -> peso
    searches = 0
    for ev in read_events():
        if ev.get("kind") != "qdrant_search":
            continue
        searches += 1
        w = decay(now - ev.get("t", now))
        ids = []
        for d in ev.get("docs", []):
            i = index.get((ev.get("collection"), d.get("s")))
            if i is not None:
                ids.append(i)
                ad[(ev["agent"], i)] += w
        ids = sorted(set(ids))[:8]
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                dd[(ids[a], ids[b])] += w
    agent_doc = sorted(ad.items(), key=lambda kv: -kv[1])[:top]
    doc_doc = sorted(dd.items(), key=lambda kv: -kv[1])[:top]
    return {
        "searches": searches,
        "agent_doc": [{"agent": a, "n": n, "w": round(w, 3)} for (a, n), w in agent_doc],
        "doc_doc": [{"a": a, "b": b, "w": round(w, 3)} for (a, b), w in doc_doc],
    }


def consulted_docs(brain):
    index = {(n["c"], n["s"]): i for i, n in enumerate(brain.get("nodes", []))}
    seen, searches = set(), 0
    for ev in read_events():
        if ev.get("kind") == "qdrant_search":
            searches += 1
            for d in ev.get("docs", []):
                i = index.get((ev.get("collection"), d.get("s")))
                if i is not None:
                    seen.add(i)
    return seen, searches


# ───────────────────────── Estadísticas por agente ─────────────────────────
def agent_stats():
    now = time.time()
    st = defaultdict(lambda: {"calls": 0, "searches": 0, "tokens_h": 0, "calls_h": 0, "errors_24h": 0,
                              "last": 0, "runs": 0, "docs": 0, "demo": False})
    for ev in read_events(since=now - 86400):
        s = st[ev.get("agent", "?")]
        s["last"] = max(s["last"], ev.get("t", 0))
        if ev.get("demo"):
            s["demo"] = True
        k = ev.get("kind")
        recent = now - ev.get("t", 0) <= 3600
        if k == "agent_start":
            s["runs"] += 1
        elif k == "llm_call":
            s["calls"] += 1
            if recent:
                s["calls_h"] += 1
                s["tokens_h"] += ev.get("tokens") or 0
        elif k == "qdrant_search":
            s["searches"] += 1
            s["docs"] += len(ev.get("docs", []))
        elif k == "error":
            s["errors_24h"] += 1
    return st


# ───────────────────────── Médico del RAG ─────────────────────────
def doctor(brain):
    issues = []

    def add(level, title, detail):
        issues.append({"level": level, "title": title, "detail": detail})

    stats = brain.get("stats", {})
    if not brain.get("nodes"):
        add("alto", "El cerebro aún no está indexado", "Ejecuta: .venv\\Scripts\\python.exe neuromap\\indexer.py")
        return {"issues": issues, "score": 0}

    empty = stats.get("empty_collections", [])
    if empty:
        add("medio", "%d colecciones vacías" % len(empty),
            "Creadas pero sin conocimiento: " + ", ".join(empty) + ". Los agentes que dependen de ellas no tienen memoria.")

    missing = sum(n.get("m", 0) for n in brain["nodes"])
    if missing:
        add("medio", "%d fragmentos sin 'source'" % missing,
            "Sin fuente no se puede citar ni auditar de dónde sale la respuesta.")

    dups = brain.get("dups", [])
    if dups:
        ej = []
        for a, b, s in dups[:3]:
            ej.append("%s ≈ %s (%.0f%%)" % (brain["nodes"][a]["s"][:34], brain["nodes"][b]["s"][:34], s * 100))
        add("bajo", "%d posibles documentos duplicados" % len(dups),
            "Ocupan espacio y sesgan los resultados. Ej.: " + " · ".join(ej))

    seen, searches = consulted_docs(brain)
    total = len(brain["nodes"])
    if searches >= 20:
        pct = 100.0 * len(seen) / total
        add("bajo", "Conocimiento sin uso", "Solo %.1f%% de los documentos se ha consultado en %d búsquedas registradas." % (pct, searches))
    else:
        add("info", "Historial corto", "Hay %d búsquedas registradas; con 20 o más el médico detecta conocimiento que nadie consulta." % searches)

    cat = load_json(AGENTS_FILE, [])
    st = agent_stats()
    now = time.time()
    for a in cat:
        s = st.get(a["id"])
        if not s:
            add("info", "%s sin actividad registrada" % a["label"], "No se ha ejecutado con trazas en las últimas 24 h.")
            continue
        if s["errors_24h"]:
            add("alto", "%s con %d errores (24 h)" % (a["label"], s["errors_24h"]), "Revisa el panel de eventos.")
        if s["tokens_h"] > LIMITE_TOKENS_HORA or s["calls_h"] > LIMITE_LLAMADAS_HORA:
            add("alto", "Freno: %s gasta mucho" % a["label"],
                "%d llamadas y %d tokens en la última hora (límite %d llamadas / %d tokens)." %
                (s["calls_h"], s["tokens_h"], LIMITE_LLAMADAS_HORA, LIMITE_TOKENS_HORA))
        if a.get("note"):
            add("info", "%s: nota de estado" % a["label"], a["note"])

    weight = {"alto": 15, "medio": 7, "bajo": 3, "info": 0}
    score = max(0, 100 - sum(weight[i["level"]] for i in issues))
    order = {"alto": 0, "medio": 1, "bajo": 2, "info": 3}
    issues.sort(key=lambda i: order[i["level"]])
    return {"issues": issues, "score": score}
