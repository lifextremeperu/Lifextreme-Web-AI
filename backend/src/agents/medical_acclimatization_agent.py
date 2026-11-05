import os
import json
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://127.0.0.1:11434/api/embeddings")
EMBEDDING_MODEL = "nomic-embed-text"

def get_embedding(text: str) -> list[float]:
    req_data = json.dumps({"model": EMBEDDING_MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res["embedding"]

class MedicalAssessRequest(BaseModel):
    client_name: str
    age: int
    target_route: str = "Salkantay Trek 5D"
    max_altitude_m: int = 4630
    days_prior_in_altitude: int = Field(1, description="Días de estancia previa en Cusco (>3,300m) o Huaraz (>3,050m)")
    has_cardio_condition: bool = False
    has_respiratory_condition: bool = False
    previous_altitude_experience: bool = True
    lake_louise_score: Optional[int] = Field(0, description="Score autoevaluado (0-12): dolor de cabeza, náuseas, fatiga, mareo")

class MedicalAssessResponse(BaseModel):
    client_name: str
    risk_level: str  # BAJO, MODERADO, ALTO, CRÍTICO
    approval_status: str  # APROBADO, REQUIERE_ACLIMATACION_PREVIA, CONTRAINDICADO_HASTA_EVALUACION
    acclimatization_plan: List[str]
    biometric_monitoring_rules: List[str]
    emergency_protocol_summary: str
    rag_citations: List[dict]

class MedicalAcclimatizationAgent:
    """
    Agente Especializado en Soporte Fisiológico y Aclimatación.
    Basado en los estándares de Inkaland Treks y Salkantay Trekking.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def assess(self, data: MedicalAssessRequest) -> MedicalAssessResponse:
        # 1. Recuperar protocolos de Qdrant
        query_text = f"protocolo de soporte fisiologico aclimatacion previa oxigenoterapia mal de montana {data.target_route}"
        q_emb = get_embedding(query_text)

        citations = []
        try:
            hits = self.client.query_points(
                collection_name="lifextreme_safety_protocols",
                query=q_emb,
                limit=2
            ).points
            for h in hits:
                citations.append({
                    "doc_id": h.payload.get("doc_id"),
                    "text": h.payload.get("text")[:180] + "...",
                    "score": round(h.score, 4)
                })
        except Exception:
            pass

        # 2. Lógica experta de evaluación de riesgo
        risk_level = "BAJO"
        approval = "APROBADO"
        acclimatization_days_needed = 2

        if data.days_prior_in_altitude < 2 and data.max_altitude_m >= 4200:
            risk_level = "ALTO"
            approval = "REQUIERE_ACLIMATACION_PREVIA"
            acclimatization_days_needed = 2
        elif data.days_prior_in_altitude == 2:
            risk_level = "MODERADO"
            approval = "APROBADO"

        if data.has_cardio_condition or data.has_respiratory_condition:
            risk_level = "CRÍTICO" if data.days_prior_in_altitude < 3 else "ALTO"
            approval = "CONTRAINDICADO_HASTA_EVALUACION"

        if data.lake_louise_score and data.lake_louise_score >= 4:
            risk_level = "CRÍTICO"
            approval = "CONTRAINDICADO_HASTA_EVALUACION"

        # 3. Plan de Aclimatación Escalonado
        plan = []
        if data.days_prior_in_altitude < 2:
            plan.append("Día -2: Arribo a Cusco (3,399m), descanso absoluto en hotel, hidratación electrolítica (3L) y dieta ligera a base de carbohidratos.")
            plan.append("Día -1: Excursión de aclimatación suave a menor altitud en el Valle Sagrado (Pisac o Ollantaytambo a 2,870m) con caminata técnica de 3 horas.")
            plan.append("Día 0: Briefing presencial obligatorio en Cusco a las 18:00 hrs y control de saturación de oxígeno.")
        else:
            plan.append("Aclimatación satisfactoria previa de 48h cumplida en Cusco. Hidratación constante de 2.5L diarios durante la marcha.")

        monitoring = [
            "Medición biométrica obligatoria 2 veces al día (07:00 AM y 19:00 PM): Pulsioximetría (SpO2) y Tensiometría.",
            "Umbral de seguridad: Si SpO2 < 70% o Lake Louise Score > 4, administración inmediata de oxígeno medicinal a 3 L/min.",
            "Disponibilidad garantizada de caballo de auxilio en el grupo para descenso preventivo inmediato."
        ]

        emergency = (
            "En caso de sospecha de Edema Pulmonar (HAPE) o Cerebral (HACE), el guía certificado WFR/UIAGM activará "
            "el protocolo de descenso inmediato perdiendo mínimo 500m de desnivel, notificará vía satelital Garmin inReach SOS "
            "y coordinará la ambulancia de enlace con O2 Medical Network en Cusco."
        )

        return MedicalAssessResponse(
            client_name=data.client_name,
            risk_level=risk_level,
            approval_status=approval,
            acclimatization_plan=plan,
            biometric_monitoring_rules=monitoring,
            emergency_protocol_summary=emergency,
            rag_citations=citations
        )
