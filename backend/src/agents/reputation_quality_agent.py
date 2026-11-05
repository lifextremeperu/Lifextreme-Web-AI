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

TRIPADVISOR_REVIEW_URL = "https://www.tripadvisor.com/UserReviewEdit-g294314-d_lifextreme_peru-Cusco.html"
GOOGLE_MAPS_REVIEW_URL = "https://g.page/r/lifextremeperu/review"

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

class TripFeedbackInput(BaseModel):
    passenger_name: str
    email: str
    phone: str
    tour_name: str = "Salkantay Trek 5D"
    guide_name: str = "Inti Quispe Mayhua"
    nps_score: int = Field(10, ge=1, le=10, description="Probabilidad de recomendar Lifextreme (1-10)")
    overall_rating_stars: int = Field(5, ge=1, le=5)
    food_rating: int = Field(5, ge=1, le=5)
    gear_comfort_rating: int = Field(5, ge=1, le=5)
    feedback_text: Optional[str] = "Una experiencia increíble, los domos y la comida estuvieron espectaculares."

class ReputationActionResponse(BaseModel):
    passenger_name: str
    sentiment_category: str  # PROMOTOR_EXCELENCIA, NEUTRO, DETRACTOR_INCIDENCIA
    public_review_links_enabled: bool
    whatsapp_message_copy: str
    tripadvisor_link: Optional[str] = None
    google_maps_link: Optional[str] = None
    internal_escalation_ticket: Optional[dict] = None
    rag_citations: List[dict]

class ReputationQualityAgent:
    """
    Agente de Calidad y Cierre Reputacional Post-Viaje.
    Inspirado en el embudo automatizado de reseñas de Alpaca Expeditions.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def process_feedback(self, feedback: TripFeedbackInput) -> ReputationActionResponse:
        query_text = f"embudo automatizado resenas tripadvisor post viaje tren retorno satisfaccion cliente {feedback.tour_name}"
        q_emb = get_embedding(query_text)

        citations = []
        try:
            hits = self.client.query_points(
                collection_name="lifextreme_benchmark_best_practices",
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

        # 1. Análisis de Sentimiento y Filtrado Reputacional
        if feedback.overall_rating_stars >= 4 and feedback.nps_score >= 8:
            sentiment = "PROMOTOR_EXCELENCIA"
            links_enabled = True
            
            wa_copy = (
                f"🏔️ ¡Hola {feedback.passenger_name}! Felicitaciones por conquistar el {feedback.tour_name}. "
                f"Todo el equipo de arrieros, cocineros y tu guía {feedback.guide_name} estamos profundamente agradecidos "
                f"por haber compartido esta cumbre contigo.\n\n"
                f"Tu testimonio inspira a nuevos montañistas de todo el mundo. ¿Nos regalarías 1 minuto de tu tiempo en el tren "
                f"para compartir tu experiencia en Tripadvisor o Google?\n\n"
                f"⭐ Tripadvisor: {TRIPADVISOR_REVIEW_URL}\n"
                f"⭐ Google Reviews: {GOOGLE_MAPS_REVIEW_URL}\n\n"
                f"¡Gracias por ser parte de la familia Lifextreme! 🏕️⚡"
            )
            
            return ReputationActionResponse(
                passenger_name=feedback.passenger_name,
                sentiment_category=sentiment,
                public_review_links_enabled=links_enabled,
                whatsapp_message_copy=wa_copy,
                tripadvisor_link=TRIPADVISOR_REVIEW_URL,
                google_maps_link=GOOGLE_MAPS_REVIEW_URL,
                internal_escalation_ticket=None,
                rag_citations=citations
            )
        else:
            # Flujo de contención y resolución de quejas antes de redes
            sentiment = "DETRACTOR_INCIDENCIA"
            links_enabled = False
            
            ticket = {
                "ticket_id": f"TKT-CALIDAD-{feedback.tour_name[:4].upper()}-{feedback.passenger_name.split()[0].upper()}",
                "priority": "ALTA_INMEDIATA",
                "assigned_to": "Director de Supervisión & Calidad (Cusco)",
                "passenger": feedback.passenger_name,
                "phone": feedback.phone,
                "guide": feedback.guide_name,
                "nps": feedback.nps_score,
                "stars": feedback.overall_rating_stars,
                "reported_issue": feedback.feedback_text,
                "action_required": "Interceptar con recepción presencial o llamada del Director en Ollantaytambo/Cusco."
            }

            wa_copy = (
                f"Hola {feedback.passenger_name}, en Lifextreme tu bienestar y satisfacción son nuestra prioridad número uno. "
                f"Lamentamos profundamente que algunos aspectos de tu experiencia en {feedback.tour_name} no hayan alcanzado "
                f"la excelencia que nos caracteriza.\n\n"
                f"Hemos escalado tu caso con carácter de URGENCIA directamente a nuestro Director de Calidad en Cusco, quien se "
                f"pondrá en contacto contigo de inmediato a tu arribo para resolver cualquier inconveniente y asegurar tu completa tranquilidad."
            )

            return ReputationActionResponse(
                passenger_name=feedback.passenger_name,
                sentiment_category=sentiment,
                public_review_links_enabled=links_enabled,
                whatsapp_message_copy=wa_copy,
                tripadvisor_link=None,
                google_maps_link=None,
                internal_escalation_ticket=ticket,
                rag_citations=citations
            )
