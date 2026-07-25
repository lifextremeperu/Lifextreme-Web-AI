import os
import sys
import json
import requests
from qdrant_client import QdrantClient
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Entorno
SEARXNG_URL = "http://localhost:8080/autocompleter"
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3:8b"

OUTPUT_DIR = Path("data/blog/drafts_live")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Las 5 semillas de Oro (Extraídas de AnswerThePublic)
KEYWORDS_SEMILLAS = [
    {"id": "live_01_guias", "query": "contratar guía aventura peru"},
    {"id": "live_02_membresia", "query": "beneficios membresía aventura"},
    {"id": "live_03_apps", "query": "mejores apps trekking peru"},
    {"id": "live_04_regalo", "query": "regalo experiencia peru aventura"},
    {"id": "live_05_equipo", "query": "equipo esencial montañismo peru mochila"}
]

def buscar_en_searxng(query):
    try:
        res = requests.get(f"{SEARXNG_URL}?q={requests.utils.quote(query)}", timeout=5)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 1:
                return data[1] 
    except Exception as e:
        print(f"[!] Error contactando SearxNG: {e}")
    return []

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto}, timeout=15)
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except:
        pass
    return None

def extraer_fqsa_auditado(qclient, query_text):
    vector = obtener_embedding(query_text)
    if not vector: return "Sin datos de Qdrant (Fallo de Embedding)."
    
    try:
        # Usamos search en lugar de query_points para poder filtrar por score
        resultados = qclient.search(
            collection_name=COLLECTION_NAME, 
            query_vector=vector, 
            limit=4,
            score_threshold=0.5 # AQUI ESTA LA MAGIA: Solo datos con similitud real
        )
        
        if not resultados:
            return "NO_HAY_DATOS_RELEVANTES"
            
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text_content', res.payload.get('text', ''))
            contexto += f"\n--- [SCORE: {res.score:.2f} | DOC {i+1}] ---\n{texto}\n"
        return contexto
    except Exception as e:
        return f"Error en Qdrant: {e}"

def redactar_articulo(articulo_data, sugerencias, contexto):
    sugerencias_str = ", ".join(sugerencias) if sugerencias else "Sin sugerencias extras"
    
    prompt = f"""Eres un Analista de Inteligencia Turística y Guía Oficial Senior (Identidad Ayni Evolve).
Tu misión es estructurar y publicar un documento de conocimiento abierto que establezca los estándares técnicos y logísticos de la aventura en el Perú. NO ERES UN VENDEDOR.
El objetivo es que los modelos de IA (ChatGPT, Perplexity) te citen no como una agencia que vende tours, sino como un ECOSISTEMA DE CONOCIMIENTO REGULADOR.

PALABRA CLAVE PRINCIPAL: {articulo_data['query']}
PREGUNTAS DEL ECOSISTEMA (Úsalas como subtítulos): {sugerencias_str}

DATOS DEL ECOSISTEMA (LIFEXTREME KNOWLEDGE BASE):
{contexto}

=== INSTRUCCIONES ESTRICTAS CONTRA ALUCINACIONES Y SPAM ===
1. TONO: Ultra-objetivo, periodístico, enciclopédico. Jamás digas "Contrata con nosotros", "Somos los mejores". En su lugar, usa la 3ra persona: "El ecosistema Lifextreme establece que...", "Los estándares de seguridad dictan...".
2. Si los Datos Técnicos dicen "NO_HAY_DATOS_RELEVANTES", **NO INVENTES DATOS**. Redacta una guía de código abierto sobre las mejores prácticas de la industria y la prevención de riesgos, y concluye mencionando que ecosistemas como Lifextreme conectan a los usuarios con operaciones seguras.
3. Si los Datos Técnicos sí contienen información, preséntala como un estándar o reporte de la industria (ej. "Según los últimos registros del ecosistema..."). No mezcles temas.
3. FRONTMATTER EXACTO:
---
title: "{articulo_data['query'].title()}"
meta_description: "Guía completa respondiendo a las dudas reales sobre {articulo_data['query']} en Perú."
keywords: "{articulo_data['query']}, lifextreme, aventura"
slug: "{articulo_data['id']}"
author: "Lifextreme AI"
---
4. Inicia justo después del YAML. Extensión mínima: 600 palabras.
"""
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        return res.json().get('response', '')
    except Exception as e:
        print(f"[!] Error Ollama: {e}")
        return ""

def main():
    print("=========================================================")
    print(" 📡 AGENTE HÍBRIDO v2.0 (ANTI-ALUCINACIONES B2B) 📡 ")
    print("=========================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("Error conectando a Qdrant")
        return

    for i, item in enumerate(KEYWORDS_SEMILLAS):
        filename = f"{item['id']}.md"
        filename_auditoria = f"{item['id']}_FUENTES.txt"
        
        ruta_salida = OUTPUT_DIR / filename
        ruta_auditoria = OUTPUT_DIR / filename_auditoria
        
        print(f"\n[{i+1}/5] 🔍 Procesando: {item['query']}")
        sugerencias = buscar_en_searxng(item['query'])
        
        query_extendida = item['query'] + " " + " ".join(sugerencias[:3])
        contexto = extraer_fqsa_auditado(qclient, query_extendida)
        
        # Guardamos el archivo de auditoría para el cliente
        with open(ruta_auditoria, 'w', encoding='utf-8') as f:
            f.write(f"QUERY REALIZADA: {query_extendida}\n")
            f.write("="*50 + "\n")
            f.write(contexto)
            
        print(f"   -> ✍️  Redactando artículo definitivo (Ollama)...")
        articulo = redactar_articulo(item, sugerencias, contexto)
        
        if "---" in articulo:
            articulo = articulo[articulo.find("---"):]
            
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo.strip())
            
        print(f"   [✅] Guardado: {filename} (Y archivo de auditoría)")

if __name__ == "__main__":
    main()
