import os
import sys
import asyncio

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.abspath("."))

from backend.src.max_agent import process_message
from backend.src.agents.medical_acclimatization_agent import MedicalAcclimatizationAgent, MedicalAssessRequest
from backend.src.agents.duffle_bag_optimizer_agent import DuffleBagOptimizerAgent, DuffleOptimizeRequest, DuffleItemInput
from backend.src.agents.tailor_made_private_agent import TailorMadePrivateAgent, TailorMadeRequest
from backend.src.agents.field_sentinel_safety_agent import FieldSentinelSafetyAgent, TelemetryReport
from backend.src.agents.reputation_quality_agent import ReputationQualityAgent, TripFeedbackInput

async def main():
    print("=" * 85)
    print(" 🏔️ DEMO EN VIVO: VIAJE COMPLETO DEL CLIENTE CON LOS 5 AGENTES LIFEXTREME PERÚ")
    print(" Pasajera: Dra. Elena Vance (41 años, viene desde Miami a nivel del mar)")
    print("=" * 85)

    # -------------------------------------------------------------------------
    # PASO 1: El usuario escribe en el Chat Web de MAX preguntando por altura y glamping
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" 💬 ESCENARIO 1: EL CLIENTE CONVERSA CON MAX EN LA WEB (ORQUESTADOR MULTIAGENTE)")
    print("━" * 85)
    user_msg_1 = (
        "Hola MAX! Somos una pareja de 41 años viniendo desde Miami. Queremos hacer Salkantay o Ausangate "
        "en modalidad privada VIP con domos glamping, pero nos preocupa el mal de altura y saber cómo "
        "cuidan a los porteadores y mulas con el peso del equipaje."
    )
    print(f"👤 USUARIO (Elena): \"{user_msg_1}\"\n")
    max_reply = await process_message(user_msg_1, history=[])
    msg_text = max_reply.get("mensaje") if isinstance(max_reply, dict) else str(max_reply)
    print(f"🤖 MAX (Orquestador Lifextreme + Subagentes + Qdrant):\n{msg_text}")

    # -------------------------------------------------------------------------
    # PASO 2: Formulario / Widget Web -> Agente 1 (Asesor Médico & Aclimatación)
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" 🩺 ESCENARIO 2: PRE-VIAJE — AGENTE 1 (ASESOR MÉDICO & ACLIMATACIÓN FISIOLÓGICA)")
    print("━" * 85)
    print("📥 [Input del Usuario en Checkout Web]:")
    print("   • Ruta: Salkantay Trek & Glamping (4,630 msnm) | Edad: 41 años | Días previos en Cusco: 1 día")
    med_agent = MedicalAcclimatizationAgent()
    med_res = med_agent.assess(MedicalAssessRequest(
        client_name="Dra. Elena Vance",
        age=41,
        target_route="Salkantay Trek & Glamping",
        max_altitude_m=4630,
        days_prior_in_altitude=1,
        has_cardio_condition=False,
        lake_louise_score=1
    ))
    print(f"\n📤 [Respuesta del Agente 1 al Cliente]:")
    print(f"   • Semáforo Fisiológico: {med_res.risk_level} -> {med_res.approval_status}")
    print(f"   • Escalera de Aclimatación Prescrita:")
    for step in med_res.acclimatization_plan:
        print(f"     - {step}")
    print(f"   • Protocolo Biométrico en Campamento: {med_res.biometric_monitoring_rules[0]}")
    print(f"   • Conocimiento Qdrant Recuperado ({len(med_res.rag_citations)} nodos):")
    for c in med_res.rag_citations:
        txt = c.get("snippet", str(c)) if isinstance(c, dict) else str(c)
        print(f"     * {txt[:140]}...")

    # -------------------------------------------------------------------------
    # PASO 3: Checklist Interactivo -> Agente 2 (Duffle Bag Optimizer 7 kg & Ley 31614)
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" 🎒 ESCENARIO 3: PRE-VIAJE — AGENTE 2 (DUFFLE BAG OPTIMIZER 7 KG & LEY 31614)")
    print("━" * 85)
    print("📥 [Input del Usuario en su Checklist de Equipaje]:")
    print("   Elena selecciona: Bolsa de dormir pluma, matra autoinflable, parka pluma, pantalón Gore-Tex,")
    print("   casaca impermeable, mudas merino, sandalias de descanso y Camelbak 2L.")
    duffle_agent = DuffleBagOptimizerAgent()
    duffle_res = duffle_agent.optimize(DuffleOptimizeRequest(
        passenger_name="Dra. Elena Vance",
        route_name="Salkantay Trek & Glamping",
        items=[
            DuffleItemInput(item_id="sleeping_bag_pluma", item_name="Bolsa de Dormir Pluma -10°C", weight_grams=1450, quantity=1),
            DuffleItemInput(item_id="matra_aislante_autoinflable", item_name="Matra Therm-a-Rest", weight_grams=440, quantity=1),
            DuffleItemInput(item_id="casaca_plumas_abrigo", item_name="Parka Plumas 800FP", weight_grams=380, quantity=1),
            DuffleItemInput(item_id="pantalon_hardshell_goretex", item_name="Pantalón Gore-Tex", weight_grams=540, quantity=1),
            DuffleItemInput(item_id="casaca_impermeable_goretex", item_name="Casaca Impermeable Arc'teryx", weight_grams=485, quantity=1),
            DuffleItemInput(item_id="botella_agua_o_camelbak_2l", item_name="Camelbak 2L Agua", weight_grams=2100, quantity=1),
            DuffleItemInput(item_id="mudas_interiores_x3", item_name="Mudas Interiores Merino", weight_grams=250, quantity=2),
            DuffleItemInput(item_id="calzado_descanso_sandalias", item_name="Sandalias Descanso Campamento", weight_grams=450, quantity=1),
        ]
    ))
    print(f"\n📤 [Respuesta del Agente 2 al Cliente]:")
    print(f"   • Peso calculado en Duffle Bag (Mula/Porteador): {duffle_res.duffle_total_weight_kg} kg / {duffle_res.max_duffle_allowance_kg} kg")
    print(f"   • Margen disponible: {duffle_res.remaining_allowance_kg} kg | Cumple límite: {'SÍ ✅' if duffle_res.is_compliant else 'NO ❌'}")
    print(f"   • 📦 Empacar en Duffle Bag (Carga de Arriería): {len(duffle_res.duffle_bag_items)} ítems")
    print(f"   • 🚶 Llevar en Mochila de Día (Daypack 25L contigo): {len(duffle_res.daypack_items)} ítems")
    print(f"   • ⚖️ Alerta / Estado: {duffle_res.alerts_and_warnings[0]}")

    # -------------------------------------------------------------------------
    # PASO 4: Cotizador VIP -> Agente 3 (Private Tailor-Made Awasi/Explora)
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" 🚙 ESCENARIO 4: RESERVA VIP — AGENTE 3 (PRIVATE TAILOR-MADE 4X4 & GLAMPING)")
    print("━" * 85)
    tailor_agent = TailorMadePrivateAgent()
    tailor_res = tailor_agent.generate_quote(TailorMadeRequest(
        client_name="Dra. Elena Vance & Esposo",
        pax_count=2,
        trip_days=5,
        preferred_regions=["Cusco", "Salkantay", "Ausangate"],
        special_interests=["Fotografía de Cóndores", "Fisioterapia Andina", "Gastronomía Hiperlocal"],
        budget_tier="VIP_PREMIUM"
    ))
    print(f"📤 [Propuesta Generada por el Agente 3]:")
    print(f"   • Título: {tailor_res.itinerary_title}")
    print(f"   • Tarifa por Persona: ${tailor_res.estimated_price_per_pax_usd:,.2f} USD | Total Pareja: ${tailor_res.total_quote_usd:,.2f} USD")
    print(f"   • Bloqueo de Reserva (30%): ${tailor_res.deposit_required_30_usd:,.2f} USD")
    print(f"   • Guía Asignado: {tailor_res.private_guide_profile}")
    print(f"   • Vehículo Asignado: {tailor_res.private_vehicle_profile}")

    # -------------------------------------------------------------------------
    # PASO 5: En Ruta (4,630 msnm) -> Agente 4 (Centinela de Operaciones & Telemetría)
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" 🛰️ ESCENARIO 5: EN RUTA (ABRA SALKANTAY 4,630m) — AGENTE 4 (CENTINELA SATELITAL)")
    print("━" * 85)
    print("📥 [Telemetría Starlink Mini / Garmin inReach enviada por el Guía desde el Paso]:")
    print("   • Pasajero reporta cefalea intensa | SpO2 cae a 68% | FC: 122 bpm | Bulto de arriero: 19.4 kg")
    sentinel_agent = FieldSentinelSafetyAgent()
    sentinel_res = sentinel_agent.process_telemetry(TelemetryReport(
        expedition_id="EXP-SALK-VIP-092",
        current_location_name="Abra Salkantay (4,630m)",
        elevation_m=4630,
        passenger_spo2_percent=68,
        passenger_pulse_bpm=122,
        lake_louise_score=6,
        porter_scale_reading_kg=19.4
    ))
    print(f"\n📤 [Respuesta Automática del Agente 4 en <1 segundo]:")
    print(f"   • Estado Operativo: {sentinel_res.status}")
    print(f"   • Evacuación Activada: {sentinel_res.evacuation_protocol_active} | Alerta Clínica O2 Medical Network: {sentinel_res.hospital_dispatch_notified}")
    print(f"   • Fiscalización Pesaje Digital Ley 31614: {sentinel_res.labor_compliance_status}")
    for act in sentinel_res.immediate_actions_required:
        print(f"     ⚡ {act}")

    # -------------------------------------------------------------------------
    # PASO 6: Post-Viaje (Tren de Retorno) -> Agente 5 (Calidad & Reputación)
    # -------------------------------------------------------------------------
    print("\n" + "━" * 85)
    print(" ⭐ ESCENARIO 6: POST-VIAJE (TREN OLLANTAYTAMBO) — AGENTE 5 (CIERRE REPUTACIONAL)")
    print("━" * 85)
    rep_agent = ReputationQualityAgent()
    rep_res = rep_agent.process_feedback(TripFeedbackInput(
        passenger_name="Dra. Elena Vance",
        email="elena.vance@miamihealth.org",
        phone="+1 305 555 0199",
        nps_score=10,
        overall_rating_stars=5,
        feedback_text="¡Increíble! Las botas de compresión neumática en el campamento, el desfase horario sin gente en el Abra y ver el pesaje digital de las mulas nos encantó."
    ))
    print(f"📤 [Respuesta del Agente 5 al Cliente]:")
    print(f"   • Clasificación: {rep_res.sentiment_category} | Enlaces de Reseña Pública: {'ACTIVOS ✅' if rep_res.public_review_links_enabled else 'BLOQUEADOS'}")
    print(f"   • Mensaje Personalizado: \"{rep_res.whatsapp_message_copy}\"")
    print(f"   • Link Directo Tripadvisor: {rep_res.tripadvisor_link}")

if __name__ == "__main__":
    asyncio.run(main())
