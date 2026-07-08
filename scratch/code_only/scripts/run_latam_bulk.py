import os, json, time, random, requests
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Configuración del agente "LatAm Bulk" (crawling serial de 5 h)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_pdfs'))
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}

# ---------------------------------------------------------------
# Enlaces directos por país (actualiza según necesites)
# ---------------------------------------------------------------
ENLACES_LATAM = {
    "chile": [
        "https://www.sernatur.cl/wp-content/uploads/2018/11/Estrategia-Nacional-de-Turismo-2012-2020.pdf",
        "https://senapred.cl/wp-content/uploads/2023/01/Plan-Estrategico-Nacional-para-la-Reduccion-del-Riesgo-de-Desastres.pdf"
    ],
    "argentina": [
        "https://www.argentina.gob.ar/sites/default/files/plan_estrategico_territorial.pdf",
        "https://www.argentina.gob.ar/sites/default/files/plan_nacional_de_reduccion_del_riesgo_de_desastres_2024-2030.pdf"
    ],
    "colombia": [
        "https://www.mincit.gov.co/getattachment/minturismo/calidad-y-desarrollo-sostenible/plan-sectorial-de-turismo-2022-2026/plan-sectorial-de-turismo-2022-2026.pdf.aspx",
        "https://www.invias.gov.co/index.php/documentos-tecnicos/11497-plan-nacional-de-seguridad-vial/file"
    ],
    "brasil": [
        "https://www.gov.br/turismo/pt-br/acesso-a-informacao/acoes-e-programas/plano-nacional-de-turismo/PNT20242027_aprovado.pdf"
    ],
    "bolivia": [
        "https://www.defensacivil.gob.bo/web/uploads/files/Plan_Nacional_Emergencias.pdf"
    ],
    "ecuador": [
        "https://www.turismo.gob.ec/wp-content/uploads/2020/03/PLANDETUR-2030.pdf"
    ]
}

# ---------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------
def cargar_historial(pais: str):
    path = os.path.join(BASE_DIR, pais, f"historial_{pais}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_historial(pais: str, hist):
    path = os.path.join(BASE_DIR, pais, f"historial_{pais}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def evaluar_con_phi3(titulo: str, url: str, pais: str) -> bool:
    prompt = f"""Eres un analista de turismo y gestión de riesgos.
¿Este documento (título: {titulo}) pertenece a una entidad oficial (gobierno, ministerio) y contiene información estratégica de infraestructura o turismo?
Responde SOLO con SI o NO."""
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3:latest", "prompt": prompt, "stream": False},
            timeout=15,
        )
        if resp.status_code == 200:
            return "SI" in resp.json().get("response", "").upper()
    except Exception:
        pass
    # Si falla la llamada, consideramos "sí" para no perder datos
    return True

def descarga_etica(url: str, destino: str) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=20)
        if r.status_code == 429:
            print("[⚠️] 429 Too Many Requests → pausa 60s")
            time.sleep(60)
            return False
        r.raise_for_status()
        ct = r.headers.get('content-type', '').lower()
        if 'pdf' not in ct and not url.lower().endswith('.pdf'):
            print('[❌] No es PDF, se omite')
            return False
        with open(destino, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f'[❗] Error al descargar {url}: {e}')
        return False

# ---------------------------------------------------------------
# Motor principal (serial, con límite de 5 h)
# ---------------------------------------------------------------
def main():
    start = time.time()
    max_seconds = 5 * 60 * 60  # 5 h

    for pais, urls in ENLACES_LATAM.items():
        pais_dir = os.path.join(BASE_DIR, pais)
        os.makedirs(pais_dir, exist_ok=True)
        historial = cargar_historial(pais)
        ya_descargadas = {h['url'] for h in historial}
        print(f"\n=== Procesando {pais.upper()} ===")

        for url in urls:
            # Verificar límite de tiempo
            if time.time() - start > max_seconds:
                print('[⏰] Tiempo límite alcanzado → finalizando')
                return
            if url in ya_descargadas:
                print(f"[✔] Ya descargado: {url}")
                continue
            titulo = os.path.basename(urlparse(url).path) or "documento"
            print(f"→ Evaluando {titulo[:60]} ...")
            if evaluar_con_phi3(titulo, url, pais):
                print('[✅] Phi‑3 aprobó')
                safe_name = "".join(c if c.isalnum() else '_' for c in titulo)[:50]
                destino = os.path.join(pais_dir, f"{safe_name}_{int(time.time())}.pdf")
                if descarga_etica(url, destino):
                    print(f"[💾] Guardado: {destino}")
                    historial.append({"url": url, "fecha": time.strftime('%Y-%m-%d %H:%M:%S'), "archivo": os.path.basename(destino)})
                    guardar_historial(pais, historial)
                else:
                    print('[❌] Falló la descarga')
            else:
                print('[🚫] Phi‑3 rechazó (no institucional)')
            # Pausa entre documentos (5‑12 s)
            espera = random.randint(5, 12)
            print(f"[🕑] Pausa {espera}s")
            time.sleep(espera)
        # Pausa entre países (30 s)
        print('[⏳] Descanso entre países → 30 s')
        time.sleep(30)
    print('[🏁] Trabajo completado antes del límite de tiempo')

if __name__ == '__main__':
    main()
