from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class CategoriaTuristica(str, Enum):
    aventura = "aventura"
    gastronomia = "gastronomia"
    cultural = "cultural"
    naturaleza = "naturaleza"
    legal_normativo = "legal_normativo"
    logistica = "logistica"
    desconocido = "desconocido"

class ChunkMetadata(BaseModel):
    """Metadatos del chunk. Varios se autocompletan por el script usando la ruta del archivo."""
    archivo_origen: str = Field(..., description="Nombre del archivo original")
    pais: str = Field(default="Perú", description="País deducido por defecto")
    region: str = Field(..., description="Región extraída de la carpeta padre (ej. CUSCO)")
    
    # Campos que rellenará el LLM a posteriori (Enriquecimiento)
    categoria_turistica: CategoriaTuristica = Field(
        default=CategoriaTuristica.desconocido, 
        description="Clasificación principal"
    )
    entidades_clave: List[str] = Field(
        default_factory=list,
        description="Lugares, rutas, o entidades mencionadas"
    )
    es_confiable: bool = Field(
        default=True, 
        description="Validación de calidad del texto."
    )

class ProcessedChunk(BaseModel):
    """Estructura final a vectorizar."""
    id_unico: str # Hash del chunk para evitar colisiones
    contenido_limpio: str
    metadata: ChunkMetadata
