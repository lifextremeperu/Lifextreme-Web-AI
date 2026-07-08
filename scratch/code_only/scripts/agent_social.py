import os, time, random, requests, json
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'social'))
os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Configuración de la API de Twitter (X) – token en variable de entorno
# ---------------------------------------------------------------------------
BEARER_TOKEN = os.getenv('TWITTER_BEARER')
if not BEARER_TOKEN:
    # Si no hay token, simplemente omitimos la fase social y registramos la condición.
    print('[⚠️] TWITTER_BEARER no está configurado – se omitirá la recolección de datos sociales.')
    BEARER_TOKEN = None
    HEADERS = {}
else:
    HEADERS = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'User-Agent': 'LifextremeBot/1.0',
    }

# Hashtags por país (puedes ampliarlos)
HASHTAGS = {
    'chile': '#TurismoChile',
    'argentina': '#VisitArgentina',
    'colombia': '#TurismoColombia',
    'brasil': '#VisitBrasil',
    'bolivia': '#TurismoBolivia',
    'ecuador': '#TurismoEcuador',
}

PROMPT = """Eres un analista de turismo y gestión de riesgos.
¿El siguiente tweet describe una atracción, infraestructura, evento o alerta de riesgo de valor estratégico? Responde SOLO con SI o NO.
Texto:\n"""

def phi3_evaluar(texto: str) -> bool:
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3:latest", "prompt": PROMPT + texto, "stream": False},
            timeout=15,
        )
        if r.status_code == 200:
            return "SI" in r.json().get('response', '').upper()
    except Exception:
        pass
    return False

def cargar_historial(pais):
    path = os.path.join(BASE_DIR, f"historial_{pais}.json")
    return json.load(open(path, 'r', encoding='utf-8')) if os.path.exists(path) else []

def guardar_historial(pais, hist):
    path = os.path.join(BASE_DIR, f"historial_{pais}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def buscar_tweets(hashtag, max_results=50):
    # Endpoint de búsqueda reciente
    url = 'https://api.twitter.com/2/tweets/search/recent'
    params = {
        'query': hashtag,
        'max_results': min(max_results, 100),
        'tweet.fields': 'created_at,author_id,lang',
    }
    resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
    if resp.status_code != 200:
        print(f"[⚠️] Error Twitter {resp.status_code}: {resp.text}")
        return []
    data = resp.json().get('data', [])
    return data

def main():
    print('=== INICIO AGENTE SOCIAL (Twitter/X) ===')
    for pais, tag in HASHTAGS.items():
        print(f"\n--- {pais.upper()} – {tag}")
        historial = cargar_historial(pais)
        vistos = {h['id'] for h in historial}
        tweets = buscar_tweets(tag, max_results=30)
        for tw in tweets:
            if tw['id'] in vistos:
                continue
            texto = tw.get('text', '')
            if phi3_evaluar(texto):
                registro = {
                    'id': tw['id'],
                    'text': texto,
                    'author_id': tw.get('author_id'),
                    'created_at': tw.get('created_at'),
                    'pais': pais,
                    'hashtag': tag,
                }
                historial.append(registro)
                print(f"[✓] RELEVANTE: {texto[:60]}")
            else:
                print(f"[✗] NO RELEVANTE: {texto[:60]}")
            time.sleep(random.randint(5, 10))
        guardar_historial(pais, historial)
        time.sleep(30)
    print('=== AGENTE SOCIAL FINALIZADO ===')

if __name__ == '__main__':
    main()
