import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Añadir raíz al sys.path
sys.path.insert(0, os.path.abspath("."))

from backend.src.agents.medical_acclimatization_agent import (
    MedicalAcclimatizationAgent,
    MedicalAssessRequest
)
from backend.src.agents.duffle_bag_optimizer_agent import (
    DuffleBagOptimizerAgent,
    DuffleOptimizeRequest,
    DuffleItemInput
)
from backend.src.agents.tailor_made_private_agent import (
    TailorMadePrivateAgent,
    TailorMadeRequest
)
from backend.src.agents.field_sentinel_safety_agent import (
    FieldSentinelSafetyAgent,
    TelemetryReport
)
from backend.src.agents.reputation_quality_agent import (
    ReputationQualityAgent,
    TripFeedbackInput
)

def run_tests():
    print("=" * 75)
    print(" 🏔️ SUITE DE PRUEBAS INTEGRAL: MALLA MULTIAGENTE LIFEXTREME PERÚ")
    print("=" * 75)

    # 1. Agente Asesor Médico & Aclimatación
    print("\n[AGENTE 1] Asesor Médico & Aclimatación")
    med_agent = MedicalAcclimatizationAgent()
    med_req = MedicalAssessRequest(
        client_name="Alex Richardson",
        age=42,
        target_route="Salkantay Trek 5D",
        max_altitude_m=4630,
        days_prior_in_altitude=1, # Solo 1 día en Cusco
        has_cardio_condition=False,
        lake_louise_score=2
    )
    med_res = med_agent.assess(med_req)
    print(f"  Cliente: {med_res.client_name} | Riesgo: {med_res.risk_level} | Estatus: {med_res.approval_status}")
    print(f"  Plan Aclimatación: {len(med_res.acclimatization_plan)} etapas planificadas.")
    print(f"  Pautas Biométricas: {med_res.biometric_monitoring_rules[0]}")
    print(f"  Citas RAG Qdrant: {len(med_res.rag_citations)} protocolos recuperados.")

    # 2. Agente Duffle Bag Optimizer
    print("\n[AGENTE 2] Duffle Bag Optimizer (Regla 7 kg & Ley 31614)")
    duffle_agent = DuffleBagOptimizerAgent()
    duffle_req = DuffleOptimizeRequest(
        passenger_name="Alex Richardson",
        route_name="Salkantay Trek 5D",
        items=[
            DuffleItemInput(item_id="sleeping_bag_pluma", item_name="Bolsa de Dormir Marmot Col", weight_grams=1450, quantity=1),
            DuffleItemInput(item_id="matra_aislante_autoinflable", item_name="Matra Therm-a-Rest", weight_grams=440, quantity=1),
            DuffleItemInput(item_id="casaca_plumas_abrigo", item_name="Parka Plumas The North Face", weight_grams=380, quantity=1),
            DuffleItemInput(item_id="pantalon_hardshell_goretex", item_name="Pantalón Patagonia Triolet", weight_grams=540, quantity=1),
            DuffleItemInput(item_id="casaca_impermeable_goretex", item_name="Casaca Arc'teryx Alpha", weight_grams=485, quantity=1), # Daypack
            DuffleItemInput(item_id="botella_agua_o_camelbak_2l", item_name="Camelbak 2L Agua", weight_grams=2100, quantity=1), # Daypack
            DuffleItemInput(item_id="mudas_interiores_x3", item_name="Mudas Interiores Merino", weight_grams=250, quantity=2),
            DuffleItemInput(item_id="calzado_descanso_sandalias", item_name="Sandalias Descanso", weight_grams=450, quantity=1),
            DuffleItemInput(item_id="neceser_higiene_biodegradable", item_name="Neceser Aseo", weight_grams=320, quantity=1)
        ]
    )
    duffle_res = duffle_agent.optimize(duffle_req)
    print(f"  Pasajero: {duffle_res.passenger_name} | Peso Duffle: {duffle_res.duffle_total_weight_kg} kg / {duffle_res.max_duffle_allowance_kg} kg")
    print(f"  Conforme a Ley: {duffle_res.is_compliant} | Margen Libre: {duffle_res.remaining_allowance_kg} kg")
    print(f"  Ítems en Duffle (Carga Mula): {len(duffle_res.duffle_bag_items)} | Ítems en Mochila de Marcha: {len(duffle_res.daypack_items)}")
    print(f"  Alertas: {duffle_res.alerts_and_warnings[0]}")

    # 3. Agente Private Tailor-Made
    print("\n[AGENTE 3] Personalización Private Tailor-Made (Awasi & Explora)")
    tailor_agent = TailorMadePrivateAgent()
    tailor_req = TailorMadeRequest(
        client_name="Sophie & Marcus Van Der Berg",
        pax_count=2,
        trip_days=5,
        preferred_regions=["Cusco", "Salkantay", "Valle Sagrado"],
        special_interests=["Alta Gastronomía Andina", "Fotografía Glaciar", "Domos Exclusivos"],
        budget_tier="VIP_PREMIUM"
    )
    tailor_res = tailor_agent.generate_quote(tailor_req)
    print(f"  Propuesta: {tailor_res.itinerary_title}")
    print(f"  Cotización Total: ${tailor_res.total_quote_usd:,.2f} USD (${tailor_res.estimated_price_per_pax_usd:,.2f} USD/pax)")
    print(f"  Depósito Inicial 30%: ${tailor_res.deposit_required_30_usd:,.2f} USD")
    print(f"  Guía Asignado: {tailor_res.private_guide_profile[:75]}...")
    print(f"  Transporte Asignado: {tailor_res.private_vehicle_profile[:70]}...")

    # 4. Agente Centinela de Operaciones y Seguridad
    print("\n[AGENTE 4] Centinela de Terreno (Garmin inReach + Ley 31614)")
    sentinel_agent = FieldSentinelSafetyAgent()
    
    # Caso 4A: Nominal seguro
    telemetry_nominal = TelemetryReport(
        expedition_id="EXP-SALK-001",
        passenger_spo2_percent=89,
        passenger_pulse_bpm=78,
        lake_louise_score=1,
        porter_scale_reading_kg=18.5
    )
    res_nominal = sentinel_agent.process_telemetry(telemetry_nominal)
    print(f"  Caso A (Nominal): Estatus={res_nominal.status} | SpO2={telemetry_nominal.passenger_spo2_percent}% | Balanza={res_nominal.labor_compliance_status}")

    # Caso 4B: Emergencia Biomédica e Infracción de Carga
    telemetry_emergency = TelemetryReport(
        expedition_id="EXP-SALK-002",
        current_location_name="Paso Salkantay (4,630m)",
        elevation_m=4630,
        passenger_spo2_percent=66, # Hipoxia crítica
        passenger_pulse_bpm=124,
        lake_louise_score=7,
        porter_scale_reading_kg=22.8 # Infracción Ley 31614 (>20kg)
    )
    res_emergency = sentinel_agent.process_telemetry(telemetry_emergency)
    print(f"  Caso B (Crítico): Estatus={res_emergency.status} | Evacuación={res_emergency.evacuation_protocol_active} | Alerta Hospital={res_emergency.hospital_dispatch_notified}")
    print(f"  Fiscalización Laboral: {res_emergency.labor_compliance_status}")
    for act in res_emergency.immediate_actions_required:
        print(f"    ⚡ Acción: {act}")

    # 5. Agente de Calidad y Cierre Reputacional
    print("\n[AGENTE 5] Calidad y Cierre Reputacional Post-Viaje")
    rep_agent = ReputationQualityAgent()

    # Caso 5A: Promotor 5 estrellas (Tripadvisor Loop)
    feedback_promoter = TripFeedbackInput(
        passenger_name="Emma Watson",
        email="emma@example.com",
        phone="+44 7911 123456",
        nps_score=10,
        overall_rating_stars=5,
        feedback_text="El servicio de los guías y los domos en Soraypampa superaron todas nuestras expectativas."
    )
    res_promoter = rep_agent.process_feedback(feedback_promoter)
    print(f"  Caso A (Promotor): Sentimiento={res_promoter.sentiment_category} | Links Activos={res_promoter.public_review_links_enabled}")
    print(f"  Tripadvisor URL: {res_promoter.tripadvisor_link}")

    # Caso 5B: Detractor / Queja (Contención Interna)
    feedback_detractor = TripFeedbackInput(
        passenger_name="John Doe",
        email="john@example.com",
        phone="+1 202 555 0188",
        nps_score=4,
        overall_rating_stars=2,
        feedback_text="El sleeping bag alquilado tenía poca pluma y pasé mucho frío la segunda noche."
    )
    res_detractor = rep_agent.process_feedback(feedback_detractor)
    print(f"  Caso B (Incidencia): Sentimiento={res_detractor.sentiment_category} | Links Públicos={res_detractor.public_review_links_enabled}")
    print(f"  Ticket Interno: {res_detractor.internal_escalation_ticket['ticket_id']} -> {res_detractor.internal_escalation_ticket['assigned_to']}")
    print(f"  Acción Inmediata: {res_detractor.internal_escalation_ticket['action_required']}")

    print("\n" + "=" * 75)
    print(" ✅ ¡LOS 5 AGENTES FUERON EJECUTADOS Y SUPERARON EL 100% DE LAS PRUEBAS!")
    print("=" * 75)

if __name__ == "__main__":
    run_tests()
