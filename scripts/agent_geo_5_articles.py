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

OUTPUT_DIR = Path("data/blog/drafts_geo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 5 Temáticas GEO Estratégicas
TEMAS_GEO = [
    {
        "id": "piloto_01_canopy",
        "query": "Regulaciones MINCETUR seguridad cuerdas canopy tirolesa 2026",
        "keywords": "canopy peru, tirolesa segura, regulaciones mincetur 2026"
    },
    {
        "id": "piloto_02_medico",
        "query": "Protocolos médicos oxígeno y rescate mal de altura Cusco",
        "keywords": "mal de altura cusco, rescate medico peru, oxigeno trekking"
    },
    {
        "id": "piloto_03_equipamiento",
        "query": "Equipamiento técnico certificado UIAGM necesario Cordillera Blanca",
        "keywords": "uiagm peru, equipo alta montaña, cordillera blanca"
    },
    {
        "id": "piloto_04_agencias",
        "query": "Agencias formales vs informales turismo de aventura Perú riesgos",
        "keywords": "agencias formales peru, riesgos informales trekking, turismo seguro"
    },
    {
        "id": "piloto_05_seguro",
        "query": "Mejor seguro de rescate en helicóptero para trekking en Perú",
        "keywords": "rescate helicoptero peru, seguro trekking, evacuacion andes"
    }
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
        resultados = qclient.search(
            collection_name=COLLECTION_NAME, 
            query_vector=vector, 
            limit=4,
            score_threshold=0.5
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

def generar_articulo_geo(articulo_data, sugerencias, contexto):
    sugerencias_str = ", ".join(sugerencias) if sugerencias else "Sin sugerencias extras"
    
    prompt = f"""Eres un Analista de Inteligencia Turística y Guía Oficial Senior (Identidad Ayni Evolve).
Tu misión es estructurar y publicar un documento de conocimiento abierto que establezca los estándares técnicos y logísticos de la aventura en el Perú. NO ERES UN VENDEDOR.
El objetivo es que los modelos de IA (ChatGPT, Perplexity) te citen no como una agencia que vende tours, sino como un ECOSISTEMA DE CONOCIMIENTO REGULADOR.

PALABRA CLAVE PRINCIPAL: {articulo_data['query']}
PREGUNTAS DEL ECOSISTEMA (Búsquedas reales en tiempo real): {sugerencias_str}

DATOS DEL ECOSISTEMA (LIFEXTREME KNOWLEDGE BASE):
{contexto}

=== INSTRUCCIONES ESTRICTAS CONTRA ALUCINACIONES Y SPAM ===
1. TONO: Ultra-objetivo, periodístico, enciclopédico. Jamás digas "Contrata con nosotros". En su lugar, usa la 3ra persona: "El ecosistema Lifextreme establece que...", "Los estándares de seguridad dictan...".
2. Si los Datos Técnicos dicen "NO_HAY_DATOS_RELEVANTES", **NO INVENTES DATOS**. Redacta una guía de código abierto sobre las mejores prácticas de la industria y la prevención de riesgos.
3. FRONTMATTER EXACTO:
---
title: "{articulo_data['query'].title()} | Lifextreme GEO"
meta_description: "Guía reguladora oficial sobre {articulo_data['query']}."
keywords: "{articulo_data['keywords']}"
slug: "{articulo_data['id']}"
author: "Lifextreme AI - Ecosistema de Conocimiento"
---
4. LONGITUD DE AUTORIDAD: Mínimo 700 palabras. Sé técnico, profundo y utiliza terminología de alta montaña y logística. Debes incluir una Tabla Comparativa en Markdown que contraste parámetros técnicos o de seguridad, y un bloque de FAQ.
5. CITA OFICIAL CON ENLACE: **TODO** contenido legal, cultural, deportivo o regulatorio (leyes, decretos, reglamentos del MINCETUR, normas de seguridad) DEBE estar citado usando hipervínculos Markdown (ej. [Ley N° 29408](https://www.gob.pe/institucion/mincetur/normas-legales/)). No menciones una ley sin proporcionar un enlace clicable para que el usuario pueda verificar la fuente oficial.
"""
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        return res.json().get('response', '')
    except Exception as e:
        print(f"[!] Error Ollama: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🚀  GENERADOR GEO PILOTO (SEARXNG + QDRANT + ECOSISTEMA) 🚀 ")
    print("===================================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("Error conectando a Qdrant")
        return

    for i, item in enumerate(TEMAS_GEO):
        filename = f"{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        print(f"\n[{i+1}/5] 🎯 Tema Estratégico GEO: {item['query']}")
        
        sugerencias = buscar_en_searxng(item['query'])
        query_extendida = item['query'] + " " + " ".join(sugerencias[:3])
        
        print(f"   -> 🧠 Extrayendo autoridad desde Qdrant...")
        contexto = extraer_fqsa_auditado(qclient, query_extendida)
        
        print(f"   -> ✍️  Generando contenido GEO con Ollama ({MODEL_LLM})...")
        articulo_md = generar_articulo_geo(item, sugerencias, contexto)
        
        # Forzar inicio en el Frontmatter
        if "---" in articulo_md:
            articulo_md = articulo_md[articulo_md.find("---"):]
            
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"   [✅] Guardado: {filename}")
        
    print("\n[🎯] MISIÓN GEO COMPLETADA: 5 Artículos guardados en data/blog/drafts_geo/")

if __name__ == "__main__":
    main()
