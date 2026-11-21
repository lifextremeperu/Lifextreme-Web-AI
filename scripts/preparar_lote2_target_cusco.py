import csv
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET

XLSX_PATH = r"data\institucional_descargas\Agencias de Turismo en Peru.xlsx"
SENT_LOG = r"reportes_b2b\envios_piloto_log.json"
OUT_CSV = r"reportes_b2b\cusco_agencias_limpio.csv"
OUT_JSON = r"reportes_b2b\prospectos_lote2_50_target.json"
TEMPLATE_IN = r"reportes_b2b\email_presentacion_ia_agencias_cusco.html"
PREVIEW_OUT = r"reportes_b2b\preview_lote2_correo.html"

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
BOUTIQUE_KW = (
    "adventure", "expedition", "trek", "andes", "inca", "machu", "salkantay",
    "expediciones", "aventura", "luxury", "boutique", "experience", "travel",
    "peru", "cusco", "sacred", "trail", "explorer", "mountain", "nature"
)
FREE_DOMAINS = ("gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "live.com", "icloud.com")


def clean_first_name(rep_legal):
    if not rep_legal:
        return "Director/a"
    # Formats like "QUISPE MAMANI, JUAN CARLOS" or "JUAN CARLOS QUISPE"
    s = rep_legal.strip()
    if "," in s:
        after = s.split(",", 1)[1].strip()
        first = after.split()[0] if after else s.split()[0]
    else:
        parts = s.split()
        # Often AP1 AP2 NOM1 NOM2 in Peru MINCETUR; pick 3rd word if >=3 words and all caps, else 1st
        first = parts[2] if len(parts) >= 3 else parts[0]
    return first.capitalize()


def score_agency(row):
    score = 0
    clase = (row["clase"] or "").lower()
    tipo = (row["tipo"] or "").lower()
    web = (row["web"] or "").lower()
    email = (row["email"] or "").lower()
    nombre = (row["nombre"] or "").lower()
    mod = (row["modalidades"] or "").lower()

    # 1. Segmento ganador del Panel de 100 Dueños: Operador Receptivo / Aventura / Boutique
    if "operador" in clase:
        score += 35
    elif "minorista" in clase:
        score += 15
    if "receptivo" in tipo or "aventura" in mod or "turismo de aventura" in mod:
        score += 20

    # 2. Señales de Agencia Boutique / Digital Joven (60% buy rate)
    if web and ("http" in web or "www." in web or "." in web):
        score += 25
    domain = email.split("@")[-1] if "@" in email else ""
    if domain and domain not in FREE_DOMAINS:
        score += 25  # Correo corporativo propio = empresa formalizada digitalmente
    if any(kw in nombre for kw in BOUTIQUE_KW):
        score += 15
    if row["rep_legal"]:
        score += 10
    if row["telefono"]:
        score += 5
    return score


def parse_cusco_xlsx():
    sent_emails = set()
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG, "r", encoding="utf-8") as f:
            log = json.load(f)
            for v in log.values():
                if v.get("email"):
                    sent_emails.add(v["email"].strip().lower())

    rows = []
    seen_emails = set()
    with zipfile.ZipFile(XLSX_PATH) as z:
        sheet_name = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")][0]
        header = []
        for idx, (_, el) in enumerate(ET.iterparse(z.open(sheet_name), events=("end",))):
            if not el.tag.endswith("}row"):
                continue
            vals = ["".join(t.text or "" for t in c.iter() if t.tag.endswith("}t") or t.tag.endswith("}v")).strip() for c in el]
            el.clear()
            if not header:
                header = vals
                continue
            if len(vals) < 12:
                continue
            ubigeo = vals[4]
            if "cusco" not in ubigeo.lower():
                continue

            raw_email = vals[6].strip().lower().split(";")[0].split(",")[0].split()[0] if vals[6].strip() else ""
            if not EMAIL_RE.match(raw_email):
                continue
            if raw_email in seen_emails or raw_email in sent_emails:
                continue
            seen_emails.add(raw_email)

            rec = {
                "ruc": vals[0],
                "razon_social": vals[1],
                "nombre": vals[2] or vals[1],
                "direccion": vals[3],
                "ubigeo": ubigeo,
                "telefono": vals[5],
                "email": raw_email,
                "web": vals[7],
                "clase": vals[8],
                "rep_legal": vals[11] if len(vals) > 11 else "",
                "saludo_nombre": clean_first_name(vals[11] if len(vals) > 11 else ""),
                "tipo": vals[13] if len(vals) > 13 else "",
                "modalidades": vals[15] if len(vals) > 15 else "",
            }
            rec["score"] = score_agency(rec)
            rows.append(rec)

    rows.sort(key=lambda r: (-r["score"], r["nombre"]))
    return rows


def build_optimized_email_html(sample_agency):
    with open(TEMPLATE_IN, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Reemplazar el <details> (que no abre en Gmail/Zoho/Outlook) por una caja siempre visible y limpia
    details_pattern = re.compile(r"<!-- DESPLEGABLE DE CERTIFICACIONES VERIFICABLES -->.*?</details>", re.S)
    visible_certs = """<!-- CERTIFICACIONES VERIFICABLES (SIEMPRE VISIBLE EN GMAIL/ZOHO/OUTLOOK) -->
                    <div style="background-color:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px;">
                      <div style="font-size:12.5px; font-weight:800; color:#c2410c; margin-bottom:8px;">
                        Certificaciones Verificables en Turismo Inteligente, IA y Ciberseguridad:
                      </div>
                      <div style="font-size:12px; line-height:1.6; color:#334155;">
                        • <strong>Innovandes Cusco 2024 (U. Andina / PROInnóvate):</strong> 1.er Puesto (Capital Semilla S/ 15,000)<br/>
                        • <strong>UNI – StartUP UNI (Lima):</strong> 3.er Puesto e Incubación en Tecnología Turística [<code>SGDUNI 6862-2026</code>]<br/>
                        • <strong>UNSAAC – Paqarina Wasi / PROInnóvate:</strong> Cusco Startup Lab 2025 [<code>N.º 013-2025</code>]<br/>
                        • <strong>Anthropic &amp; Qdrant:</strong> Model Context Protocol (MCP) · AI Fluency for Small Businesses · Qdrant Essentials 100%<br/>
                        • <strong>AWS, Google Cloud &amp; Ciberseguridad:</strong> 9 certificaciones AWS AI · MLOps Google Cloud · OWASP Top 10 (Linux Foundation)
                      </div>
                    </div>"""
    html = details_pattern.sub(visible_certs, html)

    # 2. Inyectar Bloque Anti-Objeciones del Panel de 100 Dueños (Confianza, Privacidad Local, Demo 3 min, Cero Mensualidades)
    anti_obj_block = f"""
        <!-- BLOQUE ANTI-OBJECIONES VALIDADO CON 90 DUEÑOS DE AGENCIAS EN CUSCO -->
        <tr>
          <td class="mobile-pad" style="padding:18px 28px 6px 28px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#fff7ed; border:2px solid #f97316; border-radius:10px;">
              <tr>
                <td style="padding:16px 18px; font-size:13.5px; line-height:1.6; color:#1c1917;">
                  <div style="font-size:12px; font-weight:800; color:#c2410c; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;">
                    3 Garantías Directas para {sample_agency['nombre']} (Sin Riesgo ni Letra Chica)
                  </div>
                  • <strong>Demo en vivo de 3 minutos con TU propio tarifario:</strong> Antes de invertir en el programa completo, en nuestra reunión de diagnóstico (15 min) ves en vivo cómo generamos una cotización real en PDF (S/ y USD) sin errores de horarios ni precios.<br/>
                  • <strong>100% Privacidad Local (Ley N.º 29733):</strong> Tus tarifarios confidenciales y datos de pasajeros <strong>nunca salen a entrenar modelos públicos</strong>; quedan aislados en el Qdrant privado de tu propia agencia.<br/>
                  • <strong>Cero mensualidades ocultas con Lifextreme:</strong> Pagas una sola vez por capacitar y dejar operando a tu equipo (puedes empezar con la <strong>Sesión Piloto In-Office de 2 horas a S/ 490</strong>, 100% descontable del programa).
                </td>
              </tr>
            </table>
          </td>
        </tr>
"""
    # Insertar justo antes del primer botón o tras el saludo principal
    marker = "<!-- WRAPPER"
    if "<!-- BLOQUE 1" in html:
        html = html.replace("<!-- BLOQUE 1", anti_obj_block + "\n        <!-- BLOQUE 1", 1)
    else:
        # Insert after first </tr> inside email-container
        html = html.replace("</tr>", "</tr>" + anti_obj_block, 1)

    # 3. Asegurar URLs absolutas a produccion
    html = html.replace('href="../agendar-capacitacion.html', 'href="https://www.lifextreme.com.pe/agendar-capacitacion.html')
    html = html.replace('href="agendar-capacitacion.html', 'href="https://www.lifextreme.com.pe/agendar-capacitacion.html')
    html = html.replace('src="assets/', 'src="https://www.lifextreme.com.pe/reportes_b2b/assets/')
    html = html.replace('href="assets/', 'href="https://www.lifextreme.com.pe/reportes_b2b/assets/')

    return html


def main():
    rows = parse_cusco_xlsx()
    print(f"Total agencias Cusco limpias y únicas (excluyendo Lote 1): {len(rows)}")

    # Save clean master CSV
    fields = ["score", "nombre", "saludo_nombre", "email", "web", "clase", "tipo", "telefono", "ruc", "rep_legal", "ubigeo"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # Top 50 Target (Boutique / Operadores Receptivos con correo corporativo + web)
    top50 = rows[:50]
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(top50, f, ensure_ascii=False, indent=2)

    # Build preview page with optimized email + table of the 50 selected target agencies
    sample = top50[0]
    email_html = build_optimized_email_html(sample)
    table_rows = "\n".join(
        f"<tr><td>{i}</td><td><strong>{r['nombre']}</strong></td><td>{r['saludo_nombre']}</td><td>{r['email']}</td><td>{r['clase']}</td><td>{r['score']}</td></tr>"
        for i, r in enumerate(top50, 1)
    )

    preview_page = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Revisión Lote 2 (50 Agencias Target Cusco) · Lifextreme</title>
  <style>
    body {{ margin:0; font-family:'Segoe UI', Arial, sans-serif; background:#020618; color:#f8fafc; }}
    .top-bar {{ background:linear-gradient(90deg,#ff8e1d,#f43f5e); color:#020618; padding:16px 28px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }}
    .top-bar h1 {{ margin:0; font-size:18px; font-weight:900; }}
    .grid {{ display:grid; grid-template-columns: 1.15fr 0.85fr; gap:20px; padding:20px; max-width:1600px; margin:0 auto; }}
    @media (max-width:1100px) {{ .grid {{ grid-template-columns:1fr; }} }}
    .panel {{ background:#0f1324; border:1px solid #2a3148; border-radius:14px; padding:18px; overflow:hidden; }}
    .panel h2 {{ margin:0 0 12px 0; font-size:15px; color:#ff8e1d; text-transform:uppercase; }}
    iframe {{ width:100%; height:780px; border:1px solid #2a3148; border-radius:10px; background:#ffffff; }}
    .table-wrap {{ max-height:780px; overflow-y:auto; }}
    table {{ width:100%; border-collapse:collapse; font-size:12.5px; }}
    th, td {{ padding:8px 10px; border-bottom:1px solid #1e293b; text-align:left; }}
    th {{ background:#020618; color:#94a4bb; position:sticky; top:0; }}
  </style>
</head>
<body>
  <div class="top-bar">
    <div>
      <h1>REVISIÓN PREVIA LOTE 2 · TOP 50 AGENCIAS TARGET (OPERADORES &amp; BOUTIQUE CUSCO)</h1>
      <div style="font-size:12.5px; font-weight:700;">Asunto: &ldquo;{{nombre}}, el sistema de IA que estamos instalando en agencias de Cusco&rdquo; · Incluye garantías validadas en Panel de 100 Dueños</div>
    </div>
    <div style="font-weight:900; font-size:13px;">Base limpia total Cusco: {len(rows)} agencias</div>
  </div>
  <div class="grid">
    <div class="panel">
      <h2>1. Vista previa del correo optimizado (ejemplo: {sample['nombre']})</h2>
      <iframe id="emailFrame"></iframe>
    </div>
    <div class="panel">
      <h2>2. Top 50 Agencias Seleccionadas (Score Target: Correo Corporativo + Web + Operador)</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>#</th><th>Agencia</th><th>Saludo</th><th>Correo</th><th>Clase</th><th>Score</th></tr></thead>
          <tbody>{table_rows}</tbody>
        </table>
      </div>
    </div>
  </div>
  <script>
    const htmlContent = {json.dumps(email_html, ensure_ascii=False)};
    document.getElementById('emailFrame').srcdoc = htmlContent;
  </script>
</body>
</html>"""

    with open(PREVIEW_OUT, "w", encoding="utf-8") as f:
        f.write(preview_page)

    print(f"CSV maestro: {OUT_CSV}")
    print(f"Top 50 JSON: {OUT_JSON}")
    print(f"Preview HTML: {PREVIEW_OUT}")
    print("Top 5 muestra:")
    for r in top50[:5]:
        print(f"  [{r['score']} pts] {r['nombre']} ({r['saludo_nombre']}) -> {r['email']} | {r['clase']}")


if __name__ == "__main__":
    main()
