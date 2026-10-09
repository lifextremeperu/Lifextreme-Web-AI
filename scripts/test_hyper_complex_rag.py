import sys
import time
import requests
import json
import numpy as np

def print_step(title, status="[OK]"):
    print(f"\n>> {title.upper().ljust(60, '.')} {status}")
    time.sleep(1.5)

def get_local_embedding(text):
    url = "http://localhost:11434/api/embed"
    response = requests.post(url, json={"model": "nomic-embed-text", "input": text})
    return response.json().get("embeddings", [])[0]

def chat_with_phi3(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "phi3:latest",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 1024, "top_k": 50, "top_p": 0.9}
    }
    response = requests.post(url, json=payload)
    return response.json().get("message", {}).get("content", "")

def run_simulation():
    sys.stdout.reconfigure(encoding='utf-8')
    print("="*80)
    print(" 🚀 INICIANDO EJECUCIÓN: RAG MULTI-AGENTE (MODO HIPER-TÉCNICO)")
    print(" MOTOR DE BASE DE DATOS: Qdrant Vector Engine (Simulated)")
    print(" LLM ACTIVO: Ollama (phi3:latest)")
    print(" EMBEDDER: nomic-embed-text (Vector: 768 dimensiones)")
    print("="*80)
    
    query = "Hola, viajo manana a Huaraz (Ancash) con mis padres de 65 anos. Queremos hacer trekking, pero he leido que hay huelgas y clima inestable. Si esta bloqueado o llueve, que plan B de aventura suave me recomiendas?"
    print(f"\n[QUERY ENTRADA (RAW)]: {query}")

    # Paso 1: Vectorización
    print_step("Iniciando Tokenización y Vectorización (nomic-embed-text)")
    try:
        vector = get_local_embedding(query)
        print(f"   [!] Query codificado exitosamente.")
        print(f"   [!] Dimensiones generadas: {len(vector)}")
        print(f"   [!] Extracto del Tensor: {str(vector[:5])[:-1]} ... ]")
    except Exception as e:
        print(f"Error con Ollama: {e}. Asegurate de que Ollama esta corriendo.")
        return

    # Paso 2: Búsqueda Semántica en Qdrant (MOCK con Nodos reales)
    print_step("Calculando Similitud de Coseno en Qdrant (Coleccion: Lifextreme_Knowledge)")
    time.sleep(2)
    
    mock_qdrant_hits = [
        {
            "score": 0.9432,
            "node": "MOD_SUTRAN > DEP_Ancash",
            "data": "ALERTA SUTRAN (Hoy): Bloqueos intermitentes en la via Pativilca-Huaraz debido a manifestaciones gremiales. Transito restringido a un carril."
        },
        {
            "score": 0.9105,
            "node": "MOD_SENAMHI > DEP_Ancash",
            "data": "REPORTE SENAMHI: Alerta Naranja en el Callejon de Huaylas. Lluvias fuertes y nevadas sobre los 4000 msnm (incluye Parque Nacional Huascaran / Laguna 69). Riesgo de hipotermia."
        },
        {
            "score": 0.8871,
            "node": "MOD_FQSAS > SALES DNA",
            "data": "PROTOCOLO DE VENTAS B2C (Perfil: Adulto Mayor / +60 anos): NUNCA recomendar Laguna 69 en clima inestable. Altitud (4600m) y lluvia son criticos. PLAN B ALTERNATIVO EN HUARAZ: Tours culturales e historicos de baja exigencia fisica como Monumento Arqueologico Chavin de Huantar (3100m) o Laguna de Llanganuco (Tour en bus)."
        }
    ]
    
    print("\n   [RESULTADOS DE BÚSQUEDA VECTORIAL (TOP-K=3)]:")
    context_str = ""
    for idx, hit in enumerate(mock_qdrant_hits, 1):
        print(f"   ► Nodo {idx}: [{hit['node']}] | Score: {hit['score']}")
        print(f"       Info: {hit['data']}")
        context_str += f"- [{hit['node']}]: {hit['data']}\n"
        time.sleep(0.5)
        
    # Paso 3: Reranking y Generación de Respuesta
    print_step("Ensamblando Prompt de Inyeccion de Contexto (RAG)")
    prompt_maestro = f"""
    Eres el 'Cerebro Central' de operaciones turisticas de Lifextreme.
    Un cliente ha consultado lo siguiente: '{query}'
    
    Usa EXCLUSIVAMENTE los siguientes vectores recuperados de la base de datos para responder. 
    Aplica psicologia de ventas (SALES DNA) para darle tranquilidad y asegurar la venta del Plan B:
    
    {context_str}
    
    Instrucciones: 
    1. Dirigete al cliente de forma empatica.
    2. Informale de los riesgos (SUTRAN/SENAMHI) justificando por que Laguna 69 no es opcion para sus padres.
    3. Ofrécele el Plan B (Chavin de Huantar / Llanganuco en bus).
    4. Manten la respuesta breve y resolutiva.
    """
    
    print_step("Ejecutando Inferencia Generativa (Phi-3 LLM)")
    inicio = time.time()
    respuesta = chat_with_phi3(prompt_maestro)
    fin = time.time()
    
    print(f"   [!] Inferencia completada en {round(fin - inicio, 2)} segundos.")
    print("="*80)
    print("\n[🧠 RESPUESTA GENERADA POR EL CEREBRO LIFEXTREME]:\n")
    print(respuesta)
    print("\n" + "="*80)

if __name__ == "__main__":
    run_simulation()
