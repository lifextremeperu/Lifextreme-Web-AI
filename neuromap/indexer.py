"""
LX NeuroMap · Indexador
=======================
Recorre Qdrant y construye el "cerebro": una neurona por documento (no por fragmento),
posicionada por significado (PCA sobre el vector del documento) y unida a sus vecinos
semánticos más cercanos. Guarda el resultado en neuromap/data/brain.json.

Uso:  .venv\\Scripts\\python.exe neuromap/indexer.py
"""
import json
import os
import sys
import time
from collections import defaultdict

import numpy as np
from qdrant_client import QdrantClient

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "brain.json")
QDRANT_URL = os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")
MAIN = "Lifextreme_Knowledge"
KNN = 2           # vecinos por neurona
MIN_SIM = 0.62    # similitud mínima para dibujar una sinapsis
DUP_SIM = 0.985   # umbral de posible duplicado

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def scan_collection(client, name):
    """source -> {type, area, chunks, first_id}"""
    docs = {}
    off = None
    n = 0
    t0 = time.time()
    while True:
        pts, off = client.scroll(name, limit=5000, offset=off, with_payload=["source", "type", "area"],
                                 with_vectors=False)
        for p in pts:
            pl = p.payload or {}
            src = str(pl.get("source") or "(sin fuente)")
            d = docs.get(src)
            if d is None:
                docs[src] = {"type": str(pl.get("type") or "otro"), "area": str(pl.get("area") or "general"),
                             "chunks": 1, "id": p.id, "missing": 0 if pl.get("source") else 1}
            else:
                d["chunks"] += 1
        n += len(pts)
        if n % 50000 < 5000:
            print("   %s: %d puntos (%.0fs)" % (name, n, time.time() - t0))
        if off is None:
            break
    return docs, n


def fetch_vectors(client, name, ids):
    out = {}
    for i in range(0, len(ids), 256):
        batch = ids[i:i + 256]
        for r in client.retrieve(name, ids=batch, with_vectors=True, with_payload=False):
            v = r.vector
            if isinstance(v, dict):
                v = next(iter(v.values()))
            out[r.id] = v
    return out


def main():
    client = QdrantClient(url=QDRANT_URL, timeout=120)
    cols = [c.name for c in client.get_collections().collections]
    print("Colecciones:", cols)

    summary, nodes, vecs = [], [], []
    for cname in cols:
        cnt = client.count(cname, exact=True).count
        info = client.get_collection(cname)
        summary.append({"name": cname, "points": cnt})
        if cnt == 0:
            continue
        print("Escaneando", cname, cnt)
        docs, total = scan_collection(client, cname)
        ids = [d["id"] for d in docs.values()]
        vmap = fetch_vectors(client, cname, ids)
        for src, d in docs.items():
            v = vmap.get(d["id"])
            if v is None:
                continue
            nodes.append({"s": src, "c": cname, "t": d["type"], "a": d["area"], "n": d["chunks"], "m": d["missing"]})
            vecs.append(np.asarray(v, dtype=np.float32))
        print("  -> %d documentos" % len(docs))

    X = np.vstack(vecs)
    X /= (np.linalg.norm(X, axis=1, keepdims=True) + 1e-9)
    N = len(nodes)
    print("Total neuronas:", N)

    # Posiciones: PCA -> disco uniforme por rango radial (llena la forma, conserva vecindad angular)
    Xc = X - X.mean(axis=0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    P = Xc @ Vt[:3].T
    ang = np.arctan2(P[:, 1], P[:, 0])
    r = np.hypot(P[:, 0], P[:, 1])
    rank = r.argsort().argsort() / max(N - 1, 1)
    rr = np.sqrt(rank) * 0.96
    # forma de cerebro: elipse ligeramente achatada
    px, py = np.cos(ang) * rr * 1.18, np.sin(ang) * rr * 0.86
    pz = (P[:, 2] - P[:, 2].mean()) / (P[:, 2].std() + 1e-9)
    pz = np.clip(pz / 3, -1, 1)

    # kNN por bloques
    edges, dups = {}, []
    B = 512
    for i in range(0, N, B):
        sim = X[i:i + B] @ X.T
        for k in range(sim.shape[0]):
            sim[k, i + k] = -1
        idx = np.argpartition(-sim, KNN, axis=1)[:, :KNN]
        for k in range(sim.shape[0]):
            a = i + k
            for b in idx[k]:
                s = float(sim[k, b])
                if s >= DUP_SIM and a < b:
                    dups.append([a, int(b), round(s, 4)])
                if s >= MIN_SIM:
                    key = (min(a, int(b)), max(a, int(b)))
                    edges[key] = max(edges.get(key, 0), s)
    elist = [[a, b, round(w, 3)] for (a, b), w in edges.items()]
    print("Sinapsis:", len(elist), "· posibles duplicados:", len(dups))

    for i, nd in enumerate(nodes):
        nd["x"], nd["y"], nd["z"] = round(float(px[i]), 4), round(float(py[i]), 4), round(float(pz[i]), 3)

    by_type = defaultdict(int)
    for nd in nodes:
        by_type[nd["t"]] += 1
    brain = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "collections": summary,
        "nodes": nodes,
        "edges": elist,
        "dups": dups[:400],
        "types": sorted(by_type.items(), key=lambda kv: -kv[1]),
        "stats": {"neurons": N, "synapses": len(elist),
                  "vectors": sum(c["points"] for c in summary),
                  "empty_collections": [c["name"] for c in summary if c["points"] == 0]},
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(brain, f, ensure_ascii=False, separators=(",", ":"))
    print("Guardado:", OUT, "(%.1f MB)" % (os.path.getsize(OUT) / 1e6))


if __name__ == "__main__":
    main()
