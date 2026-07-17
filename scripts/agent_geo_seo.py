import os
import sys
import requests
from qdrant_client import QdrantClient
from pathlib import Path

# Configuración UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Constantes
QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL_EMBED = "nomic-embed-text"
MODEL_LLM = "llama3:8b" 

# Crear carpeta de destino
OUTPUT_DIR = Path("data/blog/geo_seo")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def obtener_embedding(texto):
    try:
        res = requests.post(OLLAMA_EMBED_URL, json={"model": MODEL_EMBED, "input": texto})
        if res.status_code == 200:
            return res.json().get('embeddings', [])[0]
    except Exception as e:
        print(f"Error generando embedding: {e}")
    return None

def extraer_fqsa_region(qclient, region, tema):
    query = f"Reglamentos, leyes, riesgos y características logísticas de turismo en {region}. {tema}"
    vector = obtener_embedding(query)
    if not vector: return ""
    
    print(f"[*] Escaneando vectores para la región: {region}...")
    try:
        resultados = qclient.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=5
        ).points
        contexto = ""
        for i, res in enumerate(resultados):
            texto = res.payload.get('text', '')
            fuente = res.payload.get('source', 'Desconocido')
            contexto += f"\n[Documento {i+1} | {fuente}]:\n{texto}\n"
        return contexto
    except Exception as e:
        print(f"Error en Qdrant: {e}")
        return ""

def generar_articulo_seo(region, tema, contexto):
    print(f"[*] Escribiendo artículo SEO para {region} con la data técnica extraída...")
    
    prompt = f"""Eres el Jefe de Marketing B2B y Experto en SEO Local (Geo-SEO) de Lifextreme AI, la autoridad peruana en turismo.
Tu tarea es escribir un artículo de blog HIPER-LOCALIZADO altamente optimizado para Google.

TEMA: {tema} en {region}

REGLA DE ORO (EEAT): Google premia la precisión. Utiliza OBLIGATORIAMENTE la siguiente información técnica extraída de nuestra base de datos legal (FQSAs) para nutrir el artículo. Cita las normas, riesgos o detalles técnicos que encuentres en este contexto para demostrar autoridad absoluta.

CONTEXTO VECTORIAL DE QDRANT:
{contexto}

ESTRUCTURA DEL ARTÍCULO (Solo formato Markdown):
1. Un Título Principal (H1) que enganche (incluye el nombre de la región y el año 2026).
2. Un párrafo introductorio fuerte.
3. Subtítulos (H2 y H3) separando la información técnica/legal, los riesgos logísticos y consejos.
4. Conclusión y Llamado a la Acción (CTA) para contactar a Lifextreme.
5. REFERENCIAS Y FUENTES (H2): Es OBLIGATORIO incluir una sección final listando los nombres exactos de los documentos y fuentes que te he pasado en el contexto (Ej: Ley General de Turismo, Reglamento de SERNANP, etc.).

NO incluyas saludos. Devuelve ÚNICAMENTE el artículo en formato Markdown.
"""
    
    import json
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": True
        }, stream=True)
        
        print("\n[Escribiendo...]\n")
        articulo = ""
        for line in res.iter_lines():
            if line:
                chunk = json.loads(line).get('response', '')
                print(chunk, end='', flush=True)
                articulo += chunk
        print("\n")
        return articulo
    except Exception as e:
        print(f"Error en Ollama: {e}")
        return ""

def main():
    print("==================================================")
    print(" 🌍 GENERADOR GEO-SEO CON INTELIGENCIA VECTORIAL 🌍")
    print("==================================================")
    
    try:
        qclient = QdrantClient(url=QDRANT_URL, timeout=10)
    except:
        print("[!] Asegúrate de que Qdrant esté corriendo.")
        return

    # Parámetros del experimento
    region_objetivo = "Huaraz (Áncash)"
    tema_objetivo = "Guía de Riesgos y Protocolos de Alta Montaña"
    
    print(f"\nIniciando investigación automatizada para: {tema_objetivo} en {region_objetivo}")
    
    contexto_real = extraer_fqsa_region(qclient, region_objetivo, tema_objetivo)
    
    if not contexto_real.strip():
        print("[!] No se encontró información vectorial para esta región.")
        return
        
    print(f"[+] ¡Éxito! Se extrajo el núcleo legal y de riesgo para {region_objetivo}.")
    
    articulo_md = generar_articulo_seo(region_objetivo, tema_objetivo, contexto_real)
    
    # Limpiar backticks si el modelo los devuelve
    if articulo_md.startswith("```markdown"):
        articulo_md = articulo_md[11:]
    if articulo_md.startswith("```"):
        articulo_md = articulo_md[3:]
    if articulo_md.endswith("```"):
        articulo_md = articulo_md[:-3]
    
    # Guardar en disco
    filename = f"seo_{region_objetivo.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('á', 'a')}.md"
    ruta_salida = OUTPUT_DIR / filename
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(articulo_md.strip())
        
    print("\n==================================================")
    print(f"✅ ¡ARTÍCULO GEO-SEO GENERADO CON ÉXITO!")
    print(f"📁 Guardado en: {ruta_salida}")
    print("==================================================")

if __name__ == "__main__":
    main()
