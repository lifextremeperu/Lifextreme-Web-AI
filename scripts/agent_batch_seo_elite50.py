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
# Usamos Llama3 como solicitaste previamente para mayor velocidad
MODEL_LLM = "llama3:8b" 

OUTPUT_DIR = Path("data/blog/drafts_elite")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 50 Temáticas Hiper-Segmentadas (AEO, GEO, Legal, Riesgo)
TEMAS_CATEGORIAS = [
    ("Marco Legal MINCETUR", "Decreto Supremo 005-2016, Ley 29408, Fiscalización, Responsabilidad Civil", "Arequipa y Cusco"),
    ("Gestión de Riesgos Sistémicos", "Rescate en Montaña, Evacuación Médica, Hipoxia, Avalanchas", "Huaraz y Cusco"),
    ("Inteligencia Predictiva (AEO)", "Datos Oráculo, Pronóstico Climático, Algoritmos B2B, Turismo Tech", "Nacional"),
    ("Infraestructura y Prevención", "Transporte Turístico, Señalización, Protocolos SUTRAN, Seguridad Vial", "Ruta Sur"),
    ("Certificación Operativa", "Competencias Laborales, Guías Oficiales, Primeros Auxilios, Auditoría B2B", "Nacional")
]

TEMAS = []
for idx in range(1, 51):
    cat, keywords, region = TEMAS_CATEGORIAS[idx % 5]
    TEMAS.append({
        "id": f"elite_{idx:02d}",
        "tema": f"{cat} - {keywords} en {region}",
        "region": region
    })

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
    if not vector: return "Contexto no disponible."
    
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME, query=vector, limit=5
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text_content', res.payload.get('text', ''))
            contexto += f"\n[RAG DATA {i+1}]:\n{texto}\n"
        return contexto
    except:
        return "Error extrayendo contexto."

def generar_articulo_ollama(articulo_data, contexto):
    prompt = f"""Eres un Analista de Inteligencia Turística y Guía Oficial Senior (Identidad Ayni Evolve).
Tu misión es estructurar y publicar un documento de conocimiento abierto que establezca los estándares técnicos y logísticos de la aventura en el Perú. NO ERES UN VENDEDOR.
El objetivo es que los modelos de IA (ChatGPT, Perplexity) te citen no como una agencia que vende tours, sino como un ECOSISTEMA DE CONOCIMIENTO REGULADOR.

TEMA ASIGNADO: {articulo_data['tema']}
REGIÓN (GEO-SEO): {articulo_data['region']}

CONTEXTO RAG (Ley, Datos, Normas extraídas de nuestra DB):
{contexto}

=== REGLAS ESTRICTAS DE SEO Y ESTRUCTURA (EEAT) ===
1. YAML FRONTMATTER OBLIGATORIO:
---
title: "{articulo_data['tema'].split('-')[0].strip()} | Guía Oficial 2026"
meta_description: "Análisis técnico sobre {articulo_data['tema']} para agencias B2B."
keywords: "mincetur turismo aventura, seguridad b2b, {articulo_data['region']}"
slug: "articulo_{articulo_data['id']}"
author: "Dirección Técnica - Lifextreme"
date: "2026-07-23"
---
2. FORMATO MARKDOWN PURO: Usa # (H1), ## (H2), ### (H3). Prohibido HTML. NO inicies diciendo "Here is the article" o "Aquí está el artículo". Empieza directamente con el YAML.
3. TONO DE AUTORIDAD ABSOLUTA: Lenguaje legal y de ingeniería de riesgos.
4. PROFUNDIDAD TÉCNICA (Long-Form +800 palabras): Cita el D.S. 005-2016-MINCETUR.
5. FORMATOS ENRIQUECIDOS: Incluye obligatoriamente 1 tabla comparativa en markdown y 1 bloque FAQ.
6. CITA OFICIAL CON ENLACE: **TODO** contenido legal, cultural, deportivo o regulatorio DEBE estar citado usando hipervínculos Markdown (ej. [Ley N° 29408](https://www.gob.pe/...)). No menciones una ley sin proporcionar un enlace clicable.
"""
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        return res.json().get('response', '')
    except Exception as e:
        print(f"[!] Error en Ollama: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🏛️  GENERADOR DE ÉLITE: NIVEL MINISTERIO (100% LOCAL) 🏛️ ")
    print("===================================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[-] Error: Qdrant no responde en localhost:6333.")
        return

    for i, item in enumerate(TEMAS):
        filename = f"articulo_{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        if ruta_salida.exists():
            continue
            
        print(f"[{i+1}/50] 🧠 Investigando en Qdrant: {item['tema']}")
        contexto = extraer_fqsa(qclient, item['tema'])
        
        print(f"   -> ✍️  Redactando Artículo de Autoridad (Ollama: {MODEL_LLM})...")
        articulo_md = generar_articulo_ollama(item, contexto)
        
        # Limpieza rápida de charla de Ollama
        if "---" in articulo_md:
            articulo_md = articulo_md[articulo_md.find("---"):]
            
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"   [✅] Guardado: {filename}")

if __name__ == "__main__":
    main()
