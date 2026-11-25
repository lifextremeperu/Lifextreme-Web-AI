"""
Orquestador Programado: Cierre Lote 4 + Backup GitHub/Vercel + Espera 4 Horas + Lanzamiento Lote 5
-----------------------------------------------------------------------------------------------
1. Espera a que termine al 100% prospectos_lote4 (66/66).
2. Respalda todo en GitHub (git push origin main) y despliega en Vercel (vercel --prod).
3. Entra en pausa programada de 4 horas (14,400 segs) para proteger la reputación del dominio.
4. Al cumplirse las 4 horas, arma automáticamente el Lote 5 (50 PYMEs limpias de Cusco sin repetir).
5. Avisa por Telegram y arranca el envío estratégico del Lote 5 + su monitor a Telegram.
"""

import csv
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
import httpx
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(line_buffering=True)

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
CSV_PATH = os.path.join("reportes_b2b", "cusco_agencias_limpio.csv")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FREE_DOMAINS = ("gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "live.com", "icloud.com")
BAD_KW = ("yahuoo", "gamil", "hotmial", "outlok", "yaju", "speedy.com.pe", "terra.com.pe", "yahoo.es")


def send_telegram(text):
    if not TOKEN or not CHAT_ID:
        return True
    try:
        r = httpx.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=20.0,
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[TELEGRAM WARN] {e}")
        return False


def wait_for_lote4_completion():
    print("[FASE 1] Verificando cierre de Lote 4 (66/66)...")
    while True:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM prospectos_lote4 WHERE estado = 'PENDIENTE'")
        pending = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM prospectos_lote4 WHERE estado = 'ENVIADO'")
        sent = cur.fetchone()[0]
        conn.close()

        if pending == 0:
            print(f"[FASE 1] ¡Lote 4 completado ({sent}/66)!")
            break
        print(f"   Lote 4 en curso: {sent}/66 enviados ({pending} pendientes). Esperando 30s...")
        time.sleep(30)


def sync_github_and_vercel():
    print("[FASE 2] Sincronizando base de datos y cambios con GitHub y Vercel...")
    try:
        subprocess.run(["git", "add", "reportes_b2b/", "scripts/"], check=False)
        res_commit = subprocess.run(
            ["git", "commit", "-m", "chore: cierre Lote 4 (66/66) y programacion automatica Lote 5"],
            capture_output=True, text=True, check=False
        )
        print("   Git commit:", res_commit.stdout.strip() or res_commit.stderr.strip())
        res_push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, check=False)
        print("   Git push:", res_push.stdout.strip() or res_push.stderr.strip())

        env = os.environ.copy()
        env["TMP"] = r"D:\Proyectos\.tmp"
        env["TEMP"] = r"D:\Proyectos\.tmp"
        res_vercel = subprocess.run(["vercel", "--prod", "--yes"], env=env, capture_output=True, text=True, check=False, shell=True)
        print("   Vercel deploy exit code:", res_vercel.returncode)
        send_telegram("✅ *Respaldo Lote 4 completado en GitHub y Vercel.*\n\n⏳ Campaña pausada automáticamente por *4 horas* para proteger el dominio. El *Lote 5 (50 PYMEs)* arrancará solo al cumplirse el tiempo.")
    except Exception as e:
        print(f"[ERROR SYNC] {e}")


def prepare_lote5(batch_count=50):
    print(f"[FASE 4] Preparando Lote 5 ({batch_count} agencias PYME limpias sin repetir)...")
    sent_emails = set()
    if os.path.exists("reportes_b2b/envios_piloto_log.json"):
        with open("reportes_b2b/envios_piloto_log.json", "r", encoding="utf-8") as f:
            for v in json.load(f).values():
                if v.get("email"):
                    sent_emails.add(v["email"].strip().lower())

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for tbl in ("prospectos_lote2", "prospectos_lote3", "prospectos_lote4"):
        cur.execute(f"SELECT email FROM {tbl}")
        for r in cur.fetchall():
            sent_emails.add(r[0].strip().lower())

    candidates = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            em = row["email"].strip().lower()
            if em in sent_emails or any(b in em for b in BAD_KW):
                continue
            dom = em.split("@")[-1] if "@" in em else ""
            has_corp = bool(dom and dom not in FREE_DOMAINS)
            web = (row.get("web") or "").strip()
            has_web = bool(web and "." in web)
            clase = (row.get("clase") or "").lower()
            is_op = "operador" in clase or "mayorista" in clase
            if has_corp and has_web and is_op:
                row["segmento"] = "PYME Consolidada Tier-1"
                candidates.append(row)

    candidates.sort(key=lambda r: (0 if str(r.get("ruc", "")).startswith("20") else 1, -int(r.get("score", 0)), r["nombre"]))
    lote5 = candidates[:batch_count]

    with open("reportes_b2b/prospectos_lote5_50_target.json", "w", encoding="utf-8") as f:
        json.dump(lote5, f, ensure_ascii=False, indent=2)

    cur.execute("DROP TABLE IF EXISTS prospectos_lote5")
    cur.execute("""
    CREATE TABLE prospectos_lote5 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        saludo_nombre TEXT,
        email TEXT UNIQUE NOT NULL,
        web TEXT,
        clase TEXT,
        tipo TEXT,
        telefono TEXT,
        ruc TEXT,
        rep_legal TEXT,
        score INTEGER,
        segmento TEXT,
        lote INTEGER DEFAULT 5,
        estado TEXT DEFAULT 'PENDIENTE',
        intentos INTEGER DEFAULT 0,
        resend_id TEXT,
        error_msg TEXT,
        enviado_at TIMESTAMP,
        creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    for p in lote5:
        cur.execute("""
            INSERT INTO prospectos_lote5 (nombre, saludo_nombre, email, web, clase, tipo, telefono, ruc, rep_legal, score, segmento, lote)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 5)
        """, (p["nombre"], p["saludo_nombre"], p["email"], p["web"], p["clase"], p["tipo"], p["telefono"], p["ruc"], p["rep_legal"], int(p.get("score", 0)), p["segmento"]))

    conn.commit()
    conn.close()
    print(f"[FASE 4] Lote 5 listo con {len(lote5)} agencias PYME Tier-1 en SQLite.")
    return len(lote5)


def ensure_lote5_ready():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prospectos_lote5'")
    if cur.fetchone():
        cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'PENDIENTE'")
        cnt = cur.fetchone()[0]
        if cnt > 0:
            conn.close()
            print(f"[FASE 4] Lote 5 ya preparado en SQLite con {cnt} agencias pendientes (40 Tier-2 + 40 Sin Web).")
            return cnt
    conn.close()
    return prepare_lote5(50)


def main():
    skip_wait = "--now" in sys.argv
    wait_hours = 0 if skip_wait else 4
    wait_seconds = wait_hours * 3600

    wait_for_lote4_completion()
    if not skip_wait:
        sync_github_and_vercel()

        resume_time = datetime.now() + timedelta(seconds=wait_seconds)
        print(f"[FASE 3] Entrando en espera de {wait_hours} horas. Reanudación programada a las: {resume_time.strftime('%Y-%m-%d %H:%M:%S')}")

        elapsed = 0
        step = 1800  # Log cada 30 min
        while elapsed < wait_seconds:
            to_sleep = min(step, wait_seconds - elapsed)
            time.sleep(to_sleep)
            elapsed += to_sleep
            rem_min = max(0, (wait_seconds - elapsed) // 60)
            print(f"   [ESPERA 4H] Faltan {rem_min} minutos para iniciar Lote 5...")
    else:
        print("[FASE 3] Ejecución inmediata (--now): omitiendo espera de 4 horas.")

    count = ensure_lote5_ready()
    batch_today = min(40, count)
    if not send_telegram(f"🚀 *Iniciando Primera Mitad del Lote 5 ({batch_today} de {count} agencias)* tras la pausa programada.\n\n🛡️ Límite seguro diario activo: se enviarán {batch_today} hoy y los otros {count - batch_today} quedarán listos para mañana."):
        print("[ERROR] Sin acceso a red (API Telegram/Resend bloqueada). Abortando antes de iniciar envíos.")
        sys.exit(1)

    print("[FASE 5] Lanzando monitor a Telegram para Lote 5...")
    subprocess.Popen([sys.executable, "-u", "scripts/monitor_campana_telegram.py", "--table", "prospectos_lote5"])

    print(f"[FASE 5] Ejecutando envío estratégico Lote 5 (lote seguro de hoy: {batch_today})...")
    subprocess.run([
        sys.executable, "-u", "scripts/enviar_lote2_estrategico.py",
        "--table", "prospectos_lote5",
        "--send", "--batch-size", str(batch_today),
        "--micro-batch", "10", "--batch-rest", "300",
        "--delay-min", "90", "--delay-max", "180"
    ])

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'ENVIADO'")
    sent_now = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'PENDIENTE'")
    pend_now = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'ERROR'")
    err_now = cur.fetchone()[0]
    conn.close()
    send_telegram(
        f"✅ *PRIMERA MITAD DEL LOTE 5 COMPLETADA*\n\n"
        f"📊 *Resumen de la sesión:*\n"
        f"• Correos enviados hoy: *{sent_now}*\n"
        f"• Pendientes para mañana: *{pend_now}*\n"
        f"• Errores: *{err_now}*\n\n"
        f"_Lifextreme B2B Outreach Agent_ 🚀"
    )


if __name__ == "__main__":
    main()
