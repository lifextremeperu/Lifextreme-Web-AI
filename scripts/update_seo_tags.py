import re
from pathlib import Path

# Ruta del proyecto (el script está en scripts/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Nuevo title y meta description (el que el usuario eligió)
NEW_TITLE = "Turismo de Aventura en Perú – Lifextreme | Guías Expertas y Tours a Medida"
NEW_DESCRIPTION = "Descubre Perú con Lifextreme: tours de alta montaña, trekking en la selva y deportes acuáticos en la costa. Guías profesionales y planes diseñados para extranjeros y viajeros peruanos."

# Expresiones regulares para reemplazar (case‑insensitive)
TITLE_RE = re.compile(r"<title>.*?</title>", flags=re.IGNORECASE | re.DOTALL)
META_RE = re.compile(r"<meta\s+name=[\"']description[\"']\s+content=[\"'].*?[\"']\s*/?>", flags=re.IGNORECASE | re.DOTALL)

def replace_in_file(html_path: Path):
    content = html_path.read_text(encoding="utf-8")
    # Reemplazar title
    if TITLE_RE.search(content):
        content = TITLE_RE.sub(f"<title>{NEW_TITLE}</title>", content)
    else:
        # Si no hay title, lo insertamos justo después de <head>
        content = re.sub(r"<head>", f"<head>\n    <title>{NEW_TITLE}</title>", content, flags=re.IGNORECASE)
    # Reemplazar meta description
    if META_RE.search(content):
        content = META_RE.sub(f"<meta name=\"description\" content=\"{NEW_DESCRIPTION}\">", content)
    else:
        # Insertamos después de <head> si no existía
        content = re.sub(r"<head>", f"<head>\n    <meta name=\"description\" content=\"{NEW_DESCRIPTION}\">", content, flags=re.IGNORECASE)
    html_path.write_text(content, encoding="utf-8")
    print(f"✅  Updated {html_path.relative_to(PROJECT_ROOT)}")

def main():
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    if not html_files:
        print("[!] No HTML files found.")
        return
    for html_path in html_files:
        replace_in_file(html_path)
    print("\n🎉  Todos los archivos HTML fueron actualizados con el nuevo title y meta description.")

if __name__ == "__main__":
    main()
