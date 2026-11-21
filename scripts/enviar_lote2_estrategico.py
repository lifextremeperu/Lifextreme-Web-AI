"""
Script de Envío Estratégico Anti-Bloqueo - Lote 2 (50 Agencias Cusco)
--------------------------------------------------------------------
Estrategia de Máxima Precaución:
1. Micro-lotes configurables (por defecto 10 correos por sesión).
2. Retardo con ruido humano aleatorio (90s a 180s) entre cada correo.
3. Envío individualizado 1 a 1 vía Resend API con dominio verificado (lifextreme.com.pe).
4. Persistencia local en SQLite (reportes_b2b/prospectos_cusco.db) para trazabilidad total e idempotencia.
5. Headers RFC 8058 (List-Unsubscribe) + pie de cortesía para evitar reportes de spam.
6. Circuit breaker: parada automática ante cualquier error consecutivo de reputación o límites.
"""

import argparse
import os
import random
import re
import sqlite3
import sys
import time
from datetime import datetime
import httpx
from dotenv import load_dotenv

sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
TEMPLATE_PATH = os.path.join("reportes_b2b", "email_presentacion_ia_agencias_cusco.html")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("RESEND_FROM", "Engelberth Egoavil · Lifextreme <contacto@lifextreme.com.pe>")
REPLY_TO = os.getenv("ZOHO_USER", "contacto@lifextreme.com.pe")
PUBLIC_BASE_URL = os.getenv("LIFEXTREME_PUBLIC_URL", "https://www.lifextreme.com.pe")


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def load_email_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    # Asegurar enlaces absolutos y activos a la página de agendar reunión
    base = PUBLIC_BASE_URL.rstrip("/")
    html = html.replace('href="../agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    html = html.replace('href="agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    html = html.replace('src="assets/', f'src="{base}/reportes_b2b/assets/')
    html = html.replace('href="assets/', f'href="{base}/reportes_b2b/assets/')
    return html


def personalize_email(template_html, agency_row):
    nombre_agencia = agency_row["nombre"]
    saludo_nombre = agency_row["saludo_nombre"] or "Director/a"
    
    # Saludo personalizado respetuoso y limpio
    if saludo_nombre and saludo_nombre.lower() not in ("director/a", "director", "directora"):
        saludo_text = f"Hola {saludo_nombre} ({nombre_agencia}):"
    else:
        saludo_text = f"Hola equipo de {nombre_agencia}:"
    
    html = template_html.replace("Estimado/a líder de agencia:", saludo_text)
    
    # Pie de cortesía anti-spam discreto
    optout_notice = f"""
    <!-- PIE DE CORTE CORTESIA Y PROTECCIÓN -->
    <tr>
      <td style="padding:14px 28px; background-color:#f5f5f4; border-top:1px solid #e7e5e4; font-size:11px; line-height:1.5; color:#78716c; text-align:center;">
        Este correo fue enviado de forma personalizada y directa a <strong>{agency_row['email']}</strong> ({nombre_agencia}) como parte de nuestra iniciativa de IA para agencias de turismo en Cusco.<br/>
        Si no deseas recibir más actualizaciones sobre innovación turística, por favor responde a este correo con la palabra <strong>BAJA</strong> y te retiraremos de inmediato.
      </td>
    </tr>
    """
    if "</table>" in html:
        # Insertar antes del cierre de la tabla principal
        html = html.replace("</table>\n      </td>\n    </tr>\n  </table>\n</body>", optout_notice + "\n        </table>\n      </td>\n    </tr>\n  </table>\n</body>")
    
    return html


def build_subject(agency_row):
    saludo = agency_row["saludo_nombre"] or agency_row["nombre"]
    if saludo and saludo.lower() in ("director/a", "director", "directora"):
        saludo = agency_row["nombre"]
    return f"{saludo}, el sistema de IA que estamos instalando en agencias de Cusco"


def build_plain_fallback(agency_row):
    saludo = agency_row["saludo_nombre"] or "Director/a"
    return f"""Hola {saludo} ({agency_row['nombre']}),

Desde Lifextreme Cusco preparamos una propuesta de capacitación práctica In-Office (en tus propias oficinas) para implementar Claude Cowork en tu equipo de ventas y operaciones.

Puedes conocer los detalles y agendar una breve reunión de diagnóstico de 15 minutos aquí:
https://www.lifextreme.com.pe/agendar-capacitacion.html

Saludos cordiales,
Engelberth Egoavil
Lifextreme · Cusco, Perú
contacto@lifextreme.com.pe
"""


def send_via_resend(to_email, subject, html_body, plain_body):
    if not RESEND_API_KEY:
        raise RuntimeError("Falta RESEND_API_KEY en las variables de entorno.")

    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": subject,
        "html": html_body,
        "text": plain_body,
        "headers": {
            "List-Unsubscribe": f"<mailto:{REPLY_TO}?subject=Baja>",
            "X-Entity-Ref-ID": f"cusco-lote2-{int(time.time())}"
        }
    }
    resp = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30.0,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Resend HTTP {resp.status_code}: {resp.text}")
    return resp.json()


def get_pending_prospects(limit=10, table="prospectos_lote2"):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table} WHERE estado = 'PENDIENTE' ORDER BY score DESC, id ASC LIMIT ?",
        (limit,)
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def update_prospect_status(prospect_id, estado, resend_id=None, error_msg=None, table="prospectos_lote2"):
    conn = get_db_connection()
    cur = conn.cursor()
    now_str = datetime.now().isoformat(timespec="seconds")
    cur.execute(
        f"""UPDATE {table} 
           SET estado = ?, resend_id = ?, error_msg = ?, enviado_at = ?, intentos = intentos + 1
           WHERE id = ?""",
        (estado, resend_id, error_msg, now_str if estado == "ENVIADO" else None, prospect_id)
    )
    conn.commit()
    conn.close()


def print_database_summary(table="prospectos_lote2"):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT estado, COUNT(*) FROM {table} GROUP BY estado")
    stats = dict(cur.fetchall())
    conn.close()
    lote_label = "LOTE 3" if "lote3" in table else "LOTE 2"
    print("=" * 60)
    print(f"ESTADO ACTUAL DE LA BASE DE DATOS LOCAL ({lote_label}):")
    print(f" • Pendientes: {stats.get('PENDIENTE', 0)}")
    print(f" • Enviados:   {stats.get('ENVIADO', 0)}")
    print(f" • Errores:    {stats.get('ERROR', 0)}")
    print(f" • Total:      {sum(stats.values())}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Envío Seguro y Anti-Bloqueo - Campañas B2B")
    parser.add_argument("--table", default="prospectos_lote2", choices=["prospectos_lote2", "prospectos_lote3"], help="Tabla de prospectos en SQLite (default: prospectos_lote2)")
    parser.add_argument("--batch-size", type=int, default=50, help="Cantidad máxima de correos a enviar en esta sesión (default: 50)")
    parser.add_argument("--micro-batch", type=int, default=10, help="Tamaño del micro-lote antes de una pausa larga (default: 10)")
    parser.add_argument("--batch-rest", type=int, default=300, help="Segundos de descanso entre micro-lotes (default: 300s = 5 min)")
    parser.add_argument("--delay-min", type=int, default=90, help="Retardo mínimo en segundos entre correos (default: 90s)")
    parser.add_argument("--delay-max", type=int, default=180, help="Retardo máximo en segundos entre correos (default: 180s)")
    parser.add_argument("--dry-run", action="store_true", help="Simulación previa sin realizar envíos")
    parser.add_argument("--status", action="store_true", help="Muestra el estado de la base de datos local y sale")
    parser.add_argument("--test", metavar="EMAIL", help="Envía un solo correo de prueba a la dirección especificada")
    parser.add_argument("--send", action="store_true", help="Ejecuta el envío real del micro-lote programado")

    args = parser.parse_args()

    if args.status:
        print_database_summary(table=args.table)
        return

    base_html = load_email_template()

    if args.test:
        test_agency = {
            "id": 0,
            "nombre": "Agencia de Prueba Cusco",
            "saludo_nombre": "Estimado/a",
            "email": args.test,
        }
        subject = f"[PRUEBA] {build_subject(test_agency)}"
        html_body = personalize_email(base_html, test_agency)
        plain_body = build_plain_fallback(test_agency)
        print(f"[TEST] Enviando correo de prueba a {args.test}...")
        res = send_via_resend(args.test, subject, html_body, plain_body)
        print(f"[OK] Prueba enviada con éxito! Resend ID: {res.get('id')}")
        return

    pending = get_pending_prospects(limit=args.batch_size, table=args.table)
    if not pending:
        print("[INFO] No hay prospectos pendientes en la base de datos local. ¡Todos los correos han sido enviados!")
        print_database_summary(table=args.table)
        return

    print_database_summary(table=args.table)
    print(f"\n[PROGRAMACIÓN] Micro-lote seleccionado: {len(pending)} agencias")
    print(f"[ESTRATEGIA ANTI-BLOQUEO] Retardo entre envíos: {args.delay_min}s a {args.delay_max}s (ruido aleatorio)")

    if args.dry_run or not args.send:
        print("\n--- MODO SIMULACIÓN (DRY-RUN) --- (Usa --send para ejecutar realmente)")
        for idx, row in enumerate(pending, 1):
            sub = build_subject(row)
            print(f" {idx}. [{row['id']}] {row['nombre']} -> {row['email']} | Asunto: {sub}")
        return

    # MODO ENVÍO REAL
    consecutive_errors = 0
    sent_in_batch = 0

    for idx, row in enumerate(pending, 1):
        to_email = row["email"].strip()
        subject = build_subject(row)
        html_body = personalize_email(base_html, row)
        plain_body = build_plain_fallback(row)

        print(f"\n[{idx}/{len(pending)}] Procesando {row['nombre']} -> {to_email}...")

        try:
            res = send_via_resend(to_email, subject, html_body, plain_body)
            resend_id = res.get("id")
            update_prospect_status(row["id"], "ENVIADO", resend_id=resend_id, table=args.table)
            sent_in_batch += 1
            consecutive_errors = 0
            print(f"    [ENVIADO] ID Resend: {resend_id}")

            if idx < len(pending):
                if sent_in_batch % args.micro_batch == 0:
                    print(f"\n💤 [PAUSA ENTRE MICRO-LOTES] Completado bloque de {args.micro_batch}. Pausa estratégica de {args.batch_rest}s ({args.batch_rest // 60} min) para refrescar reputación...")
                    time.sleep(args.batch_rest)
                else:
                    delay = random.randint(args.delay_min, args.delay_max)
                    print(f"    [PAUSA ANTI-BLOQUEO] Esperando {delay} segundos antes del siguiente envío...")
                    time.sleep(delay)

        except Exception as e:
            err_msg = str(e)
            print(f"    [ERROR] Falló envío a {to_email}: {err_msg}")
            update_prospect_status(row["id"], "ERROR", error_msg=err_msg, table=args.table)
            consecutive_errors += 1

            if consecutive_errors >= 2:
                print("\n[CIRCUIT BREAKER] Se detectaron 2 errores consecutivos. Deteniendo ejecución preventiva para proteger reputación.")
                break

    print(f"\n[FIN DE SESIÓN] Correos enviados en este micro-lote: {sent_in_batch}")
    print_database_summary(table=args.table)


if __name__ == "__main__":
    main()
