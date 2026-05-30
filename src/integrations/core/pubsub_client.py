import json

class LocalPubSubMock:
    """
    Simulador de Google Cloud Pub/Sub para pruebas locales.
    Desacopla la emisión del evento del consumo.
    """
    def __init__(self):
        self.topic = "lifextreme-global-events"
        self.messages = []
        
    def publish(self, message_json: str):
        # Validar que sea JSON
        try:
            data = json.loads(message_json)
            self.messages.append(data)
            
            # Detectar si es el esquema nuevo (DAI-v2) o el viejo
            origen = data.get('source_id') or data.get('source', 'Desconocido')
            categoria = data.get('category') or f"Severidad {data.get('severity', 'N/A')}"
            
            print(f"[PUB/SUB] 📡 Evento publicado exitosamente en '{self.topic}':")
            print(f"   -> Origen: {origen} | Categoría: {categoria}")
            return True
        except Exception as e:
            print(f"[PUB/SUB] ❌ Error leyendo el mensaje JSON: {e}")
            return False

# Instancia singleton para el entorno local
pubsub = LocalPubSubMock()
