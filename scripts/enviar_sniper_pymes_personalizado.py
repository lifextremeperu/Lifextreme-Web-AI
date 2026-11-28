"""
Envío Personalizado 1-a-1 · Sniper 10 Agencias PYMEs Cusco
-----------------------------------------------------------
Combina la plantilla visual oficial (email_presentacion_ia_agencias_cusco.html)
con el ángulo personalizado de cada una de las 10 agencias en prospectos_sniper_pymes,
enviando vía Resend con retardos humanos (90s-140s) y aviso a Telegram al finalizar.
"""

import argparse
import html
import json
import os
import random
import sqlite3
import sys
import time
from datetime import datetime
import httpx
from dotenv import load_dotenv

sys.stdout.reconfigure(line_buffering=True)
load_dotenv()

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
JSON_PATH = os.path.join("reportes_b2b", "prospectos_sniper_pymes_cusco.json")
TEMPLATE_PATH = os.path.join("reportes_b2b", "email_ejecutivo_corto_claude.html")
PREVIEW_PATH = os.path.join("reportes_b2b", "preview_correo_corto_claude.html")

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("RESEND_FROM", "Engelberth Egoavil · Lifextreme <contacto@lifextreme.com.pe>")
REPLY_TO = os.getenv("ZOHO_USER", "contacto@lifextreme.com.pe")
PUBLIC_BASE_URL = os.getenv("LIFEXTREME_PUBLIC_URL", "https://www.lifextreme.com.pe")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_telegram(text):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        httpx.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=20.0,
        )
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        t = f.read()
    base = PUBLIC_BASE_URL.rstrip("/")
    t = t.replace('href="../agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    t = t.replace('href="agendar-capacitacion.html', f'href="{base}/agendar-capacitacion.html')
    t = t.replace('src="assets/', f'src="{base}/reportes_b2b/assets/')
    t = t.replace('href="assets/', f'href="{base}/reportes_b2b/assets/')
    return t


BOLD_PHRASES = [
    "Un asistente de IA entrenado con sus rutas",
    "un flujo de IA práctico en su propia oficina",
    "un taller práctico de 1 día en su oficina",
    "automatizar la primera respuesta 24/7 y el armado de itinerarios con IA",
    "copilotos de IA en su oficina para generar borradores de propuestas personalizadas en minutos",
    "un asistente IA que responda al instante por WhatsApp/correo",
    "una capacitación práctica In-Office pueden automatizar cotizaciones y mensajes frecuentes",
    "usar IA para armar propuestas familiares claras y rápidas",
    "automatizar sus cotizaciones iniciales con IA",
    "capacitar a sus asesores actuales con IA In-Office",
]


def build_personalized_html(base_html, item, is_preview=False):
    nombre = item["nombre"]
    email = item["email"]
    angulo_html = html.escape(item["angulo_personalizado"])
    for phrase in BOLD_PHRASES:
        esc_p = html.escape(phrase)
        if esc_p in angulo_html:
            angulo_html = angulo_html.replace(esc_p, f"<strong>{esc_p}</strong>")

    base_url = ".." if is_preview else PUBLIC_BASE_URL.rstrip("/")
    landing_url = (
        "../agendar-capacitacion.html?utm_source=sniper_claude"
        if is_preview
        else f"{base_url}/agendar-capacitacion.html?utm_source=sniper_claude"
    )

    personalized = (
        base_html.replace("{{SALUDO_AGENCIA}}", f"Hola equipo de {html.escape(nombre)}:")
        .replace("{{ANGULO_PERSONALIZADO}}", angulo_html)
        .replace("{{EMAIL_AGENCIA}}", html.escape(email))
        .replace("{{NOMBRE_AGENCIA}}", html.escape(nombre))
        .replace("{{BASE_URL}}", base_url)
        .replace("{{LANDING_URL}}", landing_url)
    )
    return personalized


def build_plain(item):
    return (
        f"Hola equipo de {item['nombre']},\n\n"
        f"{item['angulo_personalizado']}\n\n"
        f"En Lifextreme Cusco estamos realizando diagnósticos prácticos de 15 minutos (en tu propia oficina o por Google Meet) "
        f"para mostrar en vivo cómo integrar Claude Cowork, Code y Design en las laptops de tu equipo.\n\n"
        f"• Ver los 6 módulos y agendar diagnóstico de 15 min:\n"
        f"  https://www.lifextreme.com.pe/agendar-capacitacion.html?utm_source=sniper_claude\n\n"
        f"• O escríbeme directo por Telegram (+51 958 050 928):\n"
        f"  https://t.me/+51958050928\n\n"
        f"Saludos cordiales,\nEngelberth Paolo Egoavil Palomino\nCEO · Lifextreme Cusco\ncontacto@lifextreme.com.pe\n"
    )


def send_via_resend(to_email, subject, html_body, plain_body):
    if not RESEND_API_KEY:
        raise RuntimeError("Falta RESEND_API_KEY en .env")
    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "reply_to": REPLY_TO,
        "subject": subject,
        "html": html_body,
        "text": plain_body,
        "headers": {
            "List-Unsubscribe": f"<mailto:{REPLY_TO}?subject=Baja>",
            "X-Entity-Ref-ID": f"cusco-sniper-{int(time.time())}",
        },
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--delay-min", type=int, default=90)
    parser.add_argument("--delay-max", type=int, default=140)
    args = parser.parse_args()

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Extraer ángulo personalizado limpio desde el mensaje guardado
    for it in items:
        parts = it["mensaje_personalizado"].split("\n\n")
        it["angulo_personalizado"] = parts[1] if len(parts) > 1 else it["senal_evidencia"]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    pending_emails = {
        r[0].strip().lower()
        for r in cur.execute(
            "SELECT email FROM prospectos_sniper_pymes WHERE estado != 'ENVIADO'"
        ).fetchall()
    }
    conn.close()

    to_process = [it for it in items if it["email"].strip().lower() in pending_emails]
    print(f"Agencias PYME listas para envío personalizado: {len(to_process)}/{len(items)}")

    if args.dry_run or not args.send:
        if to_process:
            base_html = load_template()
            preview_html = build_personalized_html(base_html, to_process[0], is_preview=True)
            with open(PREVIEW_PATH, "w", encoding="utf-8") as pf:
                pf.write(preview_html)
            print(f"[PREVIEW] Vista previa guardada en {PREVIEW_PATH}")
        for i, it in enumerate(to_process, 1):
            print(f" {i}. {it['nombre']} -> {it['email']}")
            print(f"    Asunto: {it['asunto_sugerido']}")
            print(f"    Intro:  {it['angulo_personalizado'][:110]}...")
        return

    base_html = load_template()
    sent_count = 0
    errors = 0
    consecutive_errors = 0

    send_telegram(f"🎯 *Iniciando envío Sniper Personalizado (10 PYMEs Cusco)*\nCada agencia recibirá la propuesta completa con apertura 1-a-1.")

    for i, it in enumerate(to_process, 1):
        em = it["email"].strip()
        subj = it["asunto_sugerido"]
        h_body = build_personalized_html(base_html, it)
        p_body = build_plain(it)

        print(f"\n[{i}/{len(to_process)}] Enviando propuesta personalizada a {it['nombre']} -> {em}...")
        try:
            res = send_via_resend(em, subj, h_body, p_body)
            rid = res.get("id")
            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "UPDATE prospectos_sniper_pymes SET estado = 'ENVIADO' WHERE email = ?",
                (em,),
            )
            conn.commit()
            conn.close()
            sent_count += 1
            consecutive_errors = 0
            print(f"    [ENVIADO] ID Resend: {rid}")
            if i < len(to_process):
                d = random.randint(args.delay_min, args.delay_max)
                print(f"    [PAUSA] Esperando {d}s...")
                time.sleep(d)
        except Exception as e:
            errors += 1
            consecutive_errors += 1
            print(f"    [ERROR] {e}")
            if consecutive_errors >= 2:
                print("[CIRCUIT BREAKER] Detenido por 2 errores consecutivos.")
                break

    send_telegram(
        f"✅ *SNIPER 10 PYMEs CUSCO FINALIZADO*\n"
        f"• Enviados personalizados: *{sent_count}/{len(to_process)}*\n"
        f"• Errores: *{errors}*"
    )
    print(f"\n[FIN] Enviados: {sent_count}/{len(to_process)} | Errores: {errors}")


if __name__ == "__main__":
    main()
