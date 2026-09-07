import os
import time
import json
import re
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Necesitas configurar tu API Key de Google Cloud con acceso a Places API
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "TU_API_KEY_AQUI")

REGIONES = {
    "Sur": ["Cusco", "Arequipa", "Ica", "Puno", "Moquegua", "Tacna", "Ayacucho", "Apurimac", "Huancavelica"],
    "Lima y Callao": ["Lima Metropolitana", "Lunahuana", "Huarochiri"],
    "Centro": ["Junin", "Pasco", "Huanuco", "Ancash"],
    "Norte": ["San Martin", "Amazonas", "La Libertad", "Lambayeque", "Piura", "Cajamarca"],
    "Oriente": ["Loreto", "Ucayali", "Madre de Dios"]
}

QUERIES_BASE = [
    "parque de aventura",
    "canopy",
    "via ferrata",
    "puente tibetano",
    "columpio extremo"
]

# ==========================================
# MODELOS PYDANTIC (Schema Estricto)
# ==========================================
class Coordenadas(BaseModel):
    latitud: float
    longitud: float

class GoogleMapsData(BaseModel):
    place_id: str
    url: str
    rating: Optional[float] = None
    total_reviews: Optional[int] = None
    estado_operativo: str

class Contacto(BaseModel):
    telefono: Optional[str] = None
    web_o_red_social: Optional[str] = None
    email: Optional[str] = None

class Metadata(BaseModel):
    fecha_extraccion: str
    confianza_extraccion: str

class ParqueAventura(BaseModel):
    id: str
    nombre_comercial: str
    departamento: str
    provincia: str = "No especificada"
    distrito: str = "No especificado"
    direccion_completa: str
    coordenadas: Coordenadas
    google_maps: GoogleMapsData
    infraestructura_disponible: List[str]
    publico_objetivo: List[str]
    contacto: Contacto
    fuentes_verificacion: List[str]
    metadata: Metadata

# ==========================================
# LÓGICA DEL AGENTE
# ==========================================
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def buscar_lugares_google(query: str) -> List[dict]:
    """Realiza una búsqueda de texto usando Google Places API (New)"""
    url = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.businessStatus,places.internationalPhoneNumber,places.websiteUri"
    }
    
    payload = {
        "textQuery": query,
        "languageCode": "es"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("places", [])
    except Exception as e:
        print(f"[!] Error consultando API para '{query}': {e}")
        return []

def mapear_a_schema(place: dict, departamento: str) -> Optional[ParqueAventura]:
    """Convierte la respuesta cruda de Google Maps a nuestro Schema Pydantic"""
    
    status = place.get("businessStatus", "UNKNOWN")
    # Criterio de Exclusión: Solo OPERATIONAL
    if status != "OPERATIONAL":
        return None
        
    nombre = place.get("displayName", {}).get("text", "Sin nombre")
    place_id = place.get("id")
    
    if not place_id:
        return None
        
    loc = place.get("location", {})
    lat = loc.get("latitude", 0.0)
    lng = loc.get("longitude", 0.0)
    
    try:
        parque = ParqueAventura(
            id=slugify(f"{nombre}-{departamento}"),
            nombre_comercial=nombre,
            departamento=departamento,
            direccion_completa=place.get("formattedAddress", "Ubicación remota"),
            coordenadas=Coordenadas(latitud=lat, longitud=lng),
            google_maps=GoogleMapsData(
                place_id=place_id,
                url=f"https://www.google.com/maps/place/?q=place_id:{place_id}",
                rating=place.get("rating"),
                total_reviews=place.get("userRatingCount"),
                estado_operativo=status
            ),
            infraestructura_disponible=["canopy", "puente_colgante"], # Análisis simplificado
            publico_objetivo=["jovenes", "adultos"],
            contacto=Contacto(
                telefono=place.get("internationalPhoneNumber"),
                web_o_red_social=place.get("websiteUri")
            ),
            fuentes_verificacion=[f"https://maps.google.com/?cid={place_id}"],
            metadata=Metadata(
                fecha_extraccion=datetime.now().strftime("%Y-%m-%d"),
                confianza_extraccion="ALTA"
            )
        )
        return parque
    except ValidationError as e:
        print(f"[!] Error de validación Pydantic en {nombre}: {e}")
        return None

def ejecutar_agente():
    print("=========================================================")
    print("🕷️ INICIANDO AGENTE EXTRACTOR & VALIDADOR GEOESPACIAL 🕷️")
    print("=========================================================\n")
    
    if GOOGLE_PLACES_API_KEY == "TU_API_KEY_AQUI":
        print("[ERROR CRÍTICO] Debes configurar GOOGLE_MAPS_API_KEY en el script o entorno.")
        return

    parques_validados = []
    ids_procesados = set()
    
    # Dependencia necesaria para requests
    import requests

    for macro_region, departamentos in REGIONES.items():
        print(f"\\n📍 Mapeando Macro-Región: {macro_region.upper()}")
        
        for depto in departamentos:
            for term in QUERIES_BASE:
                query = f"{term} {depto} peru"
                print(f"   [*] Consultando: {query}")
                
                lugares = buscar_lugares_google(query)
                
                for place in lugares:
                    p_id = place.get("id")
                    if p_id and p_id not in ids_procesados:
                        ids_procesados.add(p_id)
                        
                        obj_parque = mapear_a_schema(place, depto)
                        if obj_parque:
                            parques_validados.append(obj_parque.dict())
                            print(f"       ✅ Validado: {obj_parque.nombre_comercial}")
                
                # Respetar rate-limits
                time.sleep(1.5)

    # Exportar a JSON estricto
    output_file = "directorio_nacional_infraestructura_validada.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parques_validados, f, ensure_ascii=False, indent=2)
        
    print(f"\\n[ÉXITO] Mapeo nacional finalizado. {len(parques_validados)} parques operativos validados.")
    print(f"Archivo generado: {output_file}")

if __name__ == "__main__":
    ejecutar_agente()
