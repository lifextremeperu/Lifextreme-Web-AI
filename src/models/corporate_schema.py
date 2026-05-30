from pydantic import BaseModel, Field
from typing import List, Optional

class StrategicInsightSchema(BaseModel):
    """
    Esquema Corporativo de Lifextreme para Inteligencia de Negocios (B2B).
    Utilizado para procesar PENTUR, estudios macro y oportunidades de inversión.
    """
    region: str = Field(description="Nombre de la región analizada (Ej: Loreto, Piura)")
    oportunidades_negocio: List[str] = Field(description="Déficit de servicios, nuevas tendencias, oportunidades para abrir operaciones o vender nuevos tours")
    riesgos_inversion: List[str] = Field(description="Brechas de infraestructura, conflictos sociales comunes, problemas logísticos")
    datos_macro_clave: List[str] = Field(description="Cifras de crecimiento, perfil del turista, estadísticas macroeconómicas")
    plan_gobierno: List[str] = Field(description="Inversión pública proyectada, proyectos del estado a futuro")
    resumen_ejecutivo: str = Field(description="Resumen táctico de alto nivel para el CEO")
