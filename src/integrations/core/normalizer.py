import json
from datetime import datetime

class DataNormalizer:
    """
    Obliga a todas las APIs a devolver un formato JSON estandarizado
    antes de inyectarlo en el Bus de Eventos.
    """
    
    VALID_SOURCES = ["AVIATION_STACK", "GDELT", "SENAMHI", "USGS", "GOOGLE_TRENDS"]
    
    @staticmethod
    def normalize(source: str, severity: int, location: dict, payload: str) -> str:
        if source not in DataNormalizer.VALID_SOURCES:
            raise ValueError(f"Source '{source}' no es válido.")
            
        if not (1 <= severity <= 5):
            raise ValueError("La severidad debe estar entre 1 (Bajo) y 5 (Crítico).")
            
        if not isinstance(location, dict) or "lat" not in location or "lng" not in location:
            raise ValueError("Location debe ser un diccionario con 'lat' y 'lng'.")
            
        normalized_data = {
            "source": source,
            "severity": severity,
            "location": location,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Garantiza que el output sea matemáticamente un JSON válido
        return json.dumps(normalized_data, ensure_ascii=False)
