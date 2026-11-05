import os
import json
import urllib.request
from typing import List, Optional
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient

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

class TelemetryReport(BaseModel):
    expedition_id: str = "EXP-SALK-2026-001"
    guide_name: str = "Inti Quispe Mayhua (UIAGM)"
    current_location_name: str = "Campamento Soraypampa (3,900m)"
    elevation_m: int = 3900
    satellite_device: str = "Garmin inReach Explorer+ SOS"
    utm_coordinates: Optional[str] = "18S 729100 8521000"
    passenger_spo2_percent: int = Field(88, description="Porcentaje de saturación de oxígeno del pasajero evaluado")
    passenger_pulse_bpm: int = Field(82, description="Frecuencia cardíaca en reposo")
    lake_louise_score: int = Field(1, description="Score de síntomas MAM (0-12)")
    porter_scale_reading_kg: Optional[float] = Field(18.5, description="Pesaje registrado en balanza digital electrónica")
    weather_condition: str = "Despejado con ráfagas de viento frío (-2°C)"

class SentinelActionResponse(BaseModel):
    expedition_id: str
    status: str  # NOMINAL_SEGURO, ALERTA_PREVENTIVA, EMERGENCIA_CRITICA
    biomedical_assessment: str
    labor_compliance_status: str  # CONFORME_LEY_31614, INFRACCION_EXCESO_PESO
    immediate_actions_required: List[str]
    evacuation_protocol_active: bool
    hospital_dispatch_notified: bool
    rag_citations: List[dict]

class FieldSentinelSafetyAgent:
    """
    Agente Centinela de Operaciones y Seguridad en Terreno.
    Monitorea telemetría satelital, biometría de altitud y cumplimiento de la Ley N° 31614.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def process_telemetry(self, report: TelemetryReport) -> SentinelActionResponse:
        query_text = f"protocolo de emergencia saturacion oxigeno spo2 menor 70 evacuacion caballo ley 31614 porteador {report.current_location_name}"
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

        # 1. Fiscalización Biomédica
        status = "NOMINAL_SEGURO"
        bio_assessment = f"Saturación de oxígeno SpO2 en {report.passenger_spo2_percent}% y Pulso {report.passenger_pulse_bpm} bpm. Respuesta fisiológica estable para {report.elevation_m} msnm."
        evacuation_active = False
        hospital_notified = False
        actions = []

        if report.passenger_spo2_percent < 70 or report.lake_louise_score >= 5:
            status = "EMERGENCIA_CRITICA"
            evacuation_active = True
            hospital_notified = True
            bio_assessment = f"CRÍTICO: Hipoxia severa detectada (SpO2 {report.passenger_spo2_percent}% < 70% / Lake Louise {report.lake_louise_score}). Riesgo inminente de Edema Pulmonar (HAPE)."
            actions.append("ADMINISTRAR OXÍGENO: Abrir flujo inmediato a 3-4 L/min mediante máscara de reservorio.")
            actions.append("ACTIVAR CABALLO DE AUXILIO: Iniciar descenso de emergencia de inmediato hacia cota inferior a 3,000m (Mollepata).")
            actions.append("DESPACHO CLÍNICO O2 MEDICAL: Ambulancia de soporte avanzado movilizada al punto de encuentro vial.")
        elif report.passenger_spo2_percent < 80 or report.lake_louise_score >= 3:
            status = "ALERTA_PREVENTIVA"
            bio_assessment = f"ALERTA: SpO2 en {report.passenger_spo2_percent}% con síntomas leves a moderados de mal de montaña."
            actions.append("Monitoreo continuo cada 30 minutos y reposo térmico en domo con calefacción.")
            actions.append("Suministrar hidratación caliente con sales de rehidratación oral y dieta blanda.")
        else:
            actions.append("Parámetros fisiológicos en rango seguro. Continuar marcha planificada.")

        # 2. Fiscalización Laboral (Ley N° 31614)
        labor_status = "CONFORME_LEY_31614"
        if report.porter_scale_reading_kg and report.porter_scale_reading_kg > 20.0:
            labor_status = "INFRACCION_EXCESO_PESO"
            excess = round(report.porter_scale_reading_kg - 20.0, 2)
            actions.append(f"INFRACCIÓN LEY 31614: Balanza registró {report.porter_scale_reading_kg} kg (+{excess} kg sobre el máximo legal de 20 kg). Detener bulto y redistribuir carga con mulas adicionales antes de continuar.")

        return SentinelActionResponse(
            expedition_id=report.expedition_id,
            status=status,
            biomedical_assessment=bio_assessment,
            labor_compliance_status=labor_status,
            immediate_actions_required=actions,
            evacuation_protocol_active=evacuation_active,
            hospital_dispatch_notified=hospital_notified,
            rag_citations=citations
        )
