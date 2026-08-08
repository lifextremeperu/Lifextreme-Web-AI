"""
agent_automated_growth.py - NEO V2 (Orquestador Automático de Crecimiento SEO/GEO/AEO)
Estrategia: Basado en FQSA (Frequently Questioned Safety Attributes) y Conocimiento Profundo.

Misión Diaria: Toma un tema (FQSA) de alto valor técnico, extrae los vectores de Qdrant y genera:
1. AEO: JSON-LD FAQPage para la web.
2. GEO: Tabla de Riesgo/Normativa en HTML.
3. SEO: Artículo de Autoridad en Markdown.
"""
import os
import json
import httpx
import asyncio
from datetime import datetime
from qdrant_client import AsyncQdrantClient
from pathlib import Path
import random

OLLAMA_URL = "http://localhost:11434"
QDRANT_URL = "http://localhost:6333"
KNOWLEDGE_VAULT = "Lifextreme_Knowledge"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "mistral:latest"

qclient = AsyncQdrantClient(url=QDRANT_URL)

AEO_OUTPUT_DIR = Path("frontend/public/aeo_data")
GEO_OUTPUT_DIR = Path("frontend/public/dashboards")
SEO_OUTPUT_DIR = Path("data/blog/boletines_tecnicos")

for d in [AEO_OUTPUT_DIR, GEO_OUTPUT_DIR, SEO_OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Catálogo de FQSAs (Temas de Alta Autoridad B2B/B2C)
CATALOGO_FQSA = [
    {"id": "canopy_reg", "tema": "Regulaciones MINCETUR seguridad cuerdas canopy tirolesa"},
    {"id": "rescate_medico", "tema": "Protocolos médicos oxígeno y rescate mal de altura Andes"},
    {"id": "certificacion_uiagm", "tema": "Equipamiento técnico certificado UIAGM necesario Cordillera Blanca"},
    {"id": "riesgo_informalidad", "tema": "Agencias formales vs informales turismo de aventura Perú riesgos y multas"},
    {"id": "evacuacion_heli", "tema": "Seguro de rescate en helicóptero y protocolos de evacuación Cusco"}
]

async def obtener_embedding(texto: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": texto})
        return res.json().get("embedding", [])

async def extraer_contexto_qdrant(query: str, limit=4) -> str:
    vector = await obtener_embedding(query)
    if not vector: return ""
    
    try:
        search_result = await qclient.query_points(
            collection_name=KNOWLEDGE_VAULT, query=vector, limit=limit, score_threshold=0.3
        )
        contexto = ""
        for i, p in enumerate(search_result.points):
            texto = p.payload.get("text_content", "")
            contexto += f"\n--- [Vector {i+1}] ---\n{texto}\n"
        return contexto
    except Exception as e:
        print(f"[!] Qdrant Error: {e}")
        return ""

async def generar_con_llm(prompt_sistema: str, prompt_usuario: str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        res = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": LLM_MODEL, "system": prompt_sistema, "prompt": prompt_usuario, "stream": False}
        )
        if res.status_code == 200:
            return res.json().get("response", "")
        return ""

async def main():
    print("==================================================")
    print(" LIFEXTREME NEO - MOTOR DE AUTORIDAD (FQSA RAG)")
    print("==================================================")
    
    # Elegimos un FQSA del catálogo para el trabajo del día
    fqsa_del_dia = random.choice(CATALOGO_FQSA)
    print(f"[*] FQSA Seleccionado hoy: {fqsa_del_dia['tema']}")
    
    print("[*] Extrayendo conocimiento profundo de vectores en Qdrant...")
    contexto = await extraer_contexto_qdrant(fqsa_del_dia['tema'])
    
    if not contexto:
        print("[!] No se encontró conocimiento en Qdrant sobre este FQSA. Abortando.")
        return
        
    print(">> [AEO] Generando JSON-LD (FAQPage) basado en vectores...")
    aeo_sys = "Eres un estructurador SEO técnico. Devuelve SOLO código JSON-LD tipo FAQPage válido con 3 preguntas clave sobre este contexto. No uses formato markdown."
    aeo_res = await generar_con_llm(aeo_sys, f"Contexto vectorial: {contexto}. Genera el JSON.")
    aeo_res = aeo_res.replace("```json", "").replace("```", "").strip()
    with open(AEO_OUTPUT_DIR / f"aeo_{fqsa_del_dia['id']}.json", "w", encoding="utf-8") as f:
        f.write(aeo_res)
        
    print(">> [GEO] Generando Dashboard Comparativo HTML...")
    geo_sys = "Eres un Auditor GovTech. Devuelve SOLO código HTML de una <table> comparando el 'Riesgo Informal' vs 'Estándar Lifextreme (Mincetur/UIAGM)'."
    geo_res = await generar_con_llm(geo_sys, f"Contexto vectorial: {contexto}. Crea la tabla comparativa.")
    geo_res = geo_res.replace("```html", "").replace("```", "").strip()
    with open(GEO_OUTPUT_DIR / f"geo_{fqsa_del_dia['id']}.html", "w", encoding="utf-8") as f:
        f.write(geo_res)
        
    print(">> [SEO] Redactando Artículo Técnico de Autoridad...")
    seo_sys = "Eres un especialista UIAGM/Mincetur de Lifextreme. Escribe un artículo técnico en Markdown usando los datos vectoriales. Usa tono de autoridad B2B, no vendedor."
    seo_res = await generar_con_llm(seo_sys, f"Tema: {fqsa_del_dia['tema']}. Contexto: {contexto}. Escribe el post.")
    with open(SEO_OUTPUT_DIR / f"seo_{fqsa_del_dia['id']}.md", "w", encoding="utf-8") as f:
        f.write(seo_res)
        
    print("[+] NEO terminó su ciclo diario de crecimiento FQSA con éxito.")

if __name__ == "__main__":
    asyncio.run(main())
