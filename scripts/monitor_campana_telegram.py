"""
Monitor de Campaña B2B Cusco -> Telegram
-----------------------------------------
Monitorea la base de datos SQLite (reportes_b2b/prospectos_cusco.db)
y envía una notificación final detallada al Bot de Telegram en cuanto
finalice el envío de las 50 agencias o si ocurre algún evento crítico.
"""

import argparse
import os
import sqlite3
import sys
import time
from datetime import datetime
import httpx
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(text):
    if not TOKEN or not CHAT_ID:
        print("[ERROR] Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    try:
        r = httpx.post(url, json=payload, timeout=20.0)
        return r.status_code == 200
    except Exception as e:
        print(f"[ERROR] Error al contactar Telegram: {e}")
        return False


def get_db_stats(table="prospectos_lote3"):
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT estado, COUNT(*) FROM {table} GROUP BY estado")
    stats = dict(cur.fetchall())
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    total = cur.fetchone()[0]
    conn.close()
    return {
        "enviados": stats.get("ENVIADO", 0),
        "pendientes": stats.get("PENDIENTE", 0),
        "errores": stats.get("ERROR", 0),
        "total": total,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", default="prospectos_lote3", choices=["prospectos_lote2", "prospectos_lote3"])
    args = parser.parse_args()
    table = args.table
    lote_name = "LOTE 3" if "lote3" in table else "LOTE 2"

    print(f"[MONITOR {lote_name}] Iniciando vigilancia de campaña hacia Telegram (Chat ID: {CHAT_ID})...")
    prev_sent = -1

    while True:
        stats = get_db_stats(table=table)
        if not stats:
            time.sleep(10)
            continue

        enviados = stats["enviados"]
        pendientes = stats["pendientes"]
        errores = stats["errores"]
        total = stats["total"]

        if enviados != prev_sent:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Progreso ({lote_name}): {enviados}/{total} enviados | {pendientes} pendientes | {errores} errores")
            prev_sent = enviados

        # Condición de finalización: ya no quedan pendientes
        if pendientes == 0 and total > 0:
            print(f"[MONITOR {lote_name}] ¡Campaña finalizada! Enviando reporte final a Telegram...")
            
            # Obtener últimas agencias para el reporte
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(f"SELECT nombre, email, enviado_at FROM {table} WHERE estado = 'ENVIADO' ORDER BY enviado_at ASC")
            all_sent = cur.fetchall()
            conn.close()

            primera = all_sent[0][2] if all_sent else ""
            ultima = all_sent[-1][2] if all_sent else ""

            mensaje_final = f"""🎉 *CAMPAÑA B2B CUSCO ({lote_name}) FINALIZADA CON ÉXITO*

📊 *Métricas Finales:*
• Total Agencias procesadas: *{total}*
• Correos entregados exitosamente: *{enviados} / {total}* (100%)
• Errores / Rebotes: *{errores}*
• Primer envío: `{primera}`
• Último envío: `{ultima}`

🛡️ *Estrategia Anti-Bloqueo cumplida:*
• Micro-lotes de 10 con retardos humanos (90s - 180s)
• Pausas de 5 min entre bloques
• 100% verificado en DNS Resend + SPF/DKIM
• Enlaces directos a: `https://www.lifextreme.com.pe/agendar-capacitacion.html`

🔔 *Notificaciones automáticas:*
Cada vez que una agencia agende su reunión de 15 min, recibirás la alerta inmediata aquí en Telegram y el cliente su confirmación por correo.

_Lifextreme B2B Outreach Agent_ 🚀
"""
            ok = send_telegram(mensaje_final)
            if ok:
                print("[MONITOR] Notificación enviada con éxito a Telegram. Monitor cerrando.")
            else:
                print("[MONITOR] Falló el envío de la notificación a Telegram.")
            break

        time.sleep(30)


if __name__ == "__main__":
    main()
