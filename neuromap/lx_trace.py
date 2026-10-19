"""
LX NeuroMap · SDK de trazas
===========================
Registra, en un archivo JSONL, lo que hace cada agente de Lifextreme:
búsquedas en Qdrant (y qué documentos tocó), llamadas a Ollama (modelo, ms, tokens),
llamadas HTTP, errores y ciclo de vida del agente.

Diseño:
  * Cero dependencias y tolerante a fallos: si algo falla aquí, el agente sigue igual.
  * Cero cambios en los agentes: se activa con `python neuromap/run.py scripts/agent_cfo.py`
    o con una sola línea:  `from neuromap import lx_trace; lx_trace.auto("agent_cfo")`
"""
import atexit
import functools
import inspect
import json
import os
import sys
import threading
import time
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
EVENTS_FILE = os.environ.get("LX_EVENTS_FILE", os.path.join(HERE, "data", "events.jsonl"))

_AGENT = {"name": os.environ.get("LX_AGENT", "desconocido")}
_lock = threading.Lock()
_state = {"patched": False, "started": None}

_OLLAMA = {"/api/generate": "generate", "/api/chat": "chat",
           "/api/embed": "embed", "/api/embeddings": "embed"}
_IGNORE_PORTS = {6333, 6334, 6335, 8765}  # Qdrant y el propio NeuroMap


def emit(kind, **fields):
    """Escribe un evento. Nunca lanza excepciones."""
    try:
        ev = {"t": round(time.time(), 3), "agent": _AGENT["name"],
              "pid": os.getpid(), "kind": kind}
        ev.update({k: v for k, v in fields.items() if v is not None})
        line = (json.dumps(ev, ensure_ascii=False, default=str) + "\n").encode("utf-8")
        os.makedirs(os.path.dirname(EVENTS_FILE), exist_ok=True)
        with _lock:
            fd = os.open(EVENTS_FILE, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0))
            try:
                os.write(fd, line)
            finally:
                os.close(fd)
    except Exception:
        pass


# ───────────────────────── Qdrant ─────────────────────────
def _docs_from(result):
    docs = []
    try:
        points = getattr(result, "points", result) or []
        for p in list(points)[:25]:
            pl = getattr(p, "payload", None) or {}
            src = pl.get("source") or pl.get("title") or pl.get("nombre")
            docs.append({"s": src, "sc": round(float(getattr(p, "score", 0) or 0), 3)})
    except Exception:
        pass
    return docs


def _collection_of(a, k):
    c = k.get("collection_name")
    if c is None and a and isinstance(a[0], str):
        c = a[0]
    return c


def _wrap_qdrant(fn, op):
    if inspect.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def aw(self, *a, **k):
            t0 = time.time()
            try:
                r = await fn(self, *a, **k)
            except Exception as e:
                emit("error", where="qdrant." + op, msg=str(e)[:200])
                raise
            _log_qdrant(op, a, k, r, t0)
            return r
        return aw

    @functools.wraps(fn)
    def w(self, *a, **k):
        t0 = time.time()
        try:
            r = fn(self, *a, **k)
        except Exception as e:
            emit("error", where="qdrant." + op, msg=str(e)[:200])
            raise
        _log_qdrant(op, a, k, r, t0)
        return r
    return w


def _log_qdrant(op, a, k, r, t0):
    ms = int((time.time() - t0) * 1000)
    coll = _collection_of(a, k)
    if op == "upsert":
        pts = k.get("points") if "points" in k else (a[1] if len(a) > 1 else [])
        try:
            n = len(pts)
        except Exception:
            n = None
        emit("qdrant_write", collection=coll, n=n, ms=ms)
    else:
        emit("qdrant_search", collection=coll, op=op, ms=ms, docs=_docs_from(r))


def _patch_qdrant():
    try:
        import qdrant_client
    except Exception:
        return
    for cls_name in ("QdrantClient", "AsyncQdrantClient"):
        cls = getattr(qdrant_client, cls_name, None)
        if cls is None:
            continue
        for op in ("query_points", "search", "upsert"):
            fn = getattr(cls, op, None)
            if fn is not None and not getattr(fn, "_lx", False):
                wrapped = _wrap_qdrant(fn, op)
                wrapped._lx = True
                setattr(cls, op, wrapped)


# ───────────────────────── HTTP / Ollama ─────────────────────────
def _log_http(url, method, body, status, ms, resp_json):
    try:
        u = urlparse(str(url))
        if u.port in _IGNORE_PORTS:
            return
        op = _OLLAMA.get(u.path)
        if op and (u.port == 11434 or "ollama" in (u.hostname or "")):
            model = None
            if isinstance(body, dict):
                model = body.get("model")
            tokens = None
            if isinstance(resp_json, dict):
                tokens = (resp_json.get("prompt_eval_count") or 0) + (resp_json.get("eval_count") or 0) or None
            emit("llm_call", op=op, model=model, ms=ms, tokens=tokens, status=status)
        else:
            emit("http", host=u.hostname, path=u.path[:80], method=method, status=status, ms=ms)
    except Exception:
        pass


def _json_or_none(resp, streamed):
    if streamed:
        return None
    try:
        return resp.json()
    except Exception:
        return None


def _patch_requests():
    try:
        import requests.sessions as rs
    except Exception:
        return
    orig = rs.Session.request
    if getattr(orig, "_lx", False):
        return

    @functools.wraps(orig)
    def request(self, method, url, *a, **k):
        t0 = time.time()
        try:
            resp = orig(self, method, url, *a, **k)
        except Exception as e:
            emit("error", where="http", msg=str(e)[:200], url=str(url)[:120])
            raise
        _log_http(url, method, k.get("json"), resp.status_code,
                  int((time.time() - t0) * 1000), _json_or_none(resp, k.get("stream")))
        return resp
    request._lx = True
    rs.Session.request = request


def _patch_httpx():
    try:
        import httpx
    except Exception:
        return

    def body_json(req):
        try:
            return json.loads(req.content.decode("utf-8"))
        except Exception:
            return None

    orig_s = httpx.Client.send
    if not getattr(orig_s, "_lx", False):
        @functools.wraps(orig_s)
        def send(self, request, *a, **k):
            t0 = time.time()
            resp = orig_s(self, request, *a, **k)
            try:
                if request.url.port not in _IGNORE_PORTS:
                    _log_http(request.url, request.method, body_json(request), resp.status_code,
                              int((time.time() - t0) * 1000), _json_or_none(resp, k.get("stream")))
            except Exception:
                pass
            return resp
        send._lx = True
        httpx.Client.send = send

    orig_a = httpx.AsyncClient.send
    if not getattr(orig_a, "_lx", False):
        @functools.wraps(orig_a)
        async def asend(self, request, *a, **k):
            t0 = time.time()
            resp = await orig_a(self, request, *a, **k)
            try:
                if request.url.port not in _IGNORE_PORTS:
                    _log_http(request.url, request.method, body_json(request), resp.status_code,
                              int((time.time() - t0) * 1000), _json_or_none(resp, k.get("stream")))
            except Exception:
                pass
            return resp
        asend._lx = True
        httpx.AsyncClient.send = asend


# ───────────────────────── Ciclo de vida ─────────────────────────
def auto(name=None):
    """Activa la traza para este proceso. Idempotente."""
    if _state["patched"]:
        return
    try:
        if name:
            _AGENT["name"] = name
        _state["patched"] = True
        _state["started"] = time.time()
        _patch_qdrant()
        _patch_requests()
        _patch_httpx()
        emit("agent_start", argv=sys.argv[1:6])

        prev_hook = sys.excepthook

        def hook(tp, val, tb):
            emit("error", where="crash", msg="%s: %s" % (tp.__name__, str(val)[:200]))
            prev_hook(tp, val, tb)
        sys.excepthook = hook

        def bye():
            emit("agent_end", seconds=round(time.time() - _state["started"], 1))
        atexit.register(bye)
    except Exception:
        pass
