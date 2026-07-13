import sys
import httpx
import json
from qdrant_client import QdrantClient

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
COLLECTION = "Lifextreme_Knowledge"

def get_query_embedding(text):
    try:
        response = httpx.post(OLLAMA_EMBED_URL, json={
            "model": "nomic-embed-text",
            "input": [text]
        }, timeout=120.0)
        response.raise_for_status()
        return response.json().get('embeddings', [])[0]
    except Exception as e:
        print(f"[-] Error obteniendo embedding: {e}")
        return None

def search_qdrant(query_vector, limit=10):
    try:
        response = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/search", json={
            "vector": query_vector,
            "limit": limit,
            "with_payload": True
        }, timeout=30.0)
        response.raise_for_status()
        
        # En la API HTTP, devuelve una lista de diccionarios en 'result'
        results = response.json().get("result", [])
        
        # Filtrar por score
        filtered = [r for r in results if r.get("score", 0) > 0.4]
        return filtered
    except Exception as e:
        print(f"[-] Error buscando en Qdrant (HTTP): {e}")
        return []

def generate_response(prompt, context):
    try:
        full_prompt = f"""
Eres un Consultor Estratégico Senior del MINCETUR (Ministerio de Comercio Exterior y Turismo del Perú).
Usa EXCLUSIVAMENTE el siguiente contexto oficial extraído de nuestra base de datos (PERTUR, PENTUR, Normativas, etc.) para responder a la solicitud.
Si el contexto no tiene la respuesta exacta, extrapola lógicamente basándote en las políticas públicas mostradas.

CONTEXTO OFICIAL RECUPERADO:
{context}

SOLICITUD DEL MINISTRO:
{prompt}

Responde con un formato profesional, estructurando tu propuesta de proyecto con:
1. Título del Proyecto
2. Justificación (Basada en PENTUR/PERTUR)
3. Normativa Aplicable (Ej. Canotaje, Gercetur)
4. Presupuesto/Logística Estimada
"""
        response = httpx.post(OLLAMA_GENERATE_URL, json={
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": 0.3}
        }, timeout=180.0)
        return response.json().get("response", "")
    except Exception as e:
        print(f"[-] Error generando respuesta: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🏛️ SIMULADOR MINCETUR: CONSULTA ESTRATÉGICA AL RAG 🏛️")
    print("===================================================================\n")
    
    query_text = "Basado en el PENTUR 2025 y los PERTUR regionales (ej. Amazonas, Junín), diseña el perfil de un proyecto de inversión pública priorizado enfocado en el turismo de aventura (canotaje/trekking) y sostenibilidad. Debe cumplir estrictamente la regulación vigente."
    
    print(f"🗣️ PREGUNTA DEL MINISTRO:\n\"{query_text}\"\n")
    
    print("[1] Vectorizando la pregunta...")
    query_vector = get_query_embedding(query_text)
    if not query_vector: return
    
    print("[2] Buscando en los 70,606 vectores de Qdrant (PENTUR, PERTUR, Leyes)...")
    results = search_qdrant(query_vector, limit=12)
    
    if not results:
        print("[-] No se encontraron resultados relevantes.")
        return
        
    print(f"    -> Se recuperaron {len(results)} fragmentos de alta relevancia.")
    context_text = ""
    for idx, r in enumerate(results):
        payload = r.get("payload", {})
        source = payload.get('source', 'Desconocido')
        score = r.get("score", 0)
        text = payload.get('text_content', '')
        print(f"       Relevancia: {score:.2f} | Fuente: {source}")
        context_text += f"\n--- Fuente: {source} ---\n{text}\n"
        
    print("\n[3] Generando propuesta de proyecto con Llama3 (Pensando...)\n")
    final_response = generate_response(query_text, context_text)
    
    print("===================================================================")
    print(" 📋 PROPUESTA OFICIAL DEL CEREBRO LIFEXTREME")
    print("===================================================================")
    print(final_response)
    print("===================================================================")

if __name__ == "__main__":
    main()
