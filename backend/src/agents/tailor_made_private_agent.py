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

class TailorMadeRequest(BaseModel):
    client_name: str
    pax_count: int = Field(2, ge=1, le=10)
    trip_days: int = Field(5, ge=2, le=14)
    preferred_regions: List[str] = ["Cusco", "Salkantay", "Valle Sagrado"]
    special_interests: List[str] = ["Alta Gastronomía Andina", "Fotografía de Paisaje", "Glamping Exclusivo"]
    lodging_preference: str = "Domos Geodésicos Suites & Lodges con Calefacción"
    budget_tier: str = "VIP_PREMIUM" # VIP_PREMIUM ($600-$1000 USD/día), ELITE_SIGNATURE ($1200+ USD/día)

class DayPlan(BaseModel):
    day: int
    title: str
    activities: str
    transport_mode: str
    lodging: str
    dining_highlight: str

class TailorMadeQuoteResponse(BaseModel):
    client_name: str
    itinerary_title: str
    days_count: int
    pax_count: int
    private_guide_profile: str
    private_vehicle_profile: str
    daily_schedule_policy: str
    itinerary_plan: List[DayPlan]
    estimated_price_per_pax_usd: float
    total_quote_usd: float
    deposit_required_30_usd: float
    rag_citations: List[dict]

class TailorMadePrivateAgent:
    """
    Agente de Personalización de Expediciones Privadas VIP Tailor-Made.
    Inspirado en los modelos de hospitalidad de Awasi y Explora.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def generate_quote(self, req: TailorMadeRequest) -> TailorMadeQuoteResponse:
        query_text = f"expedicion privada vip tailor made 1 guia privado 1 vehiculo 4x4 sin horarios fijos awasi explora {req.lodging_preference}"
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

        # Tarifas de lujo andino
        daily_rate_per_pax = 680.0 if req.pax_count >= 4 else 850.0
        total_pax_price = daily_rate_per_pax * req.trip_days
        total_trip_usd = total_pax_price * req.pax_count
        deposit_usd = round(total_trip_usd * 0.30, 2)

        # Generar itinerario dinámico sin horarios fijos
        itinerary = []
        for d in range(1, req.trip_days + 1):
            if d == 1:
                itinerary.append(DayPlan(
                    day=1,
                    title="Recepción Privada en Cusco & Aclimatación en Valle Sagrado",
                    activities="Traslado exclusivo directo a menor altitud (2,870m). Paseo suave entre andenes incas de Pisac y cata botánica.",
                    transport_mode="Camioneta 4x4 Toyota Land Cruiser Prado / HiAce VIP dedicada con chofer profesional.",
                    lodging="Eco-Lodge Boutique con tina caliente privada y chimenea.",
                    dining_highlight="Almuerzo campestre orgánico con trucha de altura y papas nativas de cultivo orgánico."
                ))
            elif d == 2:
                itinerary.append(DayPlan(
                    day=2,
                    title="Travesía Hacia el Santuario Glaciar de Soraypampa (3,900m)",
                    activities="Ascenso pausado hacia la base del Nevado Humantay. Caminata a ritmo propio sin grupos masivos.",
                    transport_mode="4x4 de apoyo permanente en puntos de enlace de trocha.",
                    lodging="Domo Geodésico Suite Privado con ventanal astronómico y calefactor.",
                    dining_highlight="Cena maridada de 4 tiempos a cargo del Chef de Expedición Lifextreme."
                ))
            elif d == 3:
                itinerary.append(DayPlan(
                    day=3,
                    title="Cruce del Paso Salkantay (4,630m) & Descenso a Selva Alta",
                    activities="Jornada reina de alta montaña con caballo de respaldo privado y oxigenoterapia preventiva.",
                    transport_mode="Guía UIAGM exclusivo a pie + caballo de auxilio en retaguardia.",
                    lodging="Sky Dome VIP frente a cascadas andinas.",
                    dining_highlight="Menú hipercalórico gourmet con estofado de cordero andino y quinua tricolor."
                ))
            elif d == 4:
                itinerary.append(DayPlan(
                    day=4,
                    title="Descenso a Cafetales Orgánicos de Lucmabamba & Hidroeléctrica",
                    activities="Trekking en ceja de selva, recolección de café de especialidad y aguas termales de Cocalmayo.",
                    transport_mode="4x4 privado para traslados logísticos y tren First Class a Aguas Calientes.",
                    lodging="Hotel de Montaña 5 estrellas en Aguas Calientes.",
                    dining_highlight="Cena de autor con productos de ceja de selva (cacao chuncho y frutas exóticas)."
                ))
            else:
                itinerary.append(DayPlan(
                    day=d,
                    title="Exploración Arqueoastronómica en Machu Picchu & Retorno VIP",
                    activities="Ingreso en primer turno matutino. Recorrido guiado de 4 horas con especialista en cosmovisión inca y tren Hiram Bingham de retorno.",
                    transport_mode="Tren de lujo de retorno a Ollantaytambo y transfer 4x4 a Cusco.",
                    lodging="Hotel Palacio Nazarenas / Monasterio en Cusco.",
                    dining_highlight="Cóctel de despedida de autor a base de destilados andinos y pisco de uvas patrimoniales."
                ))

        guide_profile = (
            "Guía Oficial de Montaña certificado UIAGM / IFMGA con especialización en historia prehispánica y "
            "certificación médica WFR (Wilderness First Responder). Asignado al 100% en exclusiva para tu grupo."
        )

        vehicle_profile = (
            "Camioneta 4x4 todo terreno de alta gama equipada con radio satelital VHF, oxigenoterapia de respaldo, "
            "conexión satelital Starlink portátil y comodidades de hidratación fría y caliente."
        )

        schedule_policy = (
            "Filosofía Cero Horarios Fijos: La hora de salida, paradas de fotografía y ritmo de caminata de cada jornada "
            "se acuerdan la víspera con tu guía durante la cena según tu estado físico y las condiciones meteorológicas."
        )

        return TailorMadeQuoteResponse(
            client_name=req.client_name,
            itinerary_title=f"Expedición Privada Tailor-Made Signature ({req.trip_days} Días / {req.pax_count} Personas)",
            days_count=req.trip_days,
            pax_count=req.pax_count,
            private_guide_profile=guide_profile,
            private_vehicle_profile=vehicle_profile,
            daily_schedule_policy=schedule_policy,
            itinerary_plan=itinerary,
            estimated_price_per_pax_usd=total_pax_price,
            total_quote_usd=total_trip_usd,
            deposit_required_30_usd=deposit_usd,
            rag_citations=citations
        )
