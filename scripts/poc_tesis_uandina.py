import httpx
import json

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_EMBEDDINGS = "nomic-embed-text"
MODEL_GEN = "llama3:8b" # O el modelo que el usuario tenga descargado, fallback a lo que devuelva Ollama.

# Tema impactante para la UAC
TESIS_TOPIC = "El impacto de la capacidad de carga estricta en el Santuario de Machupicchu frente a las expectativas de crecimiento económico y la demanda turística internacional al 2026."

print("INICIANDO EL ASISTENTE UNIVERSITARIO (U. ANDINA DEL CUSCO)")
print(f"Tema de Tesis: {TESIS_TOPIC}")

def get_embedding(text):
    print("-> Convirtiendo el tema de tesis a vectores matemáticos...")
    try:
        response = httpx.post(f"{OLLAMA_URL}/api/embeddings", json={
            "model": MODEL_EMBEDDINGS,
            "prompt": text
        }, timeout=30.0)
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error obteniendo embedding: {e}")
        return None

def search_qdrant(vector, limit=8):
    print("-> Consultando el 'Cerebro' de Lifextreme (Qdrant) buscando leyes y contexto...")
    try:
        response = httpx.post(f"{QDRANT_URL}/collections/Lifextreme_Knowledge/points/search", json={
            "vector": vector,
            "limit": limit,
            "with_payload": True
        })
        return response.json()["result"]
    except Exception as e:
        print(f"Error en Qdrant: {e}")
        return []

def generate_thesis(context, topic):
    print("-> Redactando la Hipótesis y Planteamiento de la Tesis con IA...\n")
    prompt = f"""
    Eres un asesor de tesis experto de la Universidad Andina del Cusco (UAC) en la escuela de Turismo.
    
    TEMA DE TESIS: {topic}
    
    Basándote ÚNICAMENTE en la siguiente base de conocimiento oficial (Leyes, planes operativos, aforos):
    {context}
    
    Por favor, redacta un 'Esqueleto de Tesis' con la siguiente estructura (Se muy profesional y académico):
    1. Planteamiento del Problema (Describir la tensión entre el turismo masivo y las leyes).
    2. Justificación Legal (Cita explícitamente alguna norma o plan del contexto provisto, si lo hay).
    3. Hipótesis Principal.
    """
    
    try:
        response = httpx.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL_GEN,
            "prompt": prompt,
            "stream": False
        }, timeout=120.0)
        
        # Intentar obtener respuesta de llama3
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Error: " + response.text
    except Exception as e:
        return f"Error en generación: {e}"

def main():
    vector = get_embedding(TESIS_TOPIC)
    if not vector:
        print("Fallo el embedding.")
        return
        
    results = search_qdrant(vector)
    
    if not results:
        print("No se encontraron resultados en Qdrant.")
        return
        
    context = ""
    for idx, r in enumerate(results):
        payload = r.get("payload", {})
        texto = payload.get("text_content", "") or payload.get("text", "")
        context += f"\n[Documento {idx+1}]: {texto}\n"
    
    thesis_output = generate_thesis(context, TESIS_TOPIC)
    
    print("\n" + "="*60)
    print("RESULTADO FINAL: ESQUELETO DE TESIS GENERADO POR LA IA")
    print("="*60)
    print(thesis_output)
    print("="*60)
    
if __name__ == "__main__":
    main()
