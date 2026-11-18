import argparse
import json
import os
import random
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

ZOHO_HOST = os.getenv("ZOHO_HOST", "smtp.zoho.com")
ZOHO_PORT = int(os.getenv("ZOHO_PORT", "465"))
ZOHO_USER = os.getenv("ZOHO_USER", "contacto@lifextreme.com.pe")
ZOHO_PASS = os.getenv("ZOHO_PASS", "")
PUBLIC_BASE_URL = os.getenv("LIFEXTREME_PUBLIC_URL", "https://www.lifextreme.com.pe")

PROSPECTS_JSON = "reportes_b2b/prospectos_top10_piloto.json"
EMAILS_DIR = "reportes_b2b/emails_personalizados"
LOG_PATH = "reportes_b2b/envios_piloto_log.json"


def build_subject(p):
    err = (p.get("audit") or {}).get("error") or ""
    if "502" in err or "500" in err:
        return f"{p['saludo_nombre']}, revisé la web de {p['agencia']} hoy (error detectado) + propuesta Cusco"
    return f"{p['saludo_nombre']}, diagnóstico rápido de {p['agencia']} + Claude Cowork In-Office (Cusco)"


def prepare_email_html(raw_html):
    """Convierte enlaces relativos locales a URLs absolutas para clientes de correo."""
    base = PUBLIC_BASE_URL.rstrip("/")
    html = raw_html.replace('href="../../agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    html = html.replace('href="../agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    html = html.replace('src="../assets/', f'src="{base}/reportes_b2b/assets/')
    html = html.replace('href="../assets/', f'href="{base}/reportes_b2b/assets/')
    return html


def load_sent_log():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sent_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def send_via_zoho(to_email, subject, html_body, plain_fallback):
    if not ZOHO_USER or not ZOHO_PASS:
        raise RuntimeError(
            "Falta ZOHO_PASS en tu archivo .env (ZOHO_USER=contacto@lifextreme.com.pe, ZOHO_PASS=<App Password de Zoho>)."
        )

    msg = MIMEMultipart("alternative")
    msg["From"] = f"Engelberth Egoavil · Lifextreme <{ZOHO_USER}>"
    msg["To"] = to_email
    msg["Reply-To"] = ZOHO_USER
    msg["Subject"] = subject

    msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL(ZOHO_HOST, ZOHO_PORT, timeout=20) as server:
        server.login(ZOHO_USER, ZOHO_PASS)
        server.sendmail(ZOHO_USER, [to_email], msg.as_string())


def main():
    parser = argparse.ArgumentParser(description="Automatización de envío B2B vía Zoho SMTP (contacto@lifextreme.com.pe)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Valida destinatarios, asuntos y HTML sin enviar (por defecto)")
    mode.add_argument("--test", metavar="EMAIL", help="Envía 1 correo de prueba al email indicado")
    mode.add_argument("--send", action="store_true", help="Envía la campaña real a los prospectos pendientes")
    parser.add_argument("--prospects", default=PROSPECTS_JSON, help="Ruta al JSON de prospectos (ej. reportes_b2b/prospectos_lote2_piloto.json)")
    parser.add_argument("--limit", type=int, default=10, help="Máximo de correos a enviar en esta ejecución (default: 10)")
    parser.add_argument("--delay-min", type=int, default=15, help="Segundos mínimos entre envíos (default: 15)")
    parser.add_argument("--delay-max", type=int, default=30, help="Segundos máximos entre envíos (default: 30)")
    args = parser.parse_args()

    if not args.test and not args.send:
        args.dry_run = True

    with open(args.prospects, "r", encoding="utf-8") as f:
        prospects = json.load(f)

    sent_log = load_sent_log()

    if args.test:
        p = prospects[0]
        html_path = os.path.join(EMAILS_DIR, f"{p['slug']}.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            html_body = prepare_email_html(hf.read())
        subject = f"[PRUEBA] {build_subject(p)}"
        plain = f"Hola {p['saludo_nombre']}, preparamos un diagnóstico para {p['agencia']} y nuestra capacitación In-Office Claude Cowork en Cusco."
        print(f"[TEST] Enviando prueba de '{p['agencia']}' a {args.test} desde {ZOHO_USER}...")
        send_via_zoho(args.test, subject, html_body, plain)
        print("[OK] Correo de prueba enviado correctamente.")
        return

    sent_count = 0
    for idx, p in enumerate(prospects, 1):
        if sent_count >= args.limit:
            break
        slug = p["slug"]
        to_email = p["email"].strip()
        subject = build_subject(p)
        html_path = os.path.join(EMAILS_DIR, f"{slug}.html")

        if slug in sent_log and sent_log[slug].get("status") == "sent":
            print(f"[{idx}/10] SKIP (ya enviado): {p['agencia']} -> {to_email}")
            continue

        if not os.path.exists(html_path):
            print(f"[{idx}/10] ERROR: falta {html_path}")
            continue

        with open(html_path, "r", encoding="utf-8") as hf:
            html_body = prepare_email_html(hf.read())

        if args.dry_run:
            print(f"[DRY-RUN {idx}/10] {p['agencia']} | Para: {to_email} | Asunto: {subject} | HTML: {len(html_body)} bytes")
            continue

        plain = (
            f"Hola {p['saludo_nombre']} ({p['agencia']}),\n\n"
            f"Revisamos {p['web']} y preparamos una propuesta In-Office en Cusco para tu equipo (5 a 10 personas): "
            f"Claude Cowork en laptops, Skills PDF para itinerarios, Calendar/Drive, Higgsfield, Claude Design/Code y tu propio RAG en Qdrant.\n\n"
            f"Agenda 15 min aquí: {PUBLIC_BASE_URL.rstrip('/')}/agendar-capacitacion.html"
        )
        try:
            print(f"[{idx}/10] Enviando a {to_email} ({p['agencia']})...")
            send_via_zoho(to_email, subject, html_body, plain)
            sent_log[slug] = {
                "email": to_email,
                "subject": subject,
                "status": "sent",
                "sent_at": datetime.now().isoformat(),
            }
            save_sent_log(sent_log)
            sent_count += 1
            print(f"  [OK] Enviado.")
            if idx < len(prospects) and sent_count < args.limit:
                wait_s = random.randint(args.delay_min, args.delay_max)
                print(f"  Esperando {wait_s}s anti-spam...")
                time.sleep(wait_s)
        except Exception as e:
            print(f"  [ERROR] {e}")
            sent_log[slug] = {
                "email": to_email,
                "subject": subject,
                "status": "error",
                "error": str(e),
                "attempted_at": datetime.now().isoformat(),
            }
            save_sent_log(sent_log)

    if args.dry_run:
        print(f"\n[DRY-RUN COMPLETO] {len(prospects)} correos validados. Remitente configurado: {ZOHO_USER} ({ZOHO_HOST}:{ZOHO_PORT}).")
        print("Para enviar una prueba: .\\.venv\\Scripts\\python.exe scripts\\enviar_campana_piloto_zoho.py --test contacto@lifextreme.com.pe")
        print("Para enviar los 10:      .\\.venv\\Scripts\\python.exe scripts\\enviar_campana_piloto_zoho.py --send")


if __name__ == "__main__":
    main()
