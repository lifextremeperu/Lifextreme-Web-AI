import time
import json
import re
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError

# ==========================================
# CONFIGURACIÓN (Open Source - Sin API Keys)
# ==========================================
# Usamos OpenStreetMap (Nominatim API)
OSM_API_URL = "https://nominatim.openstreetmap.org/search"

REGIONES = {
    "Sur": ["Cusco", "Arequipa", "Ica", "Puno", "Moquegua", "Tacna", "Ayacucho", "Apurimac", "Huancavelica"],
    "Lima y Callao": ["Lima", "Lunahuana"],
    "Centro": ["Junin", "Pasco", "Huanuco", "Ancash"],
    "Norte": ["San Martin", "Amazonas", "La Libertad", "Lambayeque", "Piura", "Cajamarca"],
    "Oriente": ["Loreto", "Ucayali", "Madre de Dios"]
}

QUERIES_BASE = [
    "parque aventura",
    "zipline",
    "tirolesa",
    "via ferrata",
    "puente tibetano"
]

# ==========================================
# MODELOS PYDANTIC (Schema Estricto)
# ==========================================
class Coordenadas(BaseModel):
    latitud: float
    longitud: float

class OpenStreetMapData(BaseModel):
    osm_id: str
    osm_type: str
    url_mapa: str
    categoria: str
    tipo: str

class Metadata(BaseModel):
    fecha_extraccion: str
    confianza_extraccion: str

class ParqueAventuraOSM(BaseModel):
    id: str
    nombre_comercial: str
    departamento: str
    direccion_completa: str
    coordenadas: Coordenadas
    osm_data: OpenStreetMapData
    infraestructura_detectada: List[str]
    metadata: Metadata

# ==========================================
# LÓGICA DEL AGENTE OPEN SOURCE
# ==========================================
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def buscar_lugares_osm(query: str) -> List[dict]:
    """Realiza una búsqueda geoespacial usando Nominatim de OpenStreetMap"""
    headers = {
        # OSM requiere un User-Agent identificable para no bloquear la petición
        "User-Agent": "Lifextreme-GeoAgent/1.0 (contacto@lifextreme.store)"
    }
    
    payload = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 10
    }
    
    try:
        response = requests.get(OSM_API_URL, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[!] Error consultando OSM API para '{query}': {e}")
        return []

def mapear_a_schema_osm(place: dict, departamento: str, term_buscado: str) -> Optional[ParqueAventuraOSM]:
    """Convierte la respuesta cruda de OSM a nuestro Schema Pydantic"""
    
    nombre = place.get("name")
    if not nombre:
        return None
        
    osm_id = str(place.get("osm_id", ""))
    
    if not osm_id:
        return None
        
    try:
        lat = float(place.get("lat", 0.0))
        lng = float(place.get("lon", 0.0))
        
        categoria = place.get("class", "")
        tipo = place.get("type", "")
        
        parque = ParqueAventuraOSM(
            id=slugify(f"{nombre}-{departamento}"),
            nombre_comercial=nombre,
            departamento=departamento,
            direccion_completa=place.get("display_name", "Ubicación remota"),
            coordenadas=Coordenadas(latitud=lat, longitud=lng),
            osm_data=OpenStreetMapData(
                osm_id=osm_id,
                osm_type=place.get("osm_type", "node"),
                url_mapa=f"https://www.openstreetmap.org/{place.get('osm_type', 'node')}/{osm_id}",
                categoria=categoria,
                tipo=tipo
            ),
            infraestructura_detectada=[term_buscado],
            metadata=Metadata(
                fecha_extraccion=datetime.now().strftime("%Y-%m-%d"),
                confianza_extraccion="ALTA"
            )
        )
        return parque
    except ValidationError as e:
        print(f"[!] Error de validación Pydantic en {nombre}: {e}")
        return None

def ejecutar_agente_osm():
    print("=========================================================")
    print("[*] INICIANDO AGENTE VALIDADOR GEOESPACIAL (OPEN SOURCE) [*]")
    print("=========================================================\n")

    parques_validados = []
    ids_procesados = set()
    
    for macro_region, departamentos in REGIONES.items():
        print(f"\n[*] Mapeando Macro-Región: {macro_region.upper()}")
        
        for depto in departamentos:
            for term in QUERIES_BASE:
                query = f"{term} {depto} peru"
                print(f"   [*] Consultando OSM: {query}")
                
                lugares = buscar_lugares_osm(query)
                
                for place in lugares:
                    p_id = str(place.get("osm_id"))
                    if p_id and p_id not in ids_procesados:
                        ids_procesados.add(p_id)
                        
                        obj_parque = mapear_a_schema_osm(place, depto, term)
                        if obj_parque:
                            parques_validados.append(obj_parque.model_dump()) # Compatible con Pydantic V2
                            print(f"       [+] Detectado: {obj_parque.nombre_comercial}")
                
                # Respetar rate-limits estrcitos de OpenStreetMap (1 req/seg)
                time.sleep(1.5)

    # Exportar a JSON estricto
    output_file = "base_datos_nacional_osm.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parques_validados, f, ensure_ascii=False, indent=2)
        
    print(f"\n[ÉXITO] Mapeo nacional finalizado. {len(parques_validados)} ubicaciones extraídas.")
    print(f"Archivo JSON generado: {output_file}")

if __name__ == "__main__":
    ejecutar_agente_osm()
