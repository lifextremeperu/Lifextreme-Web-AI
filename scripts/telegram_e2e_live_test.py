import os
import sys
import json
import time
import asyncio
import urllib.request
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath("."))
load_dotenv(override=True)

from backend.src.max_agent import process_message
from backend.src.agents.booking_registry import BookingRegistry, BookingRecord
from backend.src.agents.medical_acclimatization_agent import MedicalAcclimatizationAgent, MedicalAssessRequest
from backend.src.agents.duffle_bag_optimizer_agent import DuffleBagOptimizerAgent, DuffleOptimizeRequest, DuffleItemInput
from backend.src.agents.tailor_made_private_agent import TailorMadePrivateAgent, TailorMadeRequest
from backend.src.agents.field_sentinel_safety_agent import FieldSentinelSafetyAgent, TelemetryReport
from backend.src.agents.reputation_quality_agent import ReputationQualityAgent, TripFeedbackInput

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "2094843795").strip()
USER_PHONE = "+51958050928"
BOOKING_CODE = "LX-958050"


def tg_request(method: str, payload: dict = None) -> dict:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_tg(text: str):
    try:
        return tg_request("sendMessage", {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })
    except Exception:
        # Fallback sin Markdown si algún carácter especial falla
        return tg_request("sendMessage", {
            "chat_id": CHAT_ID,
            "text": text.replace("*", "").replace("_", ""),
            "disable_web_page_preview": True
        })


async def run_e2e_and_listen():
    me = tg_request("getMe")
    bot_username = me.get("result", {}).get("username", "LifextremeBot")
    print(f"✅ Conectado al Bot de Telegram: @{bot_username} | Chat ID: {CHAT_ID} | Teléfono: {USER_PHONE}")

    # 1. Registrar la Reserva Oficial vinculada a +51958050928 en el BookingRegistry
    registry = BookingRegistry()
    booking = registry.register_booking(BookingRecord(
        booking_code=BOOKING_CODE,
        passenger_name="Socio Elite Lifextreme",
        email="contacto@lifextreme.store",
        phone=USER_PHONE,
        tour_name="Salkantay Trek & Domos Glamping VIP 5D",
        tour_date="2026-11-15",
        pax_count=2,
        total_amount_pen=3700.0,
        paid_amount_pen=1110.0,
        payment_plan="split_30_30_40",
        lifecycle_stage="RESERVA_CONFIRMADA_PRE_VIAJE"
    ))
    print(f"✅ Reserva registrada en base de datos: {booking['booking_code']} para {USER_PHONE}")

    # -------------------------------------------------------------------------
    # ENVÍO EN VIVO AL TELEGRAM DEL USUARIO: FLUJO COMPLETO DE LAS 5 ETAPAS
    # -------------------------------------------------------------------------

    # ETAPA 1: Confirmación de Reserva y Reconocimiento de Identidad (+51958050928)
    msg_1 = (
        f"🏔️ *LIFEXTREME OUTDOOR EXPERIENCE — PRUEBA E2E EN VIVO*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 *ETAPA 1: RESERVA CONFIRMADA EN SISTEMA*\n"
        f"• *Código de Reserva:* `{BOOKING_CODE}`\n"
        f"• *Celular Vinculado:* `{USER_PHONE}`\n"
        f"• *Expedición:* Salkantay Trek & Domos Glamping VIP 5D\n"
        f"• *Abono 30% Validado:* S/ 1,110.00 (Saldo 70%: S/ 2,590.00)\n\n"
        f"🤖 _A partir de este instante, MAX detecta tu número {USER_PHONE} como PASAJERO CONFIRMADO, apaga el modo ventas y activa tus 5 Agentes Operativos._"
    )
    send_tg(msg_1)
    print("📤 [Telegram] Etapa 1 enviada.")

    # ETAPA 2: Agente 1 — Asesor Médico & Aclimatación
    med_agent = MedicalAcclimatizationAgent()
    med_res = med_agent.assess(MedicalAssessRequest(
        client_name="Socio Lifextreme (+51958050928)",
        age=35,
        target_route="Salkantay Trek & Glamping 5D",
        max_altitude_m=4630,
        days_prior_in_altitude=1,
        has_cardio_condition=False,
        lake_louise_score=1
    ))
    plan_lines = "\n".join([f"  ▫️ {step}" for step in med_res.acclimatization_plan])
    msg_2 = (
        f"🩺 *ETAPA 2 (PRE-VIAJE): AGENTE 1 — ASESOR MÉDICO & ACLIMATACIÓN*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *Semáforo Fisiológico:* `{med_res.risk_level}` ({med_res.approval_status})\n"
        f"• *Escalera de Aclimatación Obligatoria:*\n{plan_lines}\n\n"
        f"• *Innovación Lifextreme en Campamento:*\n"
        f"  ▫️ {med_res.biometric_monitoring_rules[0]}\n"
        f"  ▫️ Fisioterapia post-marcha con botas de compresión neumática solar y pediluvios botánicos andinos (romero, llantén y molle)."
    )
    send_tg(msg_2)
    print("📤 [Telegram] Etapa 2 (Agente Médico) enviada.")

    # ETAPA 3: Agente 2 — Duffle Bag Optimizer 7 kg & Ley 31614
    duffle_agent = DuffleBagOptimizerAgent()
    duffle_res = duffle_agent.optimize(DuffleOptimizeRequest(
        passenger_name="Socio Lifextreme (+51958050928)",
        route_name="Salkantay Trek & Glamping 5D",
        items=[
            DuffleItemInput(item_id="sleeping_bag_pluma", item_name="Bolsa de Dormir Pluma -10°C", weight_grams=1450, quantity=1),
            DuffleItemInput(item_id="matra_aislante_autoinflable", item_name="Matra Therm-a-Rest", weight_grams=440, quantity=1),
            DuffleItemInput(item_id="casaca_plumas_abrigo", item_name="Parka Plumas 800FP", weight_grams=380, quantity=1),
            DuffleItemInput(item_id="pantalon_hardshell_goretex", item_name="Pantalón Gore-Tex", weight_grams=540, quantity=1),
            DuffleItemInput(item_id="casaca_impermeable_goretex", item_name="Casaca Hardshell Arc'teryx", weight_grams=485, quantity=1),
            DuffleItemInput(item_id="botella_agua_o_camelbak_2l", item_name="Hidratación Camelbak 2L", weight_grams=2100, quantity=1),
            DuffleItemInput(item_id="mudas_interiores_x3", item_name="Mudas Merino Térmicas", weight_grams=250, quantity=2),
        ]
    ))
    msg_3 = (
        f"🎒 *ETAPA 3 (48H ANTES): AGENTE 2 — DUFFLE BAG OPTIMIZER (7 KG)*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *Peso en Duffle Bag (Mula/Arriero):* `{duffle_res.duffle_total_weight_kg} kg / {duffle_res.max_duffle_allowance_kg} kg` ✅\n"
        f"• *Margen Libre:* `{duffle_res.remaining_allowance_kg} kg`\n"
        f"• *Separación Inteligente:*\n"
        f"  📦 *Va en el Duffle Bag ({len(duffle_res.duffle_bag_items)} ítems):* Bolsa de dormir, matra, parka pluma, pantalón y mudas merino.\n"
        f"  🚶 *Va en tu Mochila de Día ({len(duffle_res.daypack_items)} ítems):* Casaca impermeable y Camelbak 2L.\n"
        f"• *Trazabilidad Ética Ley N° 31614:* Pesaje digital visible ante ti al salir del campamento y Pasaporte Ético Animal."
    )
    send_tg(msg_3)
    print("📤 [Telegram] Etapa 3 (Agente Duffle Bag) enviada.")

    # ETAPA 4: Agente 4 — Centinela de Terreno (Telemetría Satelital en Ruta)
    sentinel_agent = FieldSentinelSafetyAgent()
    sentinel_res = sentinel_agent.process_telemetry(TelemetryReport(
        expedition_id=BOOKING_CODE,
        current_location_name="Abra Salkantay (4,630 msnm)",
        elevation_m=4630,
        passenger_spo2_percent=88,
        passenger_pulse_bpm=82,
        lake_louise_score=1,
        porter_scale_reading_kg=18.6
    ))
    msg_4 = (
        f"🛰️ *ETAPA 4 (EN RUTA 4,630m): AGENTE 4 — CENTINELA SATELITAL (STARLINK / INREACH)*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *Ubicación:* Abra Salkantay (4,630 msnm — Desfase Horario Offset Trekking sin multitudes)\n"
        f"• *Estatus Biométrico:* `{sentinel_res.status}` (SpO2: 88% | Pulso: 82 bpm)\n"
        f"• *Auditoría Balanza Digital Porteadores:* `{sentinel_res.labor_compliance_status}` (18.6 kg <= 20 kg máx. Ley 31614)\n"
        f"• *Red de Respaldo Activa:* Corredor clínico O2 Medical Network + Caballos de rescate ensillados."
    )
    send_tg(msg_4)
    print("📤 [Telegram] Etapa 4 (Agente Centinela) enviada.")

    # ETAPA 5: Agente 5 — Calidad y Cierre Reputacional Post-Viaje
    rep_agent = ReputationQualityAgent()
    rep_res = rep_agent.process_feedback(TripFeedbackInput(
        passenger_name="Socio Lifextreme",
        email="contacto@lifextreme.store",
        phone=USER_PHONE,
        nps_score=10,
        overall_rating_stars=5,
        feedback_text="Excelente el sistema de domos, el pesaje ético y la fisioterapia en campamento."
    ))
    msg_5 = (
        f"⭐ *ETAPA 5 (TREN DE RETORNO): AGENTE 5 — CIERRE REPUTACIONAL*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *Clasificación:* `{rep_res.sentiment_category}`\n"
        f"• *Mensaje Automático Post-Viaje:*\n"
        f"{rep_res.whatsapp_message_copy}\n\n"
        f"💬 *¡AHORA ESCRÍBEME POR AQUÍ EN TELEGRAM!* 👇\n"
        f"Estoy escuchando en vivo con tu reserva `{BOOKING_CODE}` y tu número `{USER_PHONE}`. "
        f"Pregúntame cualquier cosa (ej: _\"¿Qué llevo en mi mochila?\"_, _\"Me duele la cabeza en altura\"_ o _\"Quiero cotizar un 4x4 privado\"_) y te responderé al instante."
    )
    send_tg(msg_5)
    print("📤 [Telegram] Etapa 5 (Agente Calidad + Invitación Interactiva) enviada.")


if __name__ == "__main__":
    asyncio.run(run_e2e_and_listen())
