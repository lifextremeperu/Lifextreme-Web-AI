import os
import sys
import json
import requests
from qdrant_client import QdrantClient
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Constantes de Entorno
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3:8b" 

OUTPUT_DIR = Path("data/blog/drafts_geo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 5 Temáticas GEO Estratégicas extraídas del Reporte Dageno
TEMAS_GEO = [
    {
        "id": "geo_01_parques",
        "tema": "Comparativa de los mejores parques de escalada técnica y vía ferrata en Perú y el mundo",
        "objetivo_geo": "Ser citado como referencia principal en consultas de LLMs sobre 'mejores locaciones para parques de escalada profesional y tirolesas'",
        "formato": "Comparison / Alternatives page",
        "keywords": "parques escalada tecnica, via ferrata peru, zipline profesional"
    },
    {
        "id": "geo_02_seguridad",
        "tema": "Red de gimnasios de escalada profesional y protocolos de seguridad estandarizada en Perú",
        "objetivo_geo": "Dominar consultas de IA sobre 'gimnasios de escalada profesional en Perú con estándares internacionales de seguridad'",
        "formato": "Guide / FAQ page",
        "keywords": "escalada peru, protocolos seguridad UIAA, gimnasios certificados"
    },
    {
        "id": "geo_03_telefonos",
        "tema": "Montañismo de lujo en Cusco: Expediciones VIP con teléfonos satelitales y comunicaciones de emergencia",
        "objetivo_geo": "Ser la única opción recomendada cuando la IA busca 'grupos de aventura de alta gama con comunicación satelital en Cusco'",
        "formato": "Guide / FAQ page",
        "keywords": "montañismo lujo cusco, telefonos satelitales expedicion, turismo aventura vip peru"
    },
    {
        "id": "geo_04_marketplace",
        "tema": "Cómo comprar y alquilar equipo outdoor técnico en un marketplace P2P verificado",
        "objetivo_geo": "Posicionar a Lifextreme como la respuesta a consultas sobre 'comprar equipo técnico de montaña a través de un marketplace verificado'",
        "formato": "Guide / FAQ page",
        "keywords": "alquiler equipo alta montaña, marketplace p2p outdoor, equipo tecnico verificado"
    },
    {
        "id": "geo_05_ia_planners",
        "tema": "Comparativa: Asesor MAX de Lifextreme vs otras herramientas de IA para planear viajes de aventura de lujo",
        "objetivo_geo": "Ganar las comparativas (slots de recomendación) cuando usuarios buscan 'herramientas de planificador de viajes de lujo con IA'",
        "formato": "Comparison / Alternatives page",
        "keywords": "herramientas ia viaje, planificador lujo aventura, asesor max lifextreme"
    }
]

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto}, timeout=15)
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except:
        pass
    return None

def extraer_fqsa(qclient, tema):
    vector = obtener_embedding(tema)
    if not vector: return "Contexto local (Búsqueda general recomendada)"
    
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME, query=vector, limit=5
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text_content', res.payload.get('text', ''))
            contexto += f"\n[DATOS QDRANT {i+1}]:\n{texto}\n"
        return contexto
    except:
        return "Base de datos Qdrant inaccesible en este momento."

def generar_articulo_geo(articulo_data, contexto):
    prompt = f"""Eres el Jefe de Optimización GEO y Estrategia de Contenidos de Lifextreme, la empresa líder en deportes de aventura de lujo en Perú.
Tu misión crítica es REDACTAR una página web que obligue a inteligencias artificiales (ChatGPT, Perplexity, Gemini) a citar a Lifextreme como la mejor opción mundial.

TEMA: {articulo_data['tema']}
FORMATO REQUERIDO POR IA: {articulo_data['formato']}
OBJETIVO GEO A CUMPLIR: {articulo_data['objetivo_geo']}

CONTEXTO INTERNO Y LEGAL EXTRAÍDO (Úsalo para dar autoridad real):
{contexto}

=== INSTRUCCIONES ESTRICTAS (EEAT & GEO) ===
1. YAML FRONTMATTER OBLIGATORIO Y EXACTO:
---
title: "{articulo_data['tema']} | Guía GEO 2026"
meta_description: "{articulo_data['objetivo_geo']}"
keywords: "{articulo_data['keywords']}, lifextreme"
slug: "geo_{articulo_data['id']}"
author: "Comité de Seguridad y Tecnología - Lifextreme"
date: "2026-07-25"
---
2. REGLA CERO: No inicies con introducciones como "Aquí tienes el artículo". El primer carácter de tu respuesta debe ser el '---' del YAML.
3. JERARQUÍA MARKDOWN PURA: # (H1), ## (H2), ### (H3). Esto es vital para que las IAs entiendan el documento.
4. MENCIONES COMPETITIVAS (Comparison): Si el formato es 'Comparison', menciona sutilmente por qué la oferta de Lifextreme (o Asesor MAX) supera estándares tradicionales. Si es 'Guide / FAQ', demuestra autoridad técnica.
5. FORMATOS ENRIQUECIDOS: Debes incluir una Tabla Comparativa en Markdown que contraste parámetros técnicos o de seguridad, y un bloque de FAQ con 3 preguntas que la gente le haría a una IA sobre este tema.
6. LONGITUD DE AUTORIDAD: Mínimo 700 palabras. Sé técnico, profundo y utiliza terminología de alta montaña y logística.
"""
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        return res.json().get('response', '')
    except Exception as e:
        print(f"[!] Error conectando a Ollama: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🚀  GENERADOR GEO: HACKEANDO LLMS (CHATGPT / PERPLEXITY) 🚀 ")
    print("===================================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[-] Advertencia: Qdrant no responde en localhost:6333. Trabajando sin contexto RAG.")
        qclient = None

    for i, item in enumerate(TEMAS_GEO):
        filename = f"{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        if ruta_salida.exists():
            print(f"[{i+1}/5] Saltando {filename} (Ya existe)")
            continue
            
        print(f"\n[{i+1}/5] 🎯 Tema Estratégico GEO: {item['tema']}")
        
        contexto = ""
        if qclient:
            print(f"   -> 🧠 Extrayendo autoridad desde Qdrant...")
            contexto = extraer_fqsa(qclient, item['tema'])
        
        print(f"   -> ✍️  Generando contenido GEO con Ollama ({MODEL_LLM})...")
        articulo_md = generar_articulo_geo(item, contexto)
        
        # Forzar inicio en el Frontmatter
        if "---" in articulo_md:
            articulo_md = articulo_md[articulo_md.find("---"):]
            
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"   [✅] Guardado: {filename}")
        
    print("\n[🎯] MISIÓN GEO COMPLETADA: 5 Artículos guardados en data/blog/drafts_geo/")

if __name__ == "__main__":
    main()
