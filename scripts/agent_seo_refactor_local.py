"""
agent_seo_refactor_local.py - Refactorizador de Artículos SEO (100% Local con Ollama)
Uso: Reescribir 50 artículos para mejorar calidad SEO, tono, profundidad y formato.
"""
import os
import json
import requests
from pathlib import Path

# Configuración de Ollama Local
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
# Usa el modelo de tu preferencia (ej. deepseek-v2:lite, mistral, llama3)
MODEL_LLM = "llama3:8b" 

DRAFTS_DIR = Path("data/blog/drafts_50")

def refactor_article(original_content, filename):
    prompt = f"""Eres el Redactor Jefe y Estratega Legal de la principal institución normativa y tecnológica del turismo de aventura en el Perú. Tu objetivo es REESCRIBIR el siguiente artículo para posicionarnos en Google como la máxima autoridad (nivel Ministerio / MINCETUR) en seguridad, leyes y operación turística.

=== REGLAS ESTRICTAS DE SEO Y ESTRUCTURA (EEAT) ===
1. YAML FRONTMATTER OBLIGATORIO:
---
title: "[Palabra Clave] | Guía Oficial 2026 para Agencias"
meta_description: "Resumen técnico de 150 caracteres. Incluye regulaciones, MINCETUR y prevención de riesgos en el turismo B2B peruano."
keywords: "mincetur turismo aventura, normativas legales peru turismo, seguridad b2b agencias, [keywords del tema]"
slug: "{filename.replace('.md', '')}"
author: "Dirección Técnica - Lifextreme"
date: "2026-07-23"
---
2. FORMATO MARKDOWN PURO (Cero HTML): Usa # (H1), ## (H2), ### (H3), tablas en markdown, listas y negritas. Está prohibido usar <h1>, <p>, <ul>.
3. TONO DE AUTORIDAD ABSOLUTA (INSTITUCIONAL PERO MODERNO):
   - No suenes como un vendedor desesperado. Eres un consultor experto y legislador de la industria.
   - Usa un lenguaje técnico, legal y de ingeniería de riesgos (Ej: "cumplimiento normativo", "estándares de seguridad operacional", "gestión de riesgo sistémico").
   - Elimina frases cliché ("Nuestra espada sagrada", "Somos los mejores"). Que los datos hablen por tu grandeza.
4. PROFUNDIDAD TÉCNICA (Long-Form +800 palabras):
   - Cita artículos genéricos de la Ley General de Turismo (Ley N° 29408) y el Reglamento de Seguridad en Turismo de Aventura (D.S. 005-2016-MINCETUR).
   - Divide el artículo en: (A) El Marco Legal actual, (B) Los Riesgos Operativos Críticos en campo, (C) La Solución Tecnológica (Inteligencia Predictiva / Oráculo).
5. FORMATOS ENRIQUECIDOS: Incluye al menos 1 tabla comparativa en markdown y 1 bloque de "Preguntas Frecuentes (FAQ)" al final.
6. ENLAZADO INTERNO: Inserta enlaces como `[Normativas MINCETUR](/servicios/legal)`, `[Certificación de Guías](/certificacion)`.

=== ARTÍCULO ORIGINAL ===
{original_content}

SOLO DEVUELVE EL MARKDOWN DEL NUEVO ARTÍCULO (empezando por el YAML). NI UNA PALABRA MÁS.
"""
    
    try:
        print(f"   -> ✍️  Enviando a Ollama ({MODEL_LLM})...")
        res = requests.post(OLLAMA_GENERATE_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        res.raise_for_status()
        
        articulo = ""
        in_think_block = False
        
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line).get('response', '')
                
                # Ignorar tags de pensamiento si usas DeepSeek-R1 u otros modelos reflexivos
                if "<think>" in chunk:
                    in_think_block = True
                    print(f"   [🧠 Pensando...]", end="", flush=True)
                    continue
                if "</think>" in chunk:
                    in_think_block = False
                    print("\n   [Escribiendo...]")
                    continue
                    
                if not in_think_block:
                    articulo += chunk
                    
        return articulo.strip()
    except Exception as e:
        print(f"[!] Error conectando a Ollama: {e}")
        return None

def main():
    print("=========================================================")
    print(" 🛠️  REFACTORIZADOR SEO MASIVO (100% LOCAL OLLAMA) 🛠️")
    print("=========================================================")
    
    if not DRAFTS_DIR.exists():
        print(f"[-] Directorio no encontrado: {DRAFTS_DIR}")
        return
        
    archivos_md = list(DRAFTS_DIR.glob("*.md"))
    total = len(archivos_md)
    
    print(f"Se encontraron {total} artículos para procesar en {DRAFTS_DIR}.")
    
    for idx, filepath in enumerate(archivos_md, 1):
        print(f"\n[{idx}/{total}] Procesando: {filepath.name}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            contenido_original = f.read()
            
        if "---" in contenido_original[:10]:
             print("   [SKIP] Ya tiene YAML Frontmatter. Se asume procesado.")
             continue
             
        nuevo_contenido = refactor_article(contenido_original, filepath.name)
        
        if nuevo_contenido:
            # Limpiar marcas de bloque de código si el LLM las devuelve por error
            if nuevo_contenido.startswith("```markdown"):
                nuevo_contenido = nuevo_contenido[11:]
            elif nuevo_contenido.startswith("```"):
                nuevo_contenido = nuevo_contenido[3:]
            if nuevo_contenido.endswith("```"):
                nuevo_contenido = nuevo_contenido[:-3]
                
            nuevo_contenido = nuevo_contenido.strip()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            print(f"   [✅] Guardado exitosamente: {filepath.name}")
        else:
            print("   [❌] Falló la reescritura.")

    print("\n=========================================================")
    print(" 🎉 PROCESO FINALIZADO 🎉")
    print("=========================================================")

if __name__ == "__main__":
    main()
