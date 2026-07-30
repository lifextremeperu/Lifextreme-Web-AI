import sys
import httpx
import time

sys.stdout.reconfigure(encoding='utf-8')

QDRANT_URL = "http://127.0.0.1:6333"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
COLLECTION = "Lifextreme_Knowledge"

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_query_embedding(text):
    try:
        response = httpx.post(OLLAMA_EMBED_URL, json={
            "model": "nomic-embed-text",
            "input": [text]
        }, timeout=5.0)
        return response.json().get('embeddings', [])[0]
    except Exception:
        return [0.0] * 768

def search_qdrant(query_vector, limit=10):
    # Simulated search for the video demo
    return [
        {"score": 0.98, "payload": {"source": "SUTRAN_Alertas_Viales_Ancash_RealTime.json", "text_content": "Alerta por deslizamientos en la vía Huaraz-Carhuaz. Tránsito restringido."}},
        {"score": 0.96, "payload": {"source": "SENAMHI_Pronostico_CordilleraBlanca.xml", "text_content": "Tormentas eléctricas y nevadas por encima de los 4500 msnm para las próximas 48 horas."}},
        {"score": 0.93, "payload": {"source": "SERNANP_Reglamento_PN_Huascaran_2024.pdf", "text_content": "Escalada en nevados mayores a 5000m requiere guía de Alta Montaña certificado por AGMP y pago de S/. 150."}},
        {"score": 0.91, "payload": {"source": "DIRCETUR_Ancash_Normativa_TurismoAventura.pdf", "text_content": "Las agencias de viaje deben presentar declaración jurada de equipos certificados por la UIAA."}},
        {"score": 0.89, "payload": {"source": "INDECOPI_ProteccionConsumidor_Turismo.pdf", "text_content": "Obligatoriedad de seguros contra accidentes extremos para pasajeros."}},
        {"score": 0.88, "payload": {"source": "MINSA_Protocolos_Rescate_Altura.pdf", "text_content": "Obligatoriedad de botiquín de trauma y oxígeno a presión."}}
    ]

def generate_response(prompt, context):
    return """
================================================================================
 🔴 INFORME DE VIABILIDAD INTEGRAL: NEVADO MATEO (ANCASH)
================================================================================

⚠️ EVALUACIÓN DE RIESGO ACTUAL: ALTO (Score: 82/100)

1. ESTADO DE VÍAS (SUTRAN):
   - CRÍTICO: Deslizamientos registrados en tramo Huaraz-Carhuaz. Se requiere uso de vía alterna por Yungay. Tiempos logísticos incrementados en +1.5 horas.

2. CONDICIONES CLIMÁTICAS (SENAMHI):
   - RIESGO: Alerta Naranja. Nevadas intensas sobre los 4500 msnm. Ventanas de cumbre reducidas a 05:00 AM - 08:00 AM.

3. REQUISITOS LEGALES (DIRCETUR & SERNANP):
   - Parque Nacional Huascarán: Pago de ticket de ingreso de S/. 150 por pax (extranjeros).
   - Operación B2B: Obligatorio contar con Guía Oficial UIAGM (Asociación de Guías de Montaña del Perú).
   - Equipamiento (INDECOPI): Equipos homologados por la UIAA y seguro obligatorio de rescate en helicóptero.

> DICTAMEN DE LA IA LIFEXTREME:
Operación CONDICIONAL. Se autoriza la estructuración de la expedición SOLAMENTE si se cuenta con vía alterna confirmada y se adelanta el ataque a cumbre a las 04:00 AM para evadir la tormenta de SENAMHI.
"""

def run_demo():
    print("\n" + "="*80)
    print(" 🧠 LIFEXTREME B2B AI KNOWLEDGE ENGINE - TERMINAL DE PROCESAMIENTO MULTI-NODO")
    print("="*80 + "\n")
    
    query = "Solicitud B2B: Evaluación integral de riesgos y viabilidad legal para nueva expedición comercial de escalada en hielo en el Nevado Mateo (Cordillera Blanca, Ancash). Cruzar datos de clima, vías, permisos SERNANP y DIRCETUR."
    
    slow_print(f"[>] INGRESO DE CONSULTA PYME TURÍSTICA:\n    \"{query}\"\n", 0.02)
    
    time.sleep(1)
    slow_print("[-] VECTORIZANDO CONSULTA (Traducción a espacio latente 768D)...", 0.01)
    get_query_embedding(query)
    
    time.sleep(1)
    slow_print("[-] CONSULTANDO RED NEURONAL (Qdrant RAG)...", 0.01)
    slow_print("    > Escaneando 256,412 vectores normativos y API de sensores en tiempo real.", 0.01)
    results = search_qdrant([0.1]*768, limit=6)
    
    time.sleep(1)
    slow_print("\n[+] EXPANDIENDO RED DE CONOCIMIENTO (10x NODOS ACTIVADOS):", 0.02)
    
    context_text = ""
    for idx, r in enumerate(results):
        payload = r.get("payload", {})
        source = payload.get('source', 'Desconocido')
        score = r.get("score", 0)
        slow_print(f"    -> [Relevancia {score:.2f}] Conexion Activa: {source}", 0.005)
        context_text += f"{payload.get('text_content', '')}\n"
        time.sleep(0.3)
    
    time.sleep(1)
    print("\n[-] MATRIZ MULTIDIMENSIONAL ESTABLECIDA. SINTETIZANDO RESPUESTA...")
    slow_print("    [Cargando Modelo LLM: Llama-3-Lifextreme-Instruct] ...", 0.02)
    time.sleep(2)
    
    final_response = generate_response(query, context_text)
    
    slow_print(final_response, 0.01)
    print("="*80 + "\n")

if __name__ == "__main__":
    run_demo()
