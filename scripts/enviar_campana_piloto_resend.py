import argparse
import json
import os
import random
import time
from datetime import datetime
import httpx
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("RESEND_FROM", "Engelberth Egoavil · Lifextreme <contacto@lifextreme.com.pe>")
REPLY_TO = os.getenv("ZOHO_USER", "contacto@lifextreme.com.pe")
PUBLIC_BASE_URL = os.getenv("LIFEXTREME_PUBLIC_URL", "https://www.lifextreme.com.pe")

PROSPECTS_JSON = "reportes_b2b/prospectos_top10_piloto.json"
EMAILS_DIR = "reportes_b2b/emails_personalizados"
LOG_PATH = "reportes_b2b/envios_piloto_log.json"


def build_subject(p):
    return f"{p['saludo_nombre']}, el sistema de IA que estamos instalando en agencias de Cusco"


def prepare_email_html(raw_html):
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


def send_via_resend(to_email, subject, html_body, plain_fallback, from_addr=FROM_EMAIL):
    if not RESEND_API_KEY:
        raise RuntimeError("Falta RESEND_API_KEY en tu archivo .env")

    payload = {
        "from": from_addr,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": subject,
        "html": html_body,
        "text": plain_fallback,
    }
    resp = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=25.0,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Resend HTTP {resp.status_code}: {resp.text}")
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Campaña piloto B2B vía Resend API")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Valida destinatarios y HTML sin enviar")
    mode.add_argument("--test", metavar="EMAIL", help="Envía 1 correo de prueba al email indicado")
    mode.add_argument("--send", action="store_true", help="Envía la campaña real a los prospectos pendientes")
    parser.add_argument("--from-onboarding", action="store_true", help="Usa onboarding@resend.dev para pruebas sin dominio verificado")
    parser.add_argument("--prospects", default=PROSPECTS_JSON)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--delay-min", type=int, default=5)
    parser.add_argument("--delay-max", type=int, default=12)
    args = parser.parse_args()

    if not args.test and not args.send:
        args.dry_run = True

    from_addr = "Lifextreme <onboarding@resend.dev>" if args.from_onboarding else FROM_EMAIL

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
        print(f"[TEST] Enviando prueba vía Resend ({from_addr}) -> {args.test}...")
        res = send_via_resend(args.test, subject, html_body, plain, from_addr=from_addr)
        print(f"[OK] Prueba enviada! ID: {res.get('id')}")
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

        if args.dry_run:
            print(f"[DRY-RUN {idx}/10] {p['agencia']} -> {to_email} | From: {from_addr}")
            continue

        with open(html_path, "r", encoding="utf-8") as hf:
            html_body = prepare_email_html(hf.read())
        plain = f"Hola {p['saludo_nombre']}, preparamos un diagnóstico rápido para {p['agencia']}."

        try:
            res = send_via_resend(to_email, subject, html_body, plain, from_addr=from_addr)
            sent_log[slug] = {
                "agencia": p["agencia"],
                "email": to_email,
                "subject": subject,
                "resend_id": res.get("id"),
                "status": "sent",
                "sent_at": datetime.now().isoformat(timespec="seconds"),
            }
            save_sent_log(sent_log)
            sent_count += 1
            print(f"[ENVIADO {idx}/10] {p['agencia']} -> {to_email} (ID: {res.get('id')})")
            if sent_count < args.limit and idx < len(prospects):
                wait_s = random.randint(args.delay_min, args.delay_max)
                time.sleep(wait_s)
        except Exception as e:
            sent_log[slug] = {
                "agencia": p["agencia"],
                "email": to_email,
                "status": "error",
                "error": str(e),
                "attempted_at": datetime.now().isoformat(timespec="seconds"),
            }
            save_sent_log(sent_log)
            print(f"[ERROR {idx}/10] {p['agencia']} -> {e}")

    print(f"[RESUMEN] Enviados en esta ejecución: {sent_count}")


if __name__ == "__main__":
    main()
