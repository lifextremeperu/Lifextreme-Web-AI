import json
import os
import re
import ssl
import time
import urllib.request
from html import unescape

PROSPECTS = [
    {
        "slug": "encuentros_peru_adventure",
        "agencia": "Encuentros Peru Adventure",
        "razon_social": "ENCUENTROS PERU ADVENTURE E.I.R.L.",
        "ruc": "20606891432",
        "rep_legal": "José Luis Juño Quispe",
        "saludo_nombre": "José Luis",
        "email": "info@encuentrosperuadventure.com",
        "telefono": "973124984",
        "web": "https://www.encuentrosperuadventure.com",
        "clase": "Minorista",
        "distrito": "Cusco",
        "reviews": "26 reseñas (4.8★)",
    },
    {
        "slug": "adventure_peru_tours",
        "agencia": "Adventure Peru Tours",
        "razon_social": "AGENCIA DE VIAJES Y TURISMO ADVENTURE PERU TOURS, TOURS OPERATOR E.I.R.L.",
        "ruc": "20450648672",
        "rep_legal": "José Luis Toledo Villegas",
        "saludo_nombre": "José Luis",
        "email": "info@adventureperutours.com",
        "telefono": "984264702",
        "web": "https://www.adventureperutours.com",
        "clase": "Operador de Turismo",
        "distrito": "Santiago, Cusco",
        "reviews": "18 reseñas (4.8★)",
    },
    {
        "slug": "ausangate_adventure",
        "agencia": "Ausangate Adventure",
        "razon_social": "AUSANGATE ADVENTURE S.A.C.",
        "ruc": "20611891092",
        "rep_legal": "Wilian Crispín Jancco",
        "saludo_nombre": "Wilian",
        "email": "INFO@AUSANGATEADVENTURE.COM",
        "telefono": "914201334",
        "web": "https://www.ausangateadventure.com",
        "clase": "Operador de Turismo",
        "distrito": "San Sebastián, Cusco",
        "reviews": "15 reseñas (5.0★)",
    },
    {
        "slug": "cusco_aventura",
        "agencia": "Cusco Aventura",
        "razon_social": "CUSCO VENTURA E.I.R.L.",
        "ruc": "20610721746",
        "rep_legal": "Wilfredo Ayma Auccapuma",
        "saludo_nombre": "Wilfredo",
        "email": "info@cuscoaventura.com",
        "telefono": "949904393",
        "web": "https://www.cuscoaventura.com",
        "clase": "Operador de Turismo",
        "distrito": "Cusco",
        "reviews": "13 reseñas (4.7★)",
    },
    {
        "slug": "green_peru_adventures",
        "agencia": "Green Peru Adventures",
        "razon_social": "Green Peru Adventures E.I.R.L.",
        "ruc": "20564395529",
        "rep_legal": "Roland Leonardo Gamboa",
        "saludo_nombre": "Roland",
        "email": "info@greenperuadventures.com",
        "telefono": "084 252003",
        "web": "https://www.greenperuadventures.com",
        "clase": "Minorista",
        "distrito": "Calle Triunfo 392, Cusco",
        "reviews": "11 reseñas (4.1★)",
    },
    {
        "slug": "aventuras_ecotrek_peru",
        "agencia": "Aventuras Ecotrek Peru",
        "razon_social": "Aventuras Ecotrek Peru Agencia De Viajes",
        "ruc": "20490266179",
        "rep_legal": "Luz Del Milagro Arrospide Miranda",
        "saludo_nombre": "Luz",
        "email": "info@aventurasecotrekperu.com",
        "telefono": "984562260",
        "web": "https://www.aventurasecotrekperu.com",
        "clase": "Operador de Turismo",
        "distrito": "Urb. Magisterio, Cusco",
        "reviews": "6 reseñas (4.0★)",
    },
    {
        "slug": "just_enjoy_peru",
        "agencia": "Just Enjoy Peru",
        "razon_social": "Just Enjoy Peru S.R.L.",
        "ruc": "20605069241",
        "rep_legal": "Miguel Ángel Salas Perea",
        "saludo_nombre": "Miguel Ángel",
        "email": "info@justenjoyperu.com",
        "telefono": "963358623",
        "web": "https://www.justenjoyperu.com",
        "clase": "Operador de Turismo",
        "distrito": "Poroy, Cusco",
        "reviews": "Registro MINCETUR",
    },
    {
        "slug": "mario_expeditions",
        "agencia": "Mario Expeditions",
        "razon_social": "Mario Expeditions E.I.R.L.",
        "ruc": "20603081642",
        "rep_legal": "Mario Hurtado Valencia",
        "saludo_nombre": "Mario",
        "email": "info@marioexpeditions.com",
        "telefono": "973476992",
        "web": "https://www.marioexpeditions.com",
        "clase": "Operador de Turismo",
        "distrito": "Santiago, Cusco",
        "reviews": "Registro MINCETUR",
    },
    {
        "slug": "turismo_peru_full",
        "agencia": "Turismo Peru Full",
        "razon_social": "Turismo Peru Full E.I.R.L.",
        "ruc": "20601981018",
        "rep_legal": "Richard Michael Hoffmann Arévalo",
        "saludo_nombre": "Richard",
        "email": "info@turismoperufull.com",
        "telefono": "960123801",
        "web": "https://www.turismoperufull.com",
        "clase": "Operador de Turismo",
        "distrito": "Av. El Sol 948, Cusco",
        "reviews": "Registro MINCETUR",
    },
    {
        "slug": "ed_pertur",
        "agencia": "E.D. Pertur",
        "razon_social": "E.D. Pertur E.I.R.L.",
        "ruc": "20604072833",
        "rep_legal": "Jimmy Mendoza Escalante",
        "saludo_nombre": "Jimmy",
        "email": "info@edpertur.com",
        "telefono": "084 260732",
        "web": "https://www.edpertur.com",
        "clase": "Operador de Turismo",
        "distrito": "Av. El Sol 315, Cusco",
        "reviews": "Registro MINCETUR",
    },
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LifextremeAuditBot/1.0)"}


def fetch_url(url, timeout=10):
    t0 = time.time()
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        raw = resp.read(300_000)
        elapsed = round(time.time() - t0, 2)
        return resp.status, resp.geturl(), elapsed, raw.decode("utf-8", errors="ignore")


def audit_site(url):
    info = {
        "status": None,
        "final_url": url,
        "load_s": None,
        "title": "",
        "meta_desc": "",
        "cms": "Sitio personalizado / HTML",
        "has_schema_jsonld": False,
        "schema_types": [],
        "has_llms_txt": False,
        "has_whatsapp": False,
        "multilang": False,
        "tours_detected": [],
        "error": None,
    }
    try:
        status, final_url, elapsed, html = fetch_url(url)
        info["status"] = status
        info["final_url"] = final_url
        info["load_s"] = elapsed
        low = html.lower()

        m_title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        if m_title:
            info["title"] = re.sub(r"\s+", " ", unescape(m_title.group(1))).strip()[:120]

        m_desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I | re.S)
        if not m_desc:
            m_desc = re.search(r'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']description["\']', html, re.I | re.S)
        if m_desc:
            info["meta_desc"] = re.sub(r"\s+", " ", unescape(m_desc.group(1))).strip()[:160]

        if "wp-content" in low or "wordpress" in low:
            info["cms"] = "WordPress"
        elif "wix.com" in low or "wixstatic" in low:
            info["cms"] = "Wix"
        elif "shopify" in low:
            info["cms"] = "Shopify"
        elif "_next/static" in low:
            info["cms"] = "Next.js"

        if "application/ld+json" in low:
            info["has_schema_jsonld"] = True
            types = re.findall(r'"@type"\s*:\s*"([^"]+)"', html)
            info["schema_types"] = sorted(set(types))[:6]

        info["has_whatsapp"] = ("wa.me/" in low) or ("api.whatsapp.com" in low) or ("whatsapp" in low)
        info["multilang"] = any(k in low for k in ["/en/", "/es/", "lang=", "wpml", "polylang", "gtranslate"])

        tour_keywords = [
            "Machu Picchu", "Salkantay", "Ausangate", "Inca Trail", "Camino Inca",
            "Sacred Valley", "Valle Sagrado", "Rainbow Mountain", "Vinicunca",
            "Humantay", "Choquequirao", "City Tour", "Titicaca", "Arequipa"
        ]
        found_tours = [kw for kw in tour_keywords if kw.lower() in low]
        info["tours_detected"] = found_tours[:6]

        # Check /llms.txt quickly
        base = re.match(r"https?://[^/]+", final_url)
        if base:
            try:
                st_llms, _, _, body_llms = fetch_url(base.group(0) + "/llms.txt", timeout=5)
                if st_llms == 200 and len(body_llms.strip()) > 20 and "<html" not in body_llms.lower()[:120]:
                    info["has_llms_txt"] = True
            except Exception:
                pass
    except Exception as e:
        info["error"] = str(e)[:120]
    return info


def build_diagnostic_bullets(p, a):
    bullets = []
    if a["error"]:
        bullets.append(
            f"<strong>Tu presencia web ({p['web'].replace('https://www.', '')}):</strong> detectamos que el sitio presentó latencia o bloqueo de acceso automático (<code>{a['error'][:60]}</code>); con <strong>Claude Code</strong> podemos optimizar tu web o crear una landing rápida de venta directa con cotizador en S/ y USD."
        )
    else:
        stack_msg = f"Detectamos que tu web (<code>{a['final_url'].replace('https://', '').rstrip('/')}</code>) corre sobre <strong>{a['cms']}</strong> (carga en {a['load_s']}s)."
        if a["cms"] == "WordPress":
            stack_msg += " En el taller verás cómo crear landings y cotizadores propios con <strong>Claude Code</strong> sin depender de plugins lentos ni terceros."
        else:
            stack_msg += " Con <strong>Claude Code</strong> tu equipo podrá actualizar rutas, precios y landings de venta directa en minutos."
        bullets.append(stack_msg)

    # GEO / AEO bullet
    if not a["has_llms_txt"] and not a["has_schema_jsonld"]:
        bullets.append(
            "<strong>Visibilidad en IA (SEO / GEO / AEO):</strong> hoy tu web <strong>no cuenta con datos estructurados Schema ni archivo <code>llms.txt</code></strong>, lo que reduce tus chances cuando un turista pregunta a ChatGPT, Claude o Perplexity qué agencia elegir en Cusco."
        )
    elif not a["has_llms_txt"]:
        bullets.append(
            f"<strong>Visibilidad en IA (GEO / AEO):</strong> ya tienes Schema (<code>{', '.join(a['schema_types']) or 'JSON-LD'}</code>), pero falta <strong><code>llms.txt</code> y contenido optimizado para respuestas de IA</strong> para captar reservas directas sin pagar 20%–30% a OTAs."
        )
    else:
        bullets.append(
            "<strong>Visibilidad en IA (GEO / AEO):</strong> tu web ya tiene base técnica; en el taller reforzaremos tu posicionamiento en motores de IA y propuestas visuales con <strong>Claude Design + Higgsfield</strong>."
        )

    # Operations / Tours bullet
    tours = ", ".join(a["tours_detected"]) if a["tours_detected"] else "rutas en Cusco y Machu Picchu"
    bullets.append(
        f"<strong>Operación diaria ({tours}):</strong> armamos en la laptop de tu equipo (5–10 personas) <strong>Skills de PDF para cotizar en minutos</strong>, conexión con <strong>Calendar/Drive</strong> y su <strong>propio RAG en Qdrant</strong> con tus tarifarios y políticas reales."
    )
    return bullets


def main():
    with open("reportes_b2b/email_presentacion_ia_agencias_cusco.html", "r", encoding="utf-8") as f:
        template = f.read()

    out_dir = "reportes_b2b/emails_personalizados"
    os.makedirs(out_dir, exist_ok=True)
    results = []

    anchor = (
        '              <p style="margin:0 0 10px 0; font-size:14.5px; line-height:1.6; color:#141413;">\n'
        '                <strong>Estimado/a líder de agencia:</strong> bajo el principio andino del <strong style="color:#c25e3e;">Ayni (crecemos juntos)</strong>, queremos que el turismo en Cusco modernice sus procesos <strong>sin depender de grandes corporaciones</strong>, sino enseñando a tu equipo a <strong>dominar y crear su propia tecnología</strong>.\n'
        '              </p>'
    )
    assert anchor in template, "Anchor not found in email_presentacion_ia_agencias_cusco.html"

    for p in PROSPECTS:
        print(f"Auditing {p['agencia']} -> {p['web']} ...")
        audit = audit_site(p["web"])
        bullets = build_diagnostic_bullets(p, audit)
        p_full = {**p, "audit": audit, "diagnostico_bullets": bullets}
        results.append(p_full)

        custom_block = f'''              <p style="margin:0 0 10px 0; font-size:14.5px; line-height:1.6; color:#141413;">
                <strong>Hola {p['saludo_nombre']} ({p['agencia']}):</strong> bajo el principio andino del <strong style="color:#c25e3e;">Ayni (crecemos juntos)</strong>, queremos que el turismo en Cusco modernice sus procesos <strong>sin depender de grandes corporaciones</strong>, sino enseñando a tu equipo a <strong>dominar y crear su propia tecnología</strong>.
              </p>

              <!-- DIAGNÓSTICO PERSONALIZADO DE SU WEB Y OPERACIÓN -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #0f766e; border-radius:8px; margin-bottom:12px;">
                <tr>
                  <td style="padding:12px 15px; font-size:12.5px; line-height:1.55; color:#134e4a;">
                    <strong style="color:#0f766e;">🔎 Mini-diagnóstico previo de {p['agencia']} ({p['web'].replace('https://www.', '')}):</strong><br/>
                    • {bullets[0]}<br/>
                    • {bullets[1]}<br/>
                    • {bullets[2]}
                  </td>
                </tr>
              </table>'''

        html_out = template.replace(anchor, custom_block)
        # Fix relative asset paths for subfolder reportes_b2b/emails_personalizados/
        html_out = html_out.replace('href="assets/', 'href="../assets/')
        html_out = html_out.replace('src="assets/', 'src="../assets/')
        html_out = html_out.replace('href="../agendar-capacitacion.html', 'href="../../agendar-capacitacion.html')

        out_path = os.path.join(out_dir, f"{p['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as wf:
            wf.write(html_out)

    with open("reportes_b2b/prospectos_top10_piloto.json", "w", encoding="utf-8") as jf:
        json.dump(results, jf, ensure_ascii=False, indent=2)

    print("\n=== SUMMARY ===")
    for r in results:
        a = r["audit"]
        print(f"- {r['agencia']} | status={a['status']} | cms={a['cms']} | schema={a['has_schema_jsonld']} | llms={a['has_llms_txt']} | tours={a['tours_detected']} | err={a['error']}")


if __name__ == "__main__":
    main()
