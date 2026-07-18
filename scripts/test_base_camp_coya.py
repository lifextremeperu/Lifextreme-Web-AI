import sys
import httpx
import json

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"
OLLAMA_GENERATE_URL = "http://127.0.0.1:11434/api/generate"
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

def search_qdrant(query_vector, limit=15):
    try:
        response = httpx.post(f"{QDRANT_URL}/collections/{COLLECTION}/points/search", json={
            "vector": query_vector,
            "limit": limit,
            "with_payload": True
        }, timeout=30.0)
        response.raise_for_status()
        
        results = response.json().get("result", [])
        # Filtramos por score > 0.35 para capturar reglamentos específicos de aventura
        filtered = [r for r in results if r.get("score", 0) > 0.35]
        return filtered
    except Exception as e:
        print(f"[-] Error buscando en Qdrant (HTTP): {e}")
        return []

def generate_response(prompt, context):
    try:
        full_prompt = f"""
Eres un Consultor Estratégico Senior de Turismo de Aventura y Legalidad en Perú (MINCETUR, GERCETUR).
Usa EXCLUSIVAMENTE el siguiente contexto legal y estratégico extraído de nuestra base de datos para responder.
Si el contexto no tiene la respuesta exacta, extrapola basándote en el Reglamento de Seguridad en Turismo de Aventura vigente (D.S. N° 005-2020-MINCETUR) y la normativa aplicable en Cusco (Valle Sagrado).

CONTEXTO RECUPERADO DE LA BASE DE DATOS LOCAL:
{context}

SOLICITUD DEL CLIENTE/INVERSIONISTA:
{prompt}

Responde de manera estructurada y ejecutiva, detallando paso a paso:
1. Requisitos Legales y Licencias (MINCETUR, GERCETUR Cusco, Municipalidad de Coya).
2. Requisitos Específicos por Deporte (Escalada en roca, Paddle / SUP, Mountain Bike).
3. Equipamiento de Seguridad Exigido y Certificaciones de Guías.
4. Pasos para Operar Legalmente en la Ciclovía del Maíz (permisos especiales si aplica).
"""
        response = httpx.post(OLLAMA_GENERATE_URL, json={
            "model": "phi3:latest",
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_predict": 1024}
        }, timeout=240.0)
        resp_json = response.json()
        result = resp_json.get("response", "")
        if not result:
            print(f"[-] Ollama returned empty response. Raw data: {resp_json}")
        return result
    except Exception as e:
        print(f"[-] Error generando respuesta con Ollama: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🏔️ LIFEXTREME AI: GENERADOR DE EXPEDIENTES DE INVERSIÓN 🏔️")
    print("===================================================================\n")
    
    query_text = "Quiero hacer una prueba para generar un expediente completo de un proyecto de un base camp en el valle sagrado en coya que opere 3 deportes de aventura escalada, paddle y mountain bike en la ciclovia del maiz que necesito para operar legalmente guiame paso a paso"
    
    print(f"🗣️ SOLICITUD:\n\"{query_text}\"\n")
    
    print("[1] Vectorizando la pregunta usando Ollama (nomic-embed-text)...")
    query_vector = get_query_embedding(query_text)
    if not query_vector: 
        print("[-] Falló la vectorización. Verifica que Ollama esté encendido.")
        return
    
    print("[2] Buscando en los 129,000+ vectores de Qdrant (Leyes, Reglamentos, Aventura)...")
    results = search_qdrant(query_vector, limit=5)
    
    if not results:
        print("[-] No se encontraron resultados relevantes en Qdrant.")
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
        
    print("\n[3] Generando Expediente Paso a Paso con Llama3 (Pensando... esto puede tomar un minuto)\n")
    final_response = generate_response(query_text, context_text)
    
    print("===================================================================")
    print(" 📋 EXPEDIENTE LEGAL Y OPERATIVO: BASE CAMP COYA")
    print("===================================================================")
    print(final_response)
    print("===================================================================")

    # Save to a markdown file for easy reading
    with open("expediente_coya_base_camp.md", "w", encoding="utf-8") as f:
        f.write("# Expediente Legal y Operativo: Base Camp Coya\n\n")
        f.write(final_response)
    print("\n✅ El expediente también ha sido guardado en 'expediente_coya_base_camp.md'")

if __name__ == "__main__":
    main()
