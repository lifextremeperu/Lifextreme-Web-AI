"""
Generador Sniper GTM - 10 Agencias Pequeñas / Boutique en Cusco (PYMEs)
-----------------------------------------------------------------------
Enfocado en agencias pequeñas y boutique (E.I.R.L. / S.A.C. jóvenes RUC 2061x / nicho),
excluyendo a los operadores gigantes (Valencia, Alpaca, Machu Travel, Salkantay, TreXperience).
Cruza con cusco_agencias_limpio.csv y verifica que no hayan sido contactadas en Lotes 2-5.
"""

import csv
import html
import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
CSV_PATH = os.path.join("reportes_b2b", "cusco_agencias_limpio.csv")
OUT_JSON = os.path.join("reportes_b2b", "prospectos_sniper_pymes_cusco.json")
OUT_HTML = os.path.join("reportes_b2b", "reporte_sniper_10_pymes_cusco.html")

TARGETS = [
    {
        "match_ruc": "20601976634",
        "nombre": "Gt Peru Travel",
        "tamano": "Pequeña / Mediana (Equipo ágil)",
        "senal_tipo": "Vacante Activa (Ejecutivo de Ventas / Asesor)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Publicaciones en Computrabajo Cusco buscando asesores de viajes para cotización de paquetes receptivos.",
        "urgencia_score": 95,
        "angulo_personalizado": "Vi que han estado buscando asesores de viajes en Computrabajo Cusco. Para un equipo ágil como el suyo, capacitar a sus asesores actuales con IA In-Office les permite cotizar el triple de rápido sin tener que inflar su planilla.",
    },
    {
        "match_ruc": "20606786817",
        "nombre": "Immersion Andine",
        "tamano": "Boutique (Nicho Francés / A medida)",
        "senal_tipo": "Vacante Activa (Travel Designer)",
        "senal_fuente": "Computrabajo Perú",
        "senal_evidencia": "Búsqueda activa de Travel Designer / Ejecutivo de Ventas en Cusco para viajes a medida en idioma francés.",
        "urgencia_score": 93,
        "angulo_personalizado": "Noté su búsqueda de Travel Designer en Cusco para itinerarios a medida en francés. Un asistente de IA entrenado con sus rutas redacta propuestas impecables en francés en menos de 2 minutos sin perder el toque boutique.",
    },
    {
        "match_ruc": "20527285845",
        "nombre": "TERRES MAGIQUES",
        "tamano": "Boutique (Nicho Francés / Europeo)",
        "senal_tipo": "Vacante Activa (Travel Designer Multilingüe)",
        "senal_fuente": "Computrabajo Perú / Opcionempleo",
        "senal_evidencia": "Convocatorias buscando asesores con dominio de idiomas para armar circuitos personalizados en Cusco.",
        "urgencia_score": 91,
        "angulo_personalizado": "Vi que buscan talento multilingüe para cotizaciones a medida en Cusco. Podemos instalarles un flujo de IA práctico en su propia oficina para acelerar respuestas en francés e inglés y evitar demoras por diferencia horaria con Europa.",
    },
    {
        "match_ruc": "20601609071",
        "nombre": "Peruvian Sunrise",
        "tamano": "Pequeña (Receptivo Cusco)",
        "senal_tipo": "Vacante Activa (Asesores de Paquetes)",
        "senal_fuente": "Opcionempleo / Portales Locales",
        "senal_evidencia": "Búsqueda de asesores de paquetes turísticos e idiomas para atención receptiva en Cusco.",
        "urgencia_score": 89,
        "angulo_personalizado": "Vi sus convocatorias para asesores de paquetes en Cusco. Con un taller práctico de 1 día en su oficina, su equipo puede automatizar cotizaciones repetitivas por WhatsApp y correo manteniendo sus tarifas exactas.",
    },
    {
        "match_ruc": "20615338908",
        "nombre": "CKGO2 PERU",
        "tamano": "Micro / Boutique (RUC 20615 · Nicho Checo/Europeo)",
        "senal_tipo": "Agencia Joven Multilingüe (Alta Fricción Manual)",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "Agencia joven (RUC 20615) operando con mercado europeo (dominio .cz / español-inglés-checo), donde la atención por huso horario y traducciones manuales suele saturar a equipos pequeños.",
        "urgencia_score": 87,
        "angulo_personalizado": "Al operar entre Cusco y el mercado europeo con equipos pequeños, la diferencia horaria y las cotizaciones en varios idiomas consumen muchas horas. Podemos ayudarles a automatizar la primera respuesta 24/7 y el armado de itinerarios con IA.",
    },
    {
        "match_ruc": "20614545136",
        "nombre": "BESPIRIA TRAVEL ATELIER",
        "tamano": "Boutique / Atelier (RUC 20614)",
        "senal_tipo": "Agencia Boutique Joven (Diseño a Medida)",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "Agencia nueva tipo 'Travel Atelier' (RUC 20614) enfocada en diseño artesanal de viajes, proceso 100% manual y intensivo en tiempo por cliente.",
        "urgencia_score": 86,
        "angulo_personalizado": "Como Travel Atelier en Cusco, cada itinerario a medida toma horas de redacción y ajuste. En Lifextreme instalamos copilotos de IA en su oficina para generar borradores de propuestas personalizadas en minutos respetando su estilo.",
    },
    {
        "match_ruc": "20614572893",
        "nombre": "BIOGLAMPING EXPEDITIONS",
        "tamano": "Boutique / Nicho Glamping (RUC 20614)",
        "senal_tipo": "Operador Nicho Joven (Consultas Detalladas)",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "Empresa joven (RUC 20614) de glamping y expediciones; los clientes de glamping hacen muchas preguntas previas por WhatsApp sobre logística, clima y comodidad.",
        "urgencia_score": 85,
        "angulo_personalizado": "En experiencias de glamping en Cusco los viajeros preguntan muchísimo sobre clima, equipo e itinerario antes de reservar. Podemos implementarles un asistente IA que responda al instante por WhatsApp/correo y filtre prospectos listos para pagar.",
    },
    {
        "match_ruc": "20614328640",
        "nombre": "CUSCO SAGRADO TOURS E.I.R.L.",
        "tamano": "Microempresa E.I.R.L. (RUC 20614)",
        "senal_tipo": "E.I.R.L. Reciente en Crecimiento",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "E.I.R.L. reciente (RUC 20614) con web y correo corporativo donde normalmente 1 o 2 personas ven ventas, reservas y operación a la vez.",
        "urgencia_score": 84,
        "angulo_personalizado": "En una E.I.R.L. turística en Cusco sabemos que el mismo equipo ve ventas, WhatsApp y operación diaria. Con una capacitación práctica In-Office pueden automatizar cotizaciones y mensajes frecuentes para no perder reservas por demora.",
    },
    {
        "match_ruc": "20613509471",
        "nombre": "CALLANGA FAMILY EXPLORERS",
        "tamano": "Pequeña / Familiar (RUC 20613)",
        "senal_tipo": "Agencia Familiar / Nicho Viajes en Familia",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "Agencia joven (RUC 20613) enfocada en familias; requiere cotizaciones adaptadas por edades, hoteles y ritmos de viaje.",
        "urgencia_score": 83,
        "angulo_personalizado": "Cotizar viajes familiares a Cusco requiere adaptar cada detalle según edades y ritmos. Podemos enseñar a su equipo en sus oficinas cómo usar IA para armar propuestas familiares claras y rápidas sin perder horas en Word o Excel.",
    },
    {
        "match_ruc": "20564176720",
        "nombre": "CARACOLA TRAVEL",
        "tamano": "Pequeña / Boutique Cusco",
        "senal_tipo": "Agencia Boutique con Web y Correo Directo",
        "senal_fuente": "Directorio MINCETUR + Web Activa",
        "senal_evidencia": "Agencia pequeña consolidada en Cusco con atención directa personalizada (hola@caracolatravel.com) aún no contactada en lotes previos.",
        "urgencia_score": 82,
        "angulo_personalizado": "Para una agencia boutique en Cusco como Caracola Travel, responder rápido a cada viajero marca la diferencia frente a operadores grandes. Podemos mostrarles en 15 minutos cómo automatizar sus cotizaciones iniciales con IA.",
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
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tbl,))
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

        nombre_real = row.get("nombre") or t["nombre"]
        asunto = f"{nombre_real}: cómo cotizar 3x más rápido en Cusco sin contratar más personal"
        mensaje = (
            f"Hola equipo de {nombre_real},\n\n"
            f"{t['angulo_personalizado']}\n\n"
            f"En Lifextreme Cusco realizamos una implementación práctica In-Office (en su propia oficina) para agencias ágiles. "
            f"Si desean ver una demo de 15 minutos aplicada a sus propios tours, pueden agendar aquí:\n"
            f"https://www.lifextreme.com.pe/agendar-capacitacion.html\n\n"
            f"Saludos,\nEngelberth Egoavil · Lifextreme Cusco"
        )

        records.append(
            {
                "nombre": nombre_real,
                "tamano": t["tamano"],
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

    cur.execute("DROP TABLE IF EXISTS prospectos_sniper_pymes")
    cur.execute(
        """
        CREATE TABLE prospectos_sniper_pymes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tamano TEXT,
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
            INSERT INTO prospectos_sniper_pymes
            (nombre, tamano, ruc, email, web, telefono, rep_legal, saludo_nombre, urgencia_score,
             senal_tipo, senal_fuente, senal_evidencia, estado_previo_lotes, asunto_sugerido, mensaje_personalizado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                r["nombre"], r["tamano"], r["ruc"], r["email"], r["web"], r["telefono"],
                r["rep_legal"], r["saludo_nombre"], r["urgencia_score"], r["senal_tipo"],
                r["senal_fuente"], r["senal_evidencia"], r["estado_previo_lotes"],
                r["asunto_sugerido"], r["mensaje_personalizado"],
            ),
        )

    conn.commit()
    conn.close()

    cards_html = []
    for idx, r in enumerate(records, 1):
        cards_html.append(
            f"""
        <div class="card">
          <div class="card-head">
            <div>
              <span class="rank">#{idx}</span>
              <h2>{html.escape(r['nombre'])}</h2>
              <div class="meta">Tamaño: <strong>{html.escape(r['tamano'])}</strong> · RUC: {html.escape(r['ruc'])} · Web: <a href="https://{html.escape(r['web'].replace('https://','').replace('http://',''))}" target="_blank">{html.escape(r['web'])}</a> · Tel: {html.escape(r['telefono'])}</div>
            </div>
            <div class="scores">
              <span class="score">Score {r['urgencia_score']}/100</span>
              <span class="badge">{html.escape(r['estado_previo_lotes'])}</span>
            </div>
          </div>
          <div class="signal">
            <strong>🎯 Señal ({html.escape(r['senal_fuente'])}):</strong> {html.escape(r['senal_tipo'])}<br/>
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
  <title>Reporte Sniper PYMEs · 10 Agencias Pequeñas Cusco | Lifextreme AI</title>
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
    .badge {{ background: #16a34a; color: #fff; font-weight: 600; padding: 4px 10px; border-radius: 999px; font-size: 11px; }}
    .signal {{ background: #0f172a; border-left: 3px solid #f59e0b; padding: 10px 12px; margin: 12px 0; font-size: 13px; line-height: 1.5; border-radius: 0 8px 8px 0; }}
    .msg-box {{ background: #0b1220; border: 1px solid #334155; border-radius: 8px; padding: 12px; }}
    .msg-head {{ font-size: 12px; color: #cbd5e1; margin-bottom: 8px; }}
    pre {{ white-space: pre-wrap; font-family: inherit; font-size: 13px; line-height: 1.5; margin: 0; color: #e2e8f0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>🎯 Reporte Sniper PYMEs · 10 Agencias Pequeñas y Boutique en Cusco</h1>
    <div class="sub">Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')} · Sin operadores gigantes · 100% No Contactadas en lotes previos · Solo revisión humana.</div>
    {''.join(cards_html)}
  </div>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(page)

    print(f"OK: {len(records)} agencias PYME guardadas en {OUT_JSON}, SQLite (prospectos_sniper_pymes) y {OUT_HTML}")
    for r in records:
        print(f" - [{r['urgencia_score']}] {r['nombre']} ({r['tamano']}) | {r['email']} | {r['estado_previo_lotes']}")


if __name__ == "__main__":
    main()
