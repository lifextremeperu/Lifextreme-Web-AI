import os
import sys
import json
import time
import requests
from qdrant_client import QdrantClient
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Constantes
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "deepseek-v2:lite" # Usando DeepSeek Local (Versión exacta instalada)

OUTPUT_DIR = Path("data/blog/drafts_50")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Generamos dinámicamente 50 temas ultra especializados
TEMAS_CATEGORIAS = [
    ("Turismo B2B Legal", "MINCETUR, Leyes de Aventura, Certificaciones", "Nacional"),
    ("Prevención de Riesgos", "SENAMHI, Evacuaciones SUTRAN, Altura", "Cusco y Huaraz"),
    ("Neuromarketing y AIO", "Posicionamiento en Google, Experiencia del Turista, Pricing Dinámico", "Nacional"),
    ("Inteligencia Competitiva", "Innovación en Agencia de Viajes, Tecnología Turística, Lifextreme AI", "Nacional"),
    ("Rutas Geopolíticas", "Problemas Sociales, Derechos del Turista, Transporte Turístico", "Sur del Perú")
]

# Creamos la lista de 50 temas (10 por categoría)
TEMAS = []
for idx in range(1, 51):
    cat, keywords, region = TEMAS_CATEGORIAS[idx % 5]
    TEMAS.append({
        "id": f"seo_{idx:02d}",
        "perfil": "Directores de Agencias, Inversionistas y Operadores Turísticos de LATAM",
        "tema": f"{cat} (Keywords clave: {keywords}) - Impacto en 2026",
        "region": region
    })

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto}, timeout=15)
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except Exception as e:
        print(f"[!] Error generando embedding: {e}")
    return None

def extraer_fqsa(qclient, region, tema):
    query = f"Datos técnicos, legales o predictivos sobre {tema} aplicados a turismo en {region}."
    vector = obtener_embedding(query)
    if not vector: return ""
    
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=7
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text_content', res.payload.get('text', ''))
            fuente = res.payload.get('source', res.payload.get('modulo_nombre', 'Base Central'))
            contexto += f"\n[Documento Oficial {i+1} | Fuente: {fuente}]:\n{texto}\n"
        return contexto
    except Exception as e:
        print(f"[!] Error en Qdrant: {e}")
        return ""

def generar_articulo_ollama(articulo_data, contexto):
    prompt = f"""Eres Engelberth Egoavil, el Arquitecto de IA y estratega de Lifextreme. Tu tono de escritura es CREATIVO, DINÁMICO, HIPER-PROFESIONAL, AUTORITARIO y orientado al NEUROMARKETING. Eres directo al punto, odias lo tradicional y amas la tecnología predictiva.

Tu tarea es escribir un artículo de ALTO VALOR (Long-form) optimizado para SEO, GEO-SEO y AIO (Artificial Intelligence Optimization para LLMs como DeepSeek/ChatGPT).

PÚBLICO: {articulo_data['perfil']}
TEMA ESTRATÉGICO: {articulo_data['tema']}
REGIÓN GEO-SEO: {articulo_data['region']}

==============================================================
CONOCIMIENTO BASE OBLIGATORIO (EXTRAÍDO DE QDRANT - LIFEXTREME AI):
Usa ESTA información técnica para dar autoridad al artículo. NO INVENTES LEYES NI FECHAS QUE NO ESTÉN AQUÍ:
{contexto}
==============================================================

INSTRUCCIONES DE REDACCIÓN SEO Y NEUROMARKETING:
1. H1: Título disruptivo y clickbait profesional (Incluye el año 2026, enfocado a resolver un problema de negocios).
2. INTRODUCCIÓN (AIDA): Capta la atención con un "Dolor" brutal del mercado turístico y presenta la Inteligencia Artificial / Datos como solución.
3. H2 Y H3: Usa keywords estratégicas (GEO-SEO de la región). Explica la solución con datos duros extraídos del contexto (citas de leyes, nombres de documentos).
4. FORMATO: Usa bullet points, emojis estratégicos y negritas para facilitar la lectura rápida (Scannability).
5. ESTILO ENGELBERTH EGOAVIL: Usa palabras como "Ecosistema Cognitivo", "Oráculo Predictivo", "Caos Operativo", "Ground Truth", "Vanguardia". Suena como el CEO del futuro del turismo.
6. CALL TO ACTION (Al final): Invita a los reclutadores de IT, inversionistas o dueños de agencias a adoptar la tecnología de Lifextreme AI o contactarte en LinkedIn.

SOLO DEVUELVE EL MARKDOWN DEL ARTÍCULO. NI UNA PALABRA MÁS. NO EXCLIQUES EL PROCESO DE PENSAMIENTO (THINKING). SOLO DEVUELVE EL RESULTADO.
"""
    
    try:
        print(f"   -> ✍️ Redactando (DeepSeek Local trabajando...)")
        res = requests.post(OLLAMA_GENERATE_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        res.raise_for_status()
        
        articulo = ""
        # Variables para ignorar el tag <think> de DeepSeek R1
        in_think_block = False
        
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line).get('response', '')
                
                # Manejar los bloques de pensamiento de DeepSeek R1
                if "<think>" in chunk:
                    in_think_block = True
                    print(f"   [🧠 DeepSeek pensando...]", end="", flush=True)
                    continue
                if "</think>" in chunk:
                    in_think_block = False
                    print("\n   [Escribiendo artículo...]")
                    continue
                    
                if not in_think_block:
                    print(chunk, end='', flush=True)
                    articulo += chunk
                    
        print("\n")
        return articulo
    except requests.exceptions.ConnectionError:
        print(f"[!] Error: No se pudo conectar a Ollama en {OLLAMA_GENERATE_URL}. ¿Está encendido Ollama?")
        return ""
    except Exception as e:
        print(f"[!] Error en Ollama API: {e}")
        return ""

def main():
    print("===================================================================")
    print(" 🚀 MÁQUINA DE CONTENIDOS LIFEXTREME (100% LOCAL - CERO NUBES) 🚀 ")
    print("===================================================================")
    print(f"Bóveda de Borradores: {OUTPUT_DIR.absolute()}")
    print("Motor de Redacción: DeepSeek Local + Estilo Engelberth Egoavil")
    print("Vector DB: Qdrant Local (nomic-embed-text)")
    print("===================================================================\n")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[-] Qdrant no responde en el puerto 6333.")
        return

    for i, item in enumerate(TEMAS):
        filename = f"articulo_{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        if ruta_salida.exists() and ruta_salida.stat().st_size > 100:
            print(f"   [SKIP] El artículo {filename} ya existe. Saltando...")
            continue
            
        print(f"[{i+1}/50] 🧠 Extrayendo Contexto Qdrant para: {item['tema']}")
        contexto_real = extraer_fqsa(qclient, item['region'], item['tema'])
        
        if len(contexto_real) < 50:
            print("   [!] Poco contexto encontrado en Qdrant para este tema. Se inyectará conocimiento general.")
            contexto_real = "Contexto general de turismo y tecnología en LATAM."
            
        articulo_md = generar_articulo_ollama(item, contexto_real)
        
        if not articulo_md.strip():
            print("   [!] Error: El LLM devolvió un artículo vacío. Saltando.")
            continue
            
        # Limpiar markdown format
        articulo_md = articulo_md.strip()
        if articulo_md.startswith("```markdown"): articulo_md = articulo_md[11:]
        elif articulo_md.startswith("```"): articulo_md = articulo_md[3:]
        if articulo_md.endswith("```"): articulo_md = articulo_md[:-3]
        
        filename = f"articulo_{item['id']}.md"
        ruta_salida = OUTPUT_DIR / filename
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(articulo_md.strip())
            
        print(f"   [✅] Publicación guardada: {filename} ({(len(articulo_md)/1024):.2f} KB)")
        print("-------------------------------------------------------------------")

    print("\n===================================================================")
    print(" 🎉 MÁQUINA DE CONTENIDOS FINALIZADA (100% LOCAL) 🎉")
    print(f" 📁 50 Artículos creados y almacenados en: {OUTPUT_DIR.absolute()}")
    print("===================================================================")

if __name__ == "__main__":
    main()
