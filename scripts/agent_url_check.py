import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json, time, random, requests
from datetime import datetime

# Directories for logs and data
BASE_LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(BASE_LOG_DIR, exist_ok=True)

# Import the site dictionaries defined in the scraper module
from agent_scrape_guides import GUIDE_SITES, BLOG_SITES

def log_message(message: str):
    """Append a timestamped line to the URL check log."""
    log_path = os.path.join(BASE_LOG_DIR, f"url_check_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.utcnow().isoformat()
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def check_url(url: str) -> bool:
    """Perform a HEAD request to verify that a URL is reachable.
    Returns True if status < 400, otherwise False.
    """
    try:
        resp = requests.head(url, timeout=10, headers={"User-Agent": "LifextremeBot/1.0"})
        resp.raise_for_status()
        return True
    except Exception as e:
        log_message(f"[⚠️] URL no accesible {url}: {e}")
        return False

def main():
    log_message("=== INICIO VERIFICACIÓN DE URLs ===")
    # Check guide URLs
    for site, cfg in GUIDE_SITES.items():
        base = cfg["base"]
        for pais in cfg["countries"]:
            url = base + cfg["path"](pais.lower())
            reachable = check_url(url)
            status = "OK" if reachable else "FALLA"
            log_message(f"Guía {site}/{pais}: {url} -> {status}")
            time.sleep(random.uniform(0.5, 1.5))
    # Check blog URLs
    for pais, urls in BLOG_SITES.items():
        for url in urls:
            reachable = check_url(url)
            status = "OK" if reachable else "FALLA"
            log_message(f"Blog {pais}: {url} -> {status}")
            time.sleep(random.uniform(0.5, 1.5))
    log_message("=== VERIFICACIÓN DE URLs FINALIZADA ===")

if __name__ == "__main__":
    main()
