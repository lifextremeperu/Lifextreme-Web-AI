import os
import json
import urllib.request
from typing import List, Dict, Optional
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

# Catálogo estándar de pesos referenciales en gramos
GEAR_WEIGHT_CATALOG = {
    "sleeping_bag_pluma": 1450,
    "matra_aislante_autoinflable": 440,
    "casaca_plumas_abrigo": 380,
    "pantalon_hardshell_goretex": 540,
    "casaca_impermeable_goretex": 485,
    "primera_capa_termica_superior": 200,
    "primera_capa_termica_inferior": 180,
    "mudas_interiores_x3": 250,
    "medias_merino_trekking_x3": 180,
    "calzado_descanso_sandalias": 450,
    "toalla_microfibra_secado_rapido": 120,
    "neceser_higiene_biodegradable": 320,
    "linterna_frontal_y_baterias": 95,
    "guantes_termicos_y_gorro_lana": 150,
    "powerbank_20000mah": 380,
    "botella_agua_o_camelbak_2l": 2100,
    "bloqueador_y_lentes_uv": 150,
    "botiquin_primeros_auxilios_personal": 280
}

DAYPACK_EXCLUSIVE_ITEMS = [
    "casaca_impermeable_goretex",
    "botella_agua_o_camelbak_2l",
    "bloqueador_y_lentes_uv",
    "botiquin_primeros_auxilios_personal",
    "linterna_frontal_y_baterias"
]

PROHIBITED_DUFFLE_ITEMS = ["garrafas_gas_camping", "drones_no_registrados", "bebidas_alcoholicas_vidrio"]

class DuffleItemInput(BaseModel):
    item_id: str
    item_name: str
    weight_grams: Optional[int] = None
    quantity: int = 1

class DuffleOptimizeRequest(BaseModel):
    passenger_name: str
    route_name: str = "Salkantay Trek 5D"
    items: List[DuffleItemInput]

class DuffleOptimizeResponse(BaseModel):
    passenger_name: str
    duffle_total_weight_kg: float
    max_duffle_allowance_kg: float = 7.0
    is_compliant: bool
    remaining_allowance_kg: float
    duffle_bag_items: List[Dict]
    daypack_items: List[Dict]
    alerts_and_warnings: List[str]
    porter_law_compliance_note: str
    rag_citations: List[dict]

class DuffleBagOptimizerAgent:
    """
    Agente de Logística de Marcha y Optimización de Duffle Bag (Regla de 7 kg).
    Basado en los estándares de Salkantay Trekking y la Ley del Porteador N° 31614.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    def optimize(self, req: DuffleOptimizeRequest) -> DuffleOptimizeResponse:
        # 1. Recuperar directivas de Qdrant
        query_text = f"regla de 7 kg duffle bag equipaje pasajero arrieros porteadores ley 31614 {req.route_name}"
        q_emb = get_embedding(query_text)

        citations = []
        try:
            hits = self.client.query_points(
                collection_name="lifextreme_porter_welfare_peru",
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

        duffle_items = []
        daypack_items = []
        duffle_weight_g = 0
        alerts = []

        for it in req.items:
            unit_weight = it.weight_grams or GEAR_WEIGHT_CATALOG.get(it.item_id, 300)
            total_item_weight = unit_weight * it.quantity

            if it.item_id in PROHIBITED_DUFFLE_ITEMS:
                alerts.append(f"ALERTA PROHIBICIÓN: '{it.item_name}' no está permitido en el bolso de carga por normativa SERNANP.")
                continue

            if it.item_id in DAYPACK_EXCLUSIVE_ITEMS:
                daypack_items.append({
                    "item_name": it.item_name,
                    "quantity": it.quantity,
                    "weight_g": total_item_weight,
                    "location": "Mochila de Marcha Personal (20-30 L)"
                })
            else:
                duffle_items.append({
                    "item_name": it.item_name,
                    "quantity": it.quantity,
                    "weight_g": total_item_weight,
                    "location": "Bolso Duffle de Arriería (Sellado)"
                })
                duffle_weight_g += total_item_weight

        duffle_kg = round(duffle_weight_g / 1000.0, 2)
        is_compliant = duffle_kg <= 7.0
        remaining_kg = round(max(0.0, 7.0 - duffle_kg), 2)

        if not is_compliant:
            excess = round(duffle_kg - 7.0, 2)
            alerts.append(f"EXCESO DE PESO: Tu duffle bag pesa {duffle_kg} kg (+{excess} kg sobre el límite legal). Debes retirar prendas no esenciales o transferirlas a la custodia gratuita de Lifextreme en Cusco.")
        else:
            alerts.append(f"PESO ÓPTIMO: Tienes {remaining_kg} kg libres para prendas adicionales o recuerdos.")

        porter_note = (
            "El pesaje oficial del Duffle Bag se realiza con balanza digital electrónica durante el briefing "
            "presencial en Cusco la víspera de la partida. Por estricto cumplimiento de la Ley del Porteador N° 31614, "
            "ningún arriero o porteador cargará bultos que superen los 20 kg consolidados en balanza."
        )

        return DuffleOptimizeResponse(
            passenger_name=req.passenger_name,
            duffle_total_weight_kg=duffle_kg,
            max_duffle_allowance_kg=7.0,
            is_compliant=is_compliant,
            remaining_allowance_kg=remaining_kg,
            duffle_bag_items=duffle_items,
            daypack_items=daypack_items,
            alerts_and_warnings=alerts,
            porter_law_compliance_note=porter_note,
            rag_citations=citations
        )
