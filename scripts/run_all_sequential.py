import sys
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime

# ---------------------------------------------------------------------------
# CONFIGURACIÓN GLOBAL
# ---------------------------------------------------------------------------
BASE_LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(BASE_LOG_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1️⃣  AGENTE RSS / API DE DATOS ABIERTOS
# ---------------------------------------------------------------------------
RSS_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'agent_rss_api.py'))

# ---------------------------------------------------------------------------
# 2️⃣  AGENTE SCRAPING DE GUÍAS TURÍSTICAS (LonelyPlanet, TripAdvisor)
# ---------------------------------------------------------------------------
SCRAPE_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'agent_scrape_guides.py'))

# ---------------------------------------------------------------------------
# 3️⃣  AGENTE REDES SOCIALES (Twitter/X) – requiere token en variable de entorno TWITTER_BEARER
# ---------------------------------------------------------------------------
SOCIAL_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'agent_social.py'))

# ---------------------------------------------------------------------------
# Función auxiliar para ejecutar un script y registrar su salida en un log
# ---------------------------------------------------------------------------
def run_and_log(script_path, name):
    log_file = os.path.join(BASE_LOG_DIR, f"{name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log")
    print(f"[RUNNING] Ejecutando {name} -> log: {log_file}")
    with open(log_file, "w", encoding="utf-8") as f:
        # lanzamos el proceso, se espera a que termine
        proc = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(line, end='')   # salida en consola en tiempo real
            f.write(line)
        proc.wait()
    print(f"[DONE] {name} finalizado (código {proc.returncode})\n")
    # pausa de seguridad entre etapas (30-60 s)
    pausa = random.randint(30, 60)
    print(f"[PAUSE] Pausa de {pausa}s antes del siguiente módulo")
    time.sleep(pausa)
    return proc.returncode

# ---------------------------------------------------------------------------
# ORQUESTADOR PRINCIPAL
# ---------------------------------------------------------------------------
URL_CHECK_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'agent_url_check.py'))

def main():
    print("=== INICIO DE PIPELINE ORDENADA Y PAUSADA (3 MÓDULOS) ===")
    # 0️⃣ Verificación de URLs
    rc = run_and_log(URL_CHECK_SCRIPT, "url_check")
    if rc != 0:
        print("[WARN] Verificación de URLs falló – se continuará de todos modos")
    # 1️⃣ RSS / APIs
    rc = run_and_log(RSS_SCRIPT, "rss_api")
    if rc != 0:
        print("[WARN] RSS/ API falló – se continuará con los siguientes módulos de todos modos")

    # 2️⃣ Scraping de guías turísticas
    rc = run_and_log(SCRAPE_SCRIPT, "scrape_guides")
    if rc != 0:
        print("[WARN] Scraping guías falló – se continuará con redes sociales")

    # 3️⃣ Redes sociales – OMITIDO (no hay token de Twitter)
    print("[INFO] Módulo de redes sociales omitido – no se ejecuta")

    print("=== PIPELINE COMPLETADO ===")

if __name__ == "__main__":
    main()
