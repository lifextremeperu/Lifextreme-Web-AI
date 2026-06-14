import os, time, random, requests, json
from bs4 import BeautifulSoup
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'guides'))
os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------------------------------------------
# Lista de sitios de guías (ejemplo: LonelyPlanet, TripAdvisor)
# ---------------------------------------------------------------
GUIDE_SITES = {
    "lonelyplanet": {
        "base": "https://www.lonelyplanet.com/",
        "countries": ["argentina", "chile", "colombia", "brazil", "bolivia", "ecuador"],
        "path": lambda c: f"{c}/"  # simplificado – en producción deberías apuntar a secciones específicas
    },
    "tripadvisor": {
        "base": "https://www.tripadvisor.com/",
        "countries": ["Argentina", "Chile", "Colombia", "Brazil", "Bolivia", "Ecuador"],
        "path": lambda c: f"Attractions-g{c}-Activities.html"  # placeholder
    }
}

# Blogs y páginas especializadas por país
BLOG_SITES = {
    "chile": [
        "https://chile.travel/blog/",
        "https://www.turismochile.com/blog/"
    ],
    "argentina": [
        "https://argentinaturismo.com/blog/",
        "https://www.turismoroyal.com/blog"
    ],
    "colombia": [
        "https://colombia.travel/blog/",
        "https://www.visita.co/blog"
    ],
    "brazil": [
        "https://visitbrasil.com/blog/",
        "https://www.brasiltravels.com/blog"
    ],
    "bolivia": [
        "https://boliviatourism.com/blog/",
        "https://www.turismobolivia.com/blog"
    ],
    "ecuador": [
        "https://ecuador.travel/blog/",
        "https://www.turismoec.com/blog"
    ]
}

PROMPT = """Eres un analista de turismo y gestión de riesgos.
¿El siguiente fragmento describe una atracción, infraestructura o evento turístico de valor estratégico? Responde SOLO con SI o NO.
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

def cargar_historial(site, pais):
    path = os.path.join(BASE_DIR, f"historial_{site}_{pais}.json")
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else []

def guardar_historial(site, pais, hist):
    path = os.path.join(BASE_DIR, f"historial_{site}_{pais}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def extraer_atracciones(url):
    try:
        r = requests.get(url, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Buscamos bloques típicos de título y descripción
        items = []
        for card in soup.select('h2, h3, .listing-title, .title'):
            title = card.get_text(strip=True)
            # Intentamos obtener descripción cercana
            parent = card.parent
            desc = parent.get_text(separator=' ', strip=True).replace(title, '')
            items.append((title, desc))
        return items
    except Exception as e:
        print(f"[⚠️] error al leer {url}: {e}")
        return []

def main():
    print("=== INICIO SCRAPING GUÍAS TURÍSTICAS ===")
    for site, cfg in GUIDE_SITES.items():
        base = cfg["base"]
        for pais in cfg["countries"]:
            pais_key = pais.lower().replace(" ", "_")
            historial = cargar_historial(site, pais_key)
            ya_vistos = {h["url"] for h in historial}
            url = base + cfg["path"](pais.lower())
            # Verificar que la URL esté accesible antes de extraer
            try:
                head = requests.head(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                head.raise_for_status()
                reachable = True
            except Exception as e:
                print(f"[⚠️] URL no accesible {url}: {e}")
                reachable = False
            if not reachable:
                continue
            print(f"\n--- {site.upper()} – {pais.upper()} -> {url}")
            items = extraer_atracciones(url)
            for title, desc in items:
                full_text = f"{title}\n{desc}"
                if phi3_evaluar(full_text):
                    if url in ya_vistos:
                        continue
                    registro = {
                        "site": site,
                        "pais": pais,
                        "title": title,
                        "description": desc,
                        "url": url,
                        "fecha": datetime.utcnow().isoformat(),
                    }
                    historial.append(registro)
                    print(f"[✓] RELEVANTE: {title[:60]}")
                else:
                    print(f"[✗] NO RELEVANTE: {title[:60]}")
                time.sleep(random.randint(5, 10))
            guardar_historial(site, pais_key, historial)
            time.sleep(30)  # pausa entre países
            # Enviar reporte a Telegram al completar el país
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            if bot_token and chat_id:
                msg = f"✅ Scraping completado para {pais.upper()} ({site.upper()})"
                try:
                    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": msg})
                except Exception as e:
                    print(f"[WARN] No se pudo enviar Telegram: {e}")
    print("=== SCRAPING GUÍAS FINALIZADO ===")

    # ---------------------------------------------------------------
    # Procesar blogs y páginas especializadas por país
    # ---------------------------------------------------------------
    print("\n=== INICIO SCRAPING BLOGS ESPECIALIZADOS ===")
    for pais, urls in BLOG_SITES.items():
        historial_blog = cargar_historial("blogs", pais)
        ya_vistos_blog = {h["url"] for h in historial_blog}
        print(f"\n--- Procesando blogs de {pais.upper()} ---")
        for url in urls:
            if url in ya_vistos_blog:
                print(f"[✔] Blog ya procesado: {url}")
                continue
            print(f"[▶] Scrapeando blog: {url}")
            items = extraer_atracciones(url)
            for title, desc in items:
                full_text = f"{title}\n{desc}"
                if phi3_evaluar(full_text):
                    registro = {
                        "site": "blog",
                        "pais": pais,
                        "title": title,
                        "description": desc,
                        "url": url,
                        "fecha": datetime.utcnow().isoformat(),
                    }
                    historial_blog.append(registro)
                    print(f"[✓] Blog RELEVANTE: {title[:60]}")
                else:
                    print(f"[✗] Blog NO RELEVANTE: {title[:60]}")
                time.sleep(random.randint(5, 10))
            # marcar blog como procesado
            ya_vistos_blog.add(url)
            time.sleep(30)
        guardar_historial("blogs", pais, historial_blog)
    print("=== SCRAPING BLOGS FINALIZADO ===")

    if __name__ == "__main__":
        main()
    main()
