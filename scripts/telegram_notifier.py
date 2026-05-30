import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text: str):
    if not TOKEN or not CHAT_ID:
        print("⚠️ No se puede enviar Telegram: Faltan credenciales en .env")
        return False
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️ Error al enviar Telegram: {e}")
        return False

# =====================================================================
# PLANTILLAS BASADAS EN DMO-v2.0 (BLOQUE 5)
# =====================================================================

def notify_start(departamento, pais, run_id, tier, modulos_estimados):
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"""🚀 *PIPELINE INICIADO*

📍 *Destino:* {departamento}, {pais}
🆔 *Run ID:* `{run_id}`
⏰ *Inicio:* {timestamp}
📊 *Tier estimado:* {tier} ({modulos_estimados} módulos)

_Fase 1 — Cartógrafo en ejecución..._"""
    return send_message(msg)

def notify_fase1_complete(departamento, pais, total_modulos, modulos_human, canonicos, tokens, costo_usd):
    msg = f"""✅ *FASE 1 COMPLETADA — ÍNDICE GENERADO*

📍 {departamento}, {pais}
📋 *Módulos generados:* {total_modulos}
⚠️ *Requieren revisión humana:* {modulos_human}
🗂 *Destinos canónicos referenciados:* {canonicos}

💰 *Tokens Fase 1:* {tokens:,} ({costo_usd:.3f} USD)
💾 *Guardado en disco local/GCS*

_Iniciando Fase 2 — Minería Profunda..._"""
    return send_message(msg)

def notify_fase2_batch(departamento, pais, completados, total, aprobados, regenerados, errores, tokens, costo_usd, budget_pct):
    pct = round((completados / total) * 100)
    barra_llena = "█" * (pct // 10)
    barra_vacia = "░" * (10 - (pct // 10))
    barra = barra_llena + barra_vacia
    
    msg = f"""⛏ *FASE 2 — PROGRESO*

📍 {departamento}, {pais}
📦 *Lote completado:* {completados}/{total} módulos
📈 *Progreso:* {pct}% [{barra}]

✅ Aprobados por QA: {aprobados}
🔄 Regenerados: {regenerados}
❌ Con error: {errores}

💰 *Tokens acumulados:* {tokens:,} ({costo_usd:.3f} USD)
🔥 *Uso del budget:* {budget_pct}%"""
    return send_message(msg)

def notify_department_complete(departamento, pais, total_modulos, total_fqsas, aprobadas, pct_aprobadas, human_review, errores, horas, min, costo_usd, siguiente_dept):
    msg = f"""🏆 *DEPARTAMENTO COMPLETADO*

━━━━━━━━━━━━━━━━━━━━━━━
📍 *{departamento.upper()}, {pais.upper()}*
━━━━━━━━━━━━━━━━━━━━━━━

📊 *RESUMEN DE PRODUCCIÓN*
├ Módulos generados: {total_modulos}
├ FQSAs totales: {total_fqsas}
├ Aprobadas QA: {aprobadas} ({pct_aprobadas}%)
├ Requieren revisión humana: {human_review}
└ Errores no recuperados: {errores}

⏱ *TIEMPOS*
└ Duración total: {horas}h {min}m

💰 *COSTOS*
└ Costo estimado: {costo_usd:.3f} USD

📋 *SIGUIENTE PASO DISPONIBLE:*
{siguiente_dept}

⚠️ _Acción requerida: Responde_ *APROBAR {siguiente_dept.split(' ')[0]}* _para continuar._"""
    return send_message(msg)
