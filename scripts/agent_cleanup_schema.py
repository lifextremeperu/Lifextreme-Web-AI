import re
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = PROJECT_ROOT / "index.html"
CONFIG_FILE = PROJECT_ROOT / "config" / "site_info.json"

def load_site_info():
    import json
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_html(content, site):
    # 1️⃣ Ensure single JSON‑LD TravelAgency block
    # Find all <script type="application/ld+json"> blocks
    blocks = re.findall(r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", content, flags=re.DOTALL|re.IGNORECASE)
    travel_blocks = []
    other_blocks = []
    for b in blocks:
        if "@type" in b and "TravelAgency" in b:
            travel_blocks.append(b)
        else:
            other_blocks.append(b)
    # Keep only the last (real) travel block, discard the rest
    if travel_blocks:
        # Build the new travel block using data from config
        new_travel = {
            "@context": "https://schema.org",
            "@type": "TravelAgency",
            "name": "Lifextreme",
            "url": site.get("url", "https://www.lifextreme.store"),
            "address": {
                "@type": "PostalAddress",
                "streetAddress": site["address"]["streetAddress"],
                "addressLocality": site["address"]["addressLocality"],
                "addressCountry": site["address"]["addressCountry"]
            },
            "telephone": site.get("telephone", "")
        }
        import json as _json
        travel_json = _json.dumps(new_travel, ensure_ascii=False, indent=2)
        # Replace all existing TravelAgency blocks with the new one
        for old in travel_blocks:
            content = content.replace(old, travel_json)
    # 2️⃣ Ensure meta title & description
    title_tag = f"<title>Lifextreme (lifextreme.store) | Plataforma y Club de Turismo de Aventura en Cusco, Perú</title>"
    meta_desc = f"<meta name=\"description\" content=\"Lifextreme (lifextreme.store) | Plataforma y Club de Turismo de Aventura en Cusco, Perú\">"
    # Replace or insert title
    if re.search(r"<title>.*?</title>", content, flags=re.IGNORECASE):
        content = re.sub(r"<title>.*?</title>", title_tag, content, flags=re.IGNORECASE)
    else:
        # insert just after <head>
        content = re.sub(r"<head>", f"<head>\n    {title_tag}", content, flags=re.IGNORECASE)
    # Replace or insert meta description
    if re.search(r"<meta\s+name=[\"']description[\"'].*?>", content, flags=re.IGNORECASE):
        content = re.sub(r"<meta\s+name=[\"']description[\"'].*?>", meta_desc, content, flags=re.IGNORECASE)
    else:
        content = re.sub(r"<head>", f"<head>\n    {meta_desc}", content, flags=re.IGNORECASE)
    return content

def main():
    if not INDEX_FILE.exists():
        print(f"[!] No se encontró {INDEX_FILE}")
        sys.exit(1)
    site = load_site_info()
    html = INDEX_FILE.read_text(encoding="utf-8")
    cleaned = clean_html(html, site)
    INDEX_FILE.write_text(cleaned, encoding="utf-8")
    print("✅  Bloque JSON‑LD duplicado eliminado, meta‑title y meta‑description actualizados.")
    print(f"✔  Cambios guardados en {INDEX_FILE}")

if __name__ == "__main__":
    main()
