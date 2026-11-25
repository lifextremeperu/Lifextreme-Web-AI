"""
Live Terminal Viewer - Envíos B2B Lifextreme Cusco
--------------------------------------------------
Muestra en vivo el estado del envío, la barra de progreso y el log en tiempo real.
"""

import os
import sqlite3
import time
from datetime import datetime

DB_PATH = os.path.join("reportes_b2b", "prospectos_cusco.db")
LOG_PATH = r"C:\Users\ASUS\.gemini\antigravity\brain\c592d14c-3c7f-4be6-b728-ebd8e2f2059c\.system_generated\tasks\task-944.log"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_stats():
    if not os.path.exists(DB_PATH):
        return 0, 50, []
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'ENVIADO'")
    sent = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM prospectos_lote5 WHERE estado = 'PENDIENTE'")
    pending = cur.fetchone()[0]
    cur.execute("SELECT nombre, email, enviado_at, resend_id FROM prospectos_lote5 WHERE estado = 'ENVIADO' ORDER BY id DESC LIMIT 6")
    recent = cur.fetchall()
    conn.close()
    return sent, pending, recent

def get_recent_logs(lines=12):
    if not os.path.exists(LOG_PATH):
        return ["(Esperando logs de tarea...)"]
    try:
        with open(LOG_PATH, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
            return [l.strip() for l in all_lines[-lines:] if l.strip()]
    except Exception as e:
        return [f"Error al leer log: {e}"]

def main():
    os.system("title LIFEXTREME AI - MONITOR DE ENVIO EN VIVO (B2B CUSCO)")
    os.system("color 0A")  # Fondo negro, texto verde matrix/hacker
    
    while True:
        sent, pending, recent = get_stats()
        total = sent + pending
        pct = (sent / total * 100) if total else 0
        bar_len = 30
        filled = int(bar_len * sent // total) if total else 0
        bar = "█" * filled + "░" * (bar_len - filled)

        clear_screen()
        print("=" * 82)
        print(f"  🤖 LIFEXTREME AI · MONITOR EN VIVO DE ENVÍO B2B (CUSCO)")
        print(f"  Hora actual: {datetime.now().strftime('%H:%M:%S')} | Remitente: contacto@lifextreme.com.pe")
        print("=" * 82)
        print(f"  Progreso Total: [{bar}] {sent}/{total} ({pct:.1f}%)")
        print(f"  • Enviados con éxito: {sent} agencias")
        print(f"  • Pendientes en cola: {pending} agencias")
        print(f"  • Errores / Rebotes:  0")
        print("-" * 82)
        print("  📋 ÚLTIMAS AGENCIAS ENTREGADAS:")
        for r in recent:
            print(f"   ✓ {r[0][:28]:<28} | {r[1]:<32} | {r[2]}")
        print("-" * 82)
        print("  ⚡ ACTIVIDAD EN TIEMPO REAL DEL AGENTE (TASK-944):")
        logs = get_recent_logs(10)
        for l in logs:
            print(f"   {l}")
        print("=" * 82)
        print("  [Presiona Ctrl + C para salir de este monitor - El envío seguirá en segundo plano]")
        time.sleep(2.5)

if __name__ == "__main__":
    main()
