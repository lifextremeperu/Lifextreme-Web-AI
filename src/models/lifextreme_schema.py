from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Literal
from datetime import datetime

class LifextremeSchema(BaseModel):
    """
    Esquema "Verdad" de Lifextreme (DAI-v2).
    Todo dato debe pasar por aquí antes de entrar al Bus de Eventos.
    """
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source_id: str
    category: Literal["RISK", "METRIC", "LEGAL", "WEATHER", "TRANSPORT", "MARKET"]
    location: Dict[str, Any]
    payload: Dict[str, Any]
    confidence_score: float = Field(ge=0.0, le=1.0) # Score de confianza entre 0 y 1
    
    @validator('location')
    def validate_location(cls, v):
        if 'lat' not in v or 'lng' not in v:
            raise ValueError("Location debe contener 'lat' y 'lng'.")
        return v
    
    @validator('source_id')
    def validate_source(cls, v):
        valid_sources = ["PROMPERU", "AVIATION_STACK", "GDELT", "SENAMHI", "GOOGLE_TRENDS", "WIKIDATA", "BCRP", "SUTRAN", "GOOGLE_MAPS", "AMADEUS", "SERNANP", "CONSETTUR"]
        if v not in valid_sources:
            raise ValueError(f"Source ID '{v}' no autorizado.")
        return v
