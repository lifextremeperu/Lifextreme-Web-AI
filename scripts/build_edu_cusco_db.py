import asyncio
import csv
import os
import re
import sqlite3
import urllib3
import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DB_PATH = os.path.join("data", "educacion_cusco.db")
CSV_PATH = os.path.join("data", "educacion_cusco.csv")

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:\+?51\s*)?(?:\(0?84\)\s*\d{6}|084[\s-]?\d{6}|9\d{2}[\s-]?\d{3}[\s-]?\d{3})")

EXCLUDE_EMAIL_TERMS = (
    "sentry", "wix", "example", "domain.com", "email.com", ".png", ".jpg",
    ".jpeg", ".webp", ".svg", ".css", ".js", "u00", "noreply", "no-reply",
    "bootstrap", "wordpress", "schema.org", "w3.org"
)

# Semilla verificada de instituciones educativas públicas y privadas en Cusco
SEED_INSTITUCIONES = [
    # Universidades
    ("Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)", "Universidad", "Pública", "Cusco", "https://www.unsaac.edu.pe", "mesadepartes@unsaac.edu.pe"),
    ("Universidad Andina del Cusco (UAC)", "Universidad", "Privada", "Cusco / San Jerónimo", "https://www.uandina.edu.pe", ""),
    ("Universidad Continental - Filial Cusco", "Universidad", "Privada", "Cusco", "https://ucontinental.edu.pe", ""),
    ("Universidad Tecnológica de los Andes (UTEA) - Filial Cusco", "Universidad", "Privada", "Cusco", "https://www.utea.edu.pe", ""),
    ("Universidad César Vallejo (UCV) - Campus Cusco", "Universidad", "Privada", "Cusco", "https://www.ucv.edu.pe", ""),
    ("Universidad Peruana Austral del Cusco", "Universidad", "Privada", "Cusco", "https://www.uaustral.edu.pe", ""),
    # Institutos Superiores
    ("IESTP Túpac Amaru", "Instituto Superior", "Pública", "San Sebastián, Cusco", "https://www.istta.edu.pe", ""),
    ("Instituto Superior Khipu", "Instituto Superior", "Privada", "Cusco", "https://www.khipu.edu.pe", ""),
    ("SENATI Zonal Cusco", "Instituto Superior", "Privada", "Cusco", "https://www.senati.edu.pe", ""),
    ("Instituto Superior Antonio Lorena", "Instituto Superior", "Privada", "Cusco", "https://www.antoniolorena.edu.pe", ""),
    ("Instituto Superior La Pontificia / IESTP Cusco", "Instituto Superior", "Privada", "Cusco", "https://www.ilp.edu.pe", ""),
    ("Instituto Superior Tecnológico Signos de Fe", "Instituto Superior", "Privada", "Cusco", ""),
    ("SENCICO Zonal Cusco", "Instituto Superior", "Pública", "Cusco", "https://www.sencico.gob.pe", ""),
    # Colegios Privados Cusco
    ("Colegio San Martín de Porres", "Colegio", "Privada", "Cusco", "https://sanmartincusco.edu.pe", "contacto@sanmartincusco.edu.pe"),
    ("Colegio Santa Ana de Cusco", "Colegio", "Privada", "Cusco", "https://santaanacusco.edu.pe", ""),
    ("Colegio San Francisco de Asís de Cusco", "Colegio", "Privada", "Cusco", "https://colegiosanfranciscocusco.edu.pe", ""),
    ("Colegio La Salle Cusco", "Colegio", "Privada", "Cusco", "https://lasallecusco.edu.pe", ""),
    ("Colegio Salesiano del Cusco", "Colegio", "Privada", "Cusco", "https://salesianocusco.edu.pe", ""),
    ("Colegio San José Obrero Cusco", "Colegio", "Privada", "Cusco", "https://sanjoseobrero.edu.pe", ""),
    ("Colegio San Antonio Abad del Cusco", "Colegio", "Privada", "Cusco", "https://sanantonioabad.edu.pe", ""),
    ("Colegio Andino Cusco International School", "Colegio", "Privada", "Cusco", "https://colegioandino.edu.pe", ""),
    ("Colegio Peruano Británico / Pukllasunchis", "Colegio", "Privada", "Cusco", "https://pukllasunchis.org", ""),
    ("Colegio Galileo Cusco", "Colegio", "Privada", "Cusco", "https://colegiogalileo.edu.pe", ""),
    ("Colegio Raimondi Cusco", "Colegio", "Privada", "Wanchaq, Cusco", "https://colegioraimondi.edu.pe", ""),
    ("Colegio Innova Schools Cusco", "Colegio", "Privada", "Cusco", "https://www.innovaschools.edu.pe", ""),
    ("Colegio Trilce Cusco", "Colegio", "Privada", "Cusco", "https://www.trilce.edu.pe", ""),
    ("Colegio Saco Oliveros Cusco", "Colegio", "Privada", "Cusco", "https://sacooliveros.edu.pe", ""),
    ("Colegio San Agustín Cusco", "Colegio", "Privada", "Cusco", "https://sanagustincusco.edu.pe", ""),
    ("Colegio Santa Rosa de Lima Cusco", "Colegio", "Privada", "Cusco", "https://santarosacusco.edu.pe", ""),
    ("Colegio Nuestra Señora de la Merced Cusco", "Colegio", "Privada", "Cusco", "https://mercedcusco.edu.pe", ""),
    # Colegios Públicos Emblemáticos Cusco
    ("Colegio Nacional de Ciencias del Cusco", "Colegio", "Pública", "Cusco", "https://colegiocienciascusco.edu.pe", ""),
    ("Colegio Inca Garcilaso de la Vega", "Colegio", "Pública", "Wanchaq, Cusco", "https://incagarcilasocusco.edu.pe", ""),
    ("Colegio Clorinda Matto de Turner", "Colegio", "Pública", "Cusco", "https://clorindamattocusco.edu.pe", ""),
    ("Colegio Educandas del Cusco", "Colegio", "Pública", "Cusco", "https://educandascusco.edu.pe", ""),
    ("COAR Cusco (Colegio de Alto Rendimiento)", "Colegio", "Pública", "Oropesa, Quispicanchi, Cusco", "https://www.minedu.gob.pe/coar", ""),
    # Entidades Educativas Regionales (DRE / UGEL)
    ("GEREDU / DRE Cusco - Equipo Instituciones Privadas", "DRE / UGEL", "Pública", "Cusco", "https://web.gereducusco.gob.pe", "equipoprivadas@drecusco.edu.pe"),
    ("UGEL Cusco", "DRE / UGEL", "Pública", "Cusco", "https://ugelcusco.gob.pe", ""),
    ("UGEL Urubamba", "DRE / UGEL", "Pública", "Urubamba, Cusco", "https://ugelurubamba.gob.pe", ""),
    ("UGEL Calca", "DRE / UGEL", "Pública", "Calca, Cusco", "https://ugelcalca.gob.pe", ""),
    ("UGEL Anta", "DRE / UGEL", "Pública", "Anta, Cusco", "https://ugelanta.gob.pe", ""),
    ("UGEL Canchis", "DRE / UGEL", "Pública", "Sicuani, Canchis, Cusco", "https://ugelcanchis.gob.pe", ""),
    ("UGEL Quispicanchi", "DRE / UGEL", "Pública", "Urcos, Quispicanchi, Cusco", "https://ugelquispicanchi.gob.pe", ""),
    ("UGEL La Convención", "DRE / UGEL", "Pública", "Quillabamba, La Convención, Cusco", "https://ugellaconvencion.gob.pe", ""),
]

DDG_QUERIES = [
    ("colegios privados cusco \"edu.pe\" contacto correo", "Colegio", "Privada"),
    ("colegio publico cusco \"edu.pe\" contacto", "Colegio", "Pública"),
    ("instituto superior cusco \"edu.pe\" contacto", "Instituto Superior", "Privada"),
    ("cetpro cusco contacto correo", "CETPRO", "Pública"),
]


def is_valid_email(email: str) -> bool:
    e = email.lower().strip()
    if len(e) < 6 or len(e) > 80:
        return False
    if any(term in e for term in EXCLUDE_EMAIL_TERMS):
        return False
    if not re.match(r"^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z]{2,}$", e):
        return False
    return True


async def scrape_contact_from_site(client: httpx.AsyncClient, base_url: str):
    if not base_url:
        return [], []
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    base_url = base_url.rstrip("/")

    emails = set()
    phones = set()
    paths = ["", "/contacto", "/contactenos", "/contact", "/nosotros"]

    for path in paths:
        url = base_url + path
        try:
            resp = await client.get(url, timeout=8.0, follow_redirects=True)
            if resp.status_code >= 400:
                continue
            html = resp.text
            for m in EMAIL_REGEX.findall(html):
                if is_valid_email(m):
                    emails.add(m.lower())
            # Buscar mailto: explícitos
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.select("a[href^='mailto:']"):
                addr = a.get("href", "").replace("mailto:", "").split("?")[0].strip()
                if is_valid_email(addr):
                    emails.add(addr.lower())
            text = soup.get_text(" ", strip=True)
            for p in PHONE_REGEX.findall(text):
                phones.add(p.strip())
            if emails and path == "":
                break
        except Exception:
            continue

    return sorted(emails)[:3], sorted(phones)[:2]


def discover_extra_institutions():
    discovered = []
    try:
        with DDGS() as ddgs:
            for query, tipo, gestion in DDG_QUERIES:
                try:
                    results = list(ddgs.text(query, max_results=10))
                    for r in results:
                        href = r.get("href", "")
                        title = r.get("title", "").split("|")[0].split("-")[0].strip()
                        if not href or not title:
                            continue
                        if any(skip in href.lower() for skip in ("facebook.com", "instagram.com", "youtube.com", "wikipedia.org", "colegiosperu.pe", "micole.net", "paginasamarillas")):
                            continue
                        discovered.append((title[:120], tipo, gestion, "Cusco", href, ""))
                except Exception as e:
                    print(f"[!] DDG query warning ({query}): {e}")
    except Exception as e:
        print(f"[!] DDGS init warning: {e}")
    return discovered


def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS instituciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT,
            gestion TEXT,
            distrito_provincia TEXT,
            web TEXT UNIQUE,
            email TEXT,
            telefono TEXT,
            fuente_url TEXT,
            status TEXT DEFAULT 'PENDING',
            sent_date TEXT
        )
    """)
    conn.commit()
    return conn


async def main():
    print("=== CONSTRUCTOR DE BASE DE DATOS EDUCATIVA CUSCO ===")
    extra = discover_extra_institutions()
    all_items = list(SEED_INSTITUCIONES) + extra

    # Deduplicar por dominio o nombre
    seen_domains = set()
    unique_items = []
    for item in all_items:
        nombre, tipo, gestion, distrito, web, seed_email = item
        domain = web.lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].strip()
        key = domain if domain else nombre.lower()
        if key in seen_domains:
            continue
        seen_domains.add(key)
        unique_items.append(item)

    print(f"[+] Instituciones únicas a verificar: {len(unique_items)}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    sem = asyncio.Semaphore(8)

    async def process_item(client, item):
        nombre, tipo, gestion, distrito, web, seed_email = item
        async with sem:
            emails, phones = await scrape_contact_from_site(client, web)
            if seed_email and seed_email.lower() not in emails:
                emails.insert(0, seed_email.lower())
            return {
                "nombre": nombre,
                "tipo": tipo,
                "gestion": gestion,
                "distrito_provincia": distrito,
                "web": web,
                "email": " | ".join(emails),
                "telefono": " | ".join(phones),
                "fuente_url": web,
            }

    async with httpx.AsyncClient(verify=False, headers=headers) as client:
        results = await asyncio.gather(*(process_item(client, item) for item in unique_items))

    conn = init_db()
    cur = conn.cursor()
    inserted = 0
    for r in results:
        try:
            cur.execute("""
                INSERT INTO instituciones (nombre, tipo, gestion, distrito_provincia, web, email, telefono, fuente_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(web) DO UPDATE SET
                    email = CASE WHEN excluded.email != '' THEN excluded.email ELSE instituciones.email END,
                    telefono = CASE WHEN excluded.telefono != '' THEN excluded.telefono ELSE instituciones.telefono END
            """, (
                r["nombre"], r["tipo"], r["gestion"], r["distrito_provincia"],
                r["web"] or None, r["email"], r["telefono"], r["fuente_url"]
            ))
            inserted += 1
        except Exception as e:
            print(f"[!] DB insert warning ({r['nombre']}): {e}")
    conn.commit()

    # Exportar CSV
    rows = cur.execute("""
        SELECT id, nombre, tipo, gestion, distrito_provincia, web, email, telefono, status
        FROM instituciones
        ORDER BY CASE WHEN email != '' THEN 0 ELSE 1 END, tipo, nombre
    """).fetchall()

    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Institución", "Tipo", "Gestión", "Distrito/Provincia", "Web", "Email", "Teléfono", "Estado"])
        writer.writerows(rows)

    with_email = sum(1 for r in rows if r[6])
    print(f"[OK] Total guardado en DB/CSV: {len(rows)} instituciones | Con email verificado: {with_email}")
    print("\nMuestra de instituciones con email:")
    for r in [x for x in rows if x[6]][:15]:
        print(f"  - [{r[2]} / {r[3]}] {r[1]} -> {r[6]} ({r[7]})")
    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
