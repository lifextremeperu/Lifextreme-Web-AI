"""
Generador de Base de Datos Inicial y Reporte HTML - Sniper GTM (10 Agencias Cusco)
---------------------------------------------------------------------------------
Aplica el flujo del skill first-customer-finder-cusco:
1. Toma las 10 agencias verificadas con señales reales de contratación en Cusco.
2. Cruza sus datos con cusco_agencias_limpio.csv y prospectos_cusco.db (Lotes 2-5).
3. Guarda reportes_b2b/prospectos_sniper_cusco.json y la tabla prospectos_sniper_cusco.
4. Genera el reporte visual HTML reportes_b2b/reporte_sniper_10_agencias_cusco.html.
"""

import csv
import html
import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
CSV_PATH = os.path.join("reportes_b2b", "cusco_agencias_limpio.csv")
OUT_JSON = os.path.join("reportes_b2b", "prospectos_sniper_cusco.json")
OUT_HTML = os.path.join("reportes_b2b", "reporte_sniper_10_agencias_cusco.html")

TARGETS = [
    {
        "match_ruc": "20490589857",
        "nombre": "VALENCIA TRAVEL AGENCY",
        "senal_tipo": "Vacantes Activas (Ventas + Reservas + Tourplan)",
        "senal_fuente": "Computrabajo Perú / LinkedIn / Jobleads",
        "senal_evidencia": "Publicaciones recurrentes buscando Travel Designers / Sales Agents y Asistentes de Reservas con manejo de Tourplan, CRM e idiomas.",
        "urgencia_score": 98,
        "angulo_personalizado": "Vi que están ampliando su equipo de Travel Designers y Reservas (incluso pidiendo manejo de Tourplan y CRM). En agencias con ese volumen en Cusco, implementar asistentes de IA para pre-cotizar itinerarios y responder consultas multilingües reduce hasta en 70% la carga operativa de cada asesor.",
    },
    {
        "match_ruc": "20490478605",
        "nombre": "Machu Travel Peru",
        "senal_tipo": "Vacante Activa (Ejecutivo de Ventas / Travel Designer)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Búsqueda activa de Ejecutivos de Ventas / Travel Designers en Cusco para diseño de itinerarios a la medida y cotización en inglés/francés.",
        "urgencia_score": 95,
        "angulo_personalizado": "Noté su búsqueda de Travel Designers en Cusco para armar itinerarios a medida multilingües. Podemos capacitar a su equipo comercial en sus propias oficinas para generar propuestas personalizadas y cotizaciones en minutos con IA sin perder el toque humano.",
    },
    {
        "match_ruc": "20602716229",
        "nombre": "TREXPERIENCEPERU",
        "senal_tipo": "Vacante Activa (Travel Designer / Asesor de Paquetes)",
        "senal_fuente": "Computrabajo Perú / Opcionempleo",
        "senal_evidencia": "Convocatorias activas en Cusco para Ejecutivos de Ventas y Travel Designers orientados a paquetes a Machu Picchu y atención global por WhatsApp/correo.",
        "urgencia_score": 94,
        "angulo_personalizado": "Vi que están reclutando Travel Designers y asesores para atender solicitudes globales de Machu Picchu. Con un flujo de IA bien entrenado con sus tarifas y rutas, cada asesor puede atender el triple de cotizaciones por WhatsApp y correo en tiempo récord.",
    },
    {
        "match_ruc": "20490768948",
        "nombre": "Alpaca Expeditions",
        "senal_tipo": "Vacante Activa (Ejecutivos de Ventas / Asesores)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Reclutamiento activo en Cusco de Ejecutivos de Ventas y Asesores de Viajes para atención de pasajeros internacionales.",
        "urgencia_score": 92,
        "angulo_personalizado": "Al ver que siguen sumando asesores comerciales en Cusco para pasajeros internacionales, quería mostrarles cómo otras operaciones de alto flujo están usando IA In-Office para responder consultas iniciales y armar borradores de itinerarios en segundos.",
    },
    {
        "match_ruc": "20563961521",
        "nombre": "Salkantay Trekking E.I.R.L.",
        "senal_tipo": "Vacante Activa (Travel Sales / Reservas)",
        "senal_fuente": "LinkedIn / Jobleads",
        "senal_evidencia": "Búsqueda de talento en Cusco para Travel Sales y gestión de reservas/disponibilidad con proveedores y trenes.",
        "urgencia_score": 91,
        "angulo_personalizado": "Vi sus búsquedas en Cusco para el área de Travel Sales y Reservas. Justo ayudamos a operadores de trekking a automatizar el cruce de disponibilidad, seguimiento de cotizaciones y respuestas 24/7 para que su equipo se enfoque en cerrar ventas.",
    },
    {
        "match_ruc": "20601976634",
        "nombre": "Gt Peru Travel",
        "senal_tipo": "Vacante Activa (Ejecutivo de Ventas / Asesor)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Ofertas publicadas en Computrabajo Cusco para Ejecutivos de Ventas y Asesores de Viajes en turismo receptivo.",
        "urgencia_score": 89,
        "angulo_personalizado": "Vi que están buscando asesores de viajes en Computrabajo Cusco. Antes de cargar más horas hombre en cotizaciones repetitivas, podemos enseñar a su equipo actual en una sesión práctica de 15 minutos cómo multiplicar su velocidad de respuesta con IA.",
    },
    {
        "match_ruc": "20527285845",
        "nombre": "TERRES MAGIQUES",
        "senal_tipo": "Vacante Activa (Travel Designer Multilingüe)",
        "senal_fuente": "Computrabajo Perú / Opcionempleo",
        "senal_evidencia": "Reclutamiento de Ejecutivos de Ventas / Travel Designers en Cusco con dominio de idiomas (francés/inglés) para circuitos a medida.",
        "urgencia_score": 88,
        "angulo_personalizado": "Noté que buscan Travel Designers con dominio de francés e inglés en Cusco. Con IA entrenada con sus circuitos, su equipo puede redactar itinerarios impecables en varios idiomas en menos de 2 minutos sin errores de traducción.",
    },
    {
        "match_ruc": "20606786817",
        "nombre": "Immersion Andine",
        "senal_tipo": "Vacante Activa (Ejecutivo de Ventas / Travel Designer)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Publicación activa en Cusco buscando Ejecutivo de Ventas / Travel Designer para atención personalizada y cotización de paquetes.",
        "urgencia_score": 87,
        "angulo_personalizado": "Vi que están buscando Travel Designer en Cusco para reforzar la atención a medida. Podemos mostrarles cómo un copiloto de IA adaptado a sus rutas les ayuda a responder más rápido al mercado europeo sin perder personalización.",
    },
    {
        "match_ruc": "20601609071",
        "nombre": "Peruvian Sunrise",
        "senal_tipo": "Vacante Activa (Asesores de Paquetes / Idiomas)",
        "senal_fuente": "Opcionempleo / Portales de Turismo",
        "senal_evidencia": "Convocatorias para asesores de paquetes turísticos y cotización receptiva con idiomas para circuitos de Cusco y Machu Picchu.",
        "urgencia_score": 86,
        "angulo_personalizado": "Vi sus convocatorias para asesores de paquetes turísticos en Cusco. Tenemos un taller práctico presencial de 1 día para que su equipo automatice cotizaciones y respuestas frecuentes sin cambiar sus sistemas actuales.",
    },
    {
        "match_ruc": "20527976597",
        "nombre": "Tierras Vivas",
        "senal_tipo": "Operador Receptivo en Expansión Comercial",
        "senal_fuente": "Portales de Empleo Cusco / Directorio Oficial",
        "senal_evidencia": "Operador consolidado en Cusco con demanda constante de cotizaciones multi-día (Camino Inca / Salkantay) y atención multicanal.",
        "urgencia_score": 84,
        "angulo_personalizado": "Por el volumen de rutas multi-día que manejan en Cusco, un asistente de IA entrenado con sus programas les permite responder cotizaciones iniciales al instante en inglés y español mientras sus asesores cierran los grupos.",
    },
]


def main():
    csv_by_ruc = {}
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ruc = (row.get("ruc") or "").strip()
            if ruc and ruc not in csv_by_ruc:
                csv_by_ruc[ruc] = row

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    sent_map = {}
    for tbl in ("prospectos_lote2", "prospectos_lote3", "prospectos_lote4", "prospectos_lote5"):
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tbl,)
        )
        if not cur.fetchone():
            continue
        for em, est in cur.execute(f"SELECT email, estado FROM {tbl}").fetchall():
            sent_map[em.strip().lower()] = f"{tbl} ({est})"

    records = []
    for t in TARGETS:
        row = csv_by_ruc.get(t["match_ruc"], {})
        email = (row.get("email") or "").strip()
        web = (row.get("web") or "").strip()
        tel = (row.get("telefono") or "").strip()
        rep = (row.get("rep_legal") or "").strip()
        saludo = (row.get("saludo_nombre") or "").strip() or "Director/a"
        prev_status = sent_map.get(email.lower(), "NO CONTACTADO")

        asunto = f"{row.get('nombre', t['nombre'])}: automatización IA para su equipo de ventas/reservas en Cusco"
        mensaje = (
            f"Hola equipo de {row.get('nombre', t['nombre'])},\n\n"
            f"{t['angulo_personalizado']}\n\n"
            f"En Lifextreme Cusco estamos instalando estos flujos de forma práctica In-Office (en sus propias oficinas). "
            f"Si les interesa ver una demo en vivo de 15 minutos aplicada a sus propios paquetes, pueden agendar aquí:\n"
            f"https://www.lifextreme.com.pe/agendar-capacitacion.html\n\n"
            f"Saludos,\nEngelberth Egoavil · Lifextreme Cusco"
        )

        records.append(
            {
                "nombre": row.get("nombre") or t["nombre"],
                "ruc": t["match_ruc"],
                "email": email,
                "web": web,
                "telefono": tel,
                "rep_legal": rep,
                "saludo_nombre": saludo,
                "urgencia_score": t["urgencia_score"],
                "senal_tipo": t["senal_tipo"],
                "senal_fuente": t["senal_fuente"],
                "senal_evidencia": t["senal_evidencia"],
                "estado_previo_lotes": prev_status,
                "asunto_sugerido": asunto,
                "mensaje_personalizado": mensaje,
            }
        )

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    cur.execute("DROP TABLE IF EXISTS prospectos_sniper_cusco")
    cur.execute(
        """
        CREATE TABLE prospectos_sniper_cusco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ruc TEXT,
            email TEXT UNIQUE NOT NULL,
            web TEXT,
            telefono TEXT,
            rep_legal TEXT,
            saludo_nombre TEXT,
            urgencia_score INTEGER,
            senal_tipo TEXT,
            senal_fuente TEXT,
            senal_evidencia TEXT,
            estado_previo_lotes TEXT,
            asunto_sugerido TEXT,
            mensaje_personalizado TEXT,
            estado TEXT DEFAULT 'PENDIENTE_REVISION',
            creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for r in records:
        cur.execute(
            """
            INSERT INTO prospectos_sniper_cusco
            (nombre, ruc, email, web, telefono, rep_legal, saludo_nombre, urgencia_score,
             senal_tipo, senal_fuente, senal_evidencia, estado_previo_lotes, asunto_sugerido, mensaje_personalizado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r["nombre"],
                r["ruc"],
                r["email"],
                r["web"],
                r["telefono"],
                r["rep_legal"],
                r["saludo_nombre"],
                r["urgencia_score"],
                r["senal_tipo"],
                r["senal_fuente"],
                r["senal_evidencia"],
                r["estado_previo_lotes"],
                r["asunto_sugerido"],
                r["mensaje_personalizado"],
            ),
        )

    conn.commit()
    conn.close()

    cards_html = []
    for idx, r in enumerate(records, 1):
        badge_color = "#16a34a" if r["estado_previo_lotes"] == "NO CONTACTADO" else "#d97706"
        cards_html.append(
            f"""
        <div class="card">
          <div class="card-head">
            <div>
              <span class="rank">#{idx}</span>
              <h2>{html.escape(r['nombre'])}</h2>
              <div class="meta">RUC: {html.escape(r['ruc'])} · Web: <a href="https://{html.escape(r['web'].replace('https://','').replace('http://',''))}" target="_blank">{html.escape(r['web'])}</a> · Tel: {html.escape(r['telefono'])}</div>
            </div>
            <div class="scores">
              <span class="score">Score {r['urgencia_score']}/100</span>
              <span class="badge" style="background:{badge_color}">{html.escape(r['estado_previo_lotes'])}</span>
            </div>
          </div>
          <div class="signal">
            <strong>🎯 Señal detectada ({html.escape(r['senal_fuente'])}):</strong> {html.escape(r['senal_tipo'])}<br/>
            <span>{html.escape(r['senal_evidencia'])}</span>
          </div>
          <div class="msg-box">
            <div class="msg-head">
              <strong>✉️ Para:</strong> <code>{html.escape(r['email'])}</code> · <strong>Asunto:</strong> {html.escape(r['asunto_sugerido'])}
            </div>
            <pre>{html.escape(r['mensaje_personalizado'])}</pre>
          </div>
        </div>
        """
        )

    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Reporte Sniper GTM · 10 Agencias Cusco | Lifextreme AI</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; margin: 0; padding: 28px; }}
    .wrap {{ max-width: 1020px; margin: 0 auto; }}
    h1 {{ margin: 0 0 6px; font-size: 24px; color: #f8fafc; }}
    .sub {{ color: #94a3b8; margin-bottom: 24px; font-size: 14px; }}
    .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 18px; margin-bottom: 16px; }}
    .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; flex-wrap: wrap; }}
    .rank {{ background: #38bdf8; color: #0f172a; font-weight: 700; padding: 2px 8px; border-radius: 6px; font-size: 13px; margin-right: 8px; }}
    h2 {{ display: inline; font-size: 18px; margin: 0; color: #fff; }}
    .meta {{ font-size: 13px; color: #94a3b8; margin-top: 6px; }}
    .meta a {{ color: #38bdf8; text-decoration: none; }}
    .scores {{ display: flex; gap: 8px; align-items: center; }}
    .score {{ background: #0ea5e9; color: #fff; font-weight: 700; padding: 4px 10px; border-radius: 999px; font-size: 12px; }}
    .badge {{ color: #fff; font-weight: 600; padding: 4px 10px; border-radius: 999px; font-size: 11px; }}
    .signal {{ background: #0f172a; border-left: 3px solid #f59e0b; padding: 10px 12px; margin: 12px 0; font-size: 13px; line-height: 1.5; border-radius: 0 8px 8px 0; }}
    .msg-box {{ background: #0b1220; border: 1px solid #334155; border-radius: 8px; padding: 12px; }}
    .msg-head {{ font-size: 12px; color: #cbd5e1; margin-bottom: 8px; }}
    pre {{ white-space: pre-wrap; font-family: inherit; font-size: 13px; line-height: 1.5; margin: 0; color: #e2e8f0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>🎯 Reporte Sniper GTM · Top 10 Agencias de Turismo en Cusco</h1>
    <div class="sub">Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')} · Basado en señales reales de contratación (Computrabajo, Bumeran, LinkedIn, Opcionempleo) · Solo revisión humana (sin envío automático).</div>
    {''.join(cards_html)}
  </div>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"OK: {len(records)} agencias guardadas en {OUT_JSON}, SQLite (prospectos_sniper_cusco) y {OUT_HTML}")
    for r in records:
        print(f" - [{r['urgencia_score']}] {r['nombre']} | {r['email']} | {r['estado_previo_lotes']}")


if __name__ == "__main__":
    main()
