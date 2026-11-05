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

router = APIRouter()

# Instancias singleton de los agentes
medical_agent = MedicalAcclimatizationAgent()
duffle_agent = DuffleBagOptimizerAgent()
tailor_made_agent = TailorMadePrivateAgent()
sentinel_agent = FieldSentinelSafetyAgent()
reputation_agent = ReputationQualityAgent()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mesh": "Lifextreme Multiagent Operational Mesh v2.0",
        "active_agents": [
            "Agente 1: Asesor Médico & Aclimatación (Soporte Fisiológico)",
            "Agente 2: Duffle Bag Optimizer (Logística 7 kg & Ley 31614)",
            "Agente 3: Private Tailor-Made (4x4 & Guía VIP)",
            "Agente 4: Centinela de Operaciones y Seguridad en Terreno",
            "Agente 5: Calidad y Cierre Reputacional (Post-Viaje)"
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
