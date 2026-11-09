from fastapi import APIRouter, HTTPException
from .medical_acclimatization_agent import (
    MedicalAcclimatizationAgent,
    MedicalAssessRequest,
    MedicalAssessResponse
)
from .duffle_bag_optimizer_agent import (
    DuffleBagOptimizerAgent,
    DuffleOptimizeRequest,
    DuffleOptimizeResponse
)
from .tailor_made_private_agent import (
    TailorMadePrivateAgent,
    TailorMadeRequest,
    TailorMadeQuoteResponse
)
from .field_sentinel_safety_agent import (
    FieldSentinelSafetyAgent,
    TelemetryReport,
    SentinelActionResponse
)
from .reputation_quality_agent import (
    ReputationQualityAgent,
    TripFeedbackInput,
    ReputationActionResponse
)
from .booking_registry import BookingRegistry, BookingRecord
from .governance_expediente_agent import (
    GovernanceExpedienteAgent,
    ExpedienteRequest,
    ExpedienteResponse
)

router = APIRouter()

# Instancias singleton de los agentes y registro central de reservas
medical_agent = MedicalAcclimatizationAgent()
duffle_agent = DuffleBagOptimizerAgent()
tailor_made_agent = TailorMadePrivateAgent()
sentinel_agent = FieldSentinelSafetyAgent()
reputation_agent = ReputationQualityAgent()
booking_registry = BookingRegistry()
governance_agent = GovernanceExpedienteAgent()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mesh": "Lifextreme Multiagent Operational Mesh v2.1 + Governance DIR-AG-QDRANT-2026-001",
        "active_agents": [
            "Agente 1: Asesor Médico & Aclimatación (Soporte Fisiológico)",
            "Agente 2: Duffle Bag Optimizer (Logística 7 kg & Ley 31614)",
            "Agente 3: Private Tailor-Made (4x4 & Guía VIP)",
            "Agente 4: Centinela de Operaciones y Seguridad en Terreno",
            "Agente 5: Calidad y Cierre Reputacional (Post-Viaje)",
            "Agente 6 (DIR-AG-QDRANT-2026-001): Gobernanza IA & Expediente Técnico Educativo/Institucional"
        ]
    }

@router.post("/medical/assess", response_model=MedicalAssessResponse)
async def assess_medical_acclimatization(req: MedicalAssessRequest):
    try:
        return medical_agent.assess(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en evaluación médica: {str(e)}")

@router.post("/logistics/duffle-check", response_model=DuffleOptimizeResponse)
async def check_duffle_bag(req: DuffleOptimizeRequest):
    try:
        return duffle_agent.optimize(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en optimización de duffle bag: {str(e)}")

@router.post("/tailor-made/quote", response_model=TailorMadeQuoteResponse)
async def quote_private_tailor_made(req: TailorMadeRequest):
    try:
        return tailor_made_agent.generate_quote(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en cotización tailor-made: {str(e)}")

@router.post("/sentinel/telemetry-alert", response_model=SentinelActionResponse)
async def process_field_telemetry(req: TelemetryReport):
    try:
        return sentinel_agent.process_telemetry(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en centinela de operaciones: {str(e)}")

@router.post("/reputation/feedback", response_model=ReputationActionResponse)
async def process_trip_reputation(req: TripFeedbackInput):
    try:
        return reputation_agent.process_feedback(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en cierre reputacional: {str(e)}")


@router.post("/bookings/register")
async def register_confirmed_booking(req: BookingRecord):
    try:
        return booking_registry.register_booking(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando reserva: {str(e)}")


@router.get("/bookings/{booking_code}")
async def verify_booking_status(booking_code: str):
    rec = booking_registry.find_booking(booking_code=booking_code)
    if not rec:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return rec


@router.post("/governance/expediente", response_model=ExpedienteResponse)
async def generate_governance_expediente(req: ExpedienteRequest):
    try:
        return await governance_agent.generate_expediente_package(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en pipeline de Gobernanza IA: {str(e)}")


