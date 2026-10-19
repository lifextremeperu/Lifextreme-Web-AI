"""
LX NeuroMap · Servidor (solo biblioteca estándar, sin instalar nada)
Uso:  .venv\\Scripts\\python.exe neuromap/server.py      →  http://localhost:8765
"""
import json
import mimetypes
import os
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from neuromap import engine  # noqa: E402
from neuromap import lx_trace  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, "web")
PORT = int(os.environ.get("NEUROMAP_PORT", "8765"))
QDRANT = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
OLLAMA = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
MAIN = "Lifextreme_Knowledge"

_brain = {"mtime": 0, "data": {}, "index": {}}


def brain():
    try:
        m = os.path.getmtime(engine.BRAIN_FILE)
    except OSError:
        return {}
    if m != _brain["mtime"]:
        _brain["data"] = engine.load_json(engine.BRAIN_FILE, {})
        _brain["index"] = {(n["c"], n["s"]): i for i, n in enumerate(_brain["data"].get("nodes", []))}
        _brain["mtime"] = m
    return _brain["data"]


def post_json(url, payload, timeout=60):
    req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def semantic_search(q, limit=40):
    """Embebe la consulta con Ollama y busca en Qdrant. Devuelve índices de neuronas."""
    brain()
    emb = post_json(OLLAMA + "/api/embeddings", {"model": "nomic-embed-text", "prompt": q})["embedding"]
    res = post_json("%s/collections/%s/points/query" % (QDRANT, MAIN),
                    {"query": emb, "limit": limit, "with_payload": ["source"]})["result"]["points"]
    seen, hits = set(), []
    for p in res:
        src = (p.get("payload") or {}).get("source")
        i = _brain["index"].get((MAIN, src))
        if i is not None and i not in seen:
            seen.add(i)
            hits.append({"i": i, "s": src, "sc": round(p.get("score", 0), 3)})
    lx_trace._AGENT["name"] = "buscador"
    lx_trace.emit("qdrant_search", collection=MAIN, op="query", ms=0, query=q[:120],
                  docs=[{"s": h["s"], "sc": h["sc"]} for h in hits])
    return hits


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == "/api/brain":
                return self._send(200, brain() or {"nodes": []})
            if u.path == "/api/agents":
                cat = engine.load_json(engine.AGENTS_FILE, [])
                st = engine.agent_stats()
                known = {a["id"] for a in cat}
                for k in st:
                    if k not in known:
                        cat.append({"id": k, "label": k, "icon": "··", "color": "#8a93a6", "impact": "-", "role": "", "note": ""})
                for a in cat:
                    a["stats"] = st.get(a["id"], {})
                return self._send(200, cat)
            if u.path == "/api/recent":
                secs = float(q.get("seconds", ["600"])[0])
                return self._send(200, engine.read_events(since=time.time() - secs, max_events=3000))
            if u.path == "/api/learned":
                return self._send(200, engine.learned(brain()))
            if u.path == "/api/doctor":
                return self._send(200, engine.doctor(brain()))
            if u.path == "/api/search":
                text = (q.get("q", [""])[0]).strip()
                if not text:
                    return self._send(400, {"error": "Falta q"})
                try:
                    return self._send(200, {"hits": semantic_search(text)})
                except Exception as e:
                    return self._send(502, {"error": "Búsqueda no disponible (¿Ollama/Qdrant encendidos?): %s" % e})
            if u.path == "/api/stream":
                return self._stream()
            path = "index.html" if u.path in ("/", "") else u.path.lstrip("/")
            full = os.path.normpath(os.path.join(WEB, path))
            if not full.startswith(WEB) or not os.path.isfile(full):
                return self._send(404, {"error": "no encontrado"})
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
            with open(full, "rb") as f:
                return self._send(200, f.read(), ctype + ("; charset=utf-8" if ctype.startswith("text") or "javascript" in ctype else ""))
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:
            try:
                self._send(500, {"error": str(e)})
            except Exception:
                pass

    def _stream(self):
        """Server-Sent Events: sigue el final de events.jsonl en vivo."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        os.makedirs(os.path.dirname(engine.EVENTS_FILE), exist_ok=True)
        open(engine.EVENTS_FILE, "a").close()
        f = open(engine.EVENTS_FILE, "r", encoding="utf-8", errors="replace")
        f.seek(0, os.SEEK_END)
        last_ping = time.time()
        try:
            while True:
                line = f.readline()
                if line:
                    if line.endswith("\n"):
                        self.wfile.write(("data: " + line.strip() + "\n\n").encode("utf-8"))
                        self.wfile.flush()
                else:
                    time.sleep(0.25)
                    if time.time() - last_ping > 15:
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
                        last_ping = time.time()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            f.close()


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    srv.daemon_threads = True
    print("LX NeuroMap en http://localhost:%d" % PORT)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
