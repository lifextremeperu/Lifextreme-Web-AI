import os, json, time, random, requests, feedparser
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'news'))
os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------------------------------------------
# Lista de feeds RSS (puedes ampliar con más fuentes)
# ---------------------------------------------------------------
FEEDS = {
    "chile": "https://www.sernatur.cl/rss/noticias.xml",
    "argentina": "https://www.argentina.gob.ar/api/ministerio/turismo/rss",
    "colombia": "https://www.mincit.gov.co/rss/turismo",
    # agrega más países si lo deseas
}

PROMPT = """Eres un analista de turismo y gestión de riesgos.
¿El siguiente texto contiene información estratégica (plan, infraestructura, evento, alerta) de turismo? Responde SOLO con SI o NO.
Texto:\n"""

def phi3_evaluar(texto: str) -> bool:
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3:latest", "prompt": PROMPT + texto, "stream": False},
            timeout=15,
        )
        if r.status_code == 200:
            return "SI" in r.json().get("response", "").upper()
    except Exception:
        pass
    return False

def cargar_historial(pais):
    path = os.path.join(BASE_DIR, f"historial_{pais}.json")
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else []

def guardar_historial(pais, hist):
    path = os.path.join(BASE_DIR, f"historial_{pais}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def main():
    print("=== INICIO AGENTE RSS/API ===")
    for pais, url in FEEDS.items():
        print(f"\n--- Procesando {pais.upper()} ---")
        historial = cargar_historial(pais)
        ya_vistos = {h["link"] for h in historial}
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if entry.link in ya_vistos:
                continue
            texto = f"{entry.title}\n{entry.summary}"
            if phi3_evaluar(texto):
                print(f"[✓] RELEVANTE: {entry.title[:60]}")
                registro = {
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.summary,
                    "published": entry.get("published", datetime.utcnow().isoformat()),
                    "pais": pais,
                }
                historial.append(registro)
            else:
                print(f"[✗] NO RELEVANTE: {entry.title[:60]}")
            time.sleep(random.randint(5, 10))  # pausa anti‑bloqueo
        guardar_historial(pais, historial)
        time.sleep(30)  # pausa entre países
    print("=== AGENTE RSS/API FINALIZADO ===")

if __name__ == "__main__":
    main()
