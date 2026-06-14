import os
import json
import time
import requests
from urllib.parse import urlparse
from googlesearch import search

# ==============================================================================
# CONFIGURACIÓN DEL AGENTE ARAÑA (SPIDER)
# ==============================================================================
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_pdfs', 'chile'))
HISTORY_FILE = os.path.join(OUTPUT_DIR, 'descargas_history.json')
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"

# Asegurar que el directorio de salida existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def cargar_historial():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial(historial):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

def descargar_pdf(url, title):
    # Generar un nombre de archivo seguro
    safe_title = "".join([c if c.isalnum() else "_" for c in title]).strip("_")
    if not safe_title:
        safe_title = "documento_descargado"
        
    filename = f"{safe_title[:50]}_{int(time.time())}.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    try:
        print(f"    [DESCARGANDO] {url} ...")
        # Usamos un user-agent genérico para evitar bloqueos básicos
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Verificar que sea un PDF
        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
            print("    [WARNING] El enlace no parece ser un PDF válido. Se omitirá.")
            return False
            
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    
        print(f"    [ÉXITO] Guardado en: {filename}")
        return True
    except Exception as e:
        print(f"    [ERROR] Falló la descarga: {str(e)}")
        # Si se creó el archivo a medias, lo borramos
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

def evaluar_relevancia_con_ia(titulo, url, snippet):
    """
    Usa el modelo local Phi-3 para determinar si un documento encontrado
    es valioso para nuestra base de conocimiento logístico y turístico.
    """
    prompt = f"""Eres un clasificador de inteligencia B2B.
Evalúa el siguiente documento encontrado en internet para decidir si debemos descargarlo.
Buscamos documentos oficiales de planeamiento territorial, turismo, reportes de infraestructura, y rutas logísticas en Chile.
NO queremos panfletos comerciales simples, publicidad, o artículos de opinión sin datos.

Título: {titulo}
URL: {url}
Resumen: {snippet}

¿Es este documento útil e institucional?
Responde ÚNICAMENTE con la palabra "SI" o "NO"."""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=20)
        if response.status_code == 200:
            result = response.json().get("response", "").strip().upper()
            return "SI" in result or "SÍ" in result
    except Exception as e:
        print(f"    [ERROR LLM] No se pudo consultar a Ollama: {str(e)}")
    
    # En caso de duda o error de IA, descargamos por si acaso (fail-safe open)
    return True

def run_spider(queries, max_results_per_query=5):
    historial = cargar_historial()
    urls_descargadas = [h.get("url") for h in historial]
    
    print("================================================================")
    print(" LIFEXTREME SPIDER - Módulo de Rastreo Autónomo (CHILE)")
    print(" Modelo Analista:", MODEL_NAME)
    print(" Destino de Datos:", OUTPUT_DIR)
    print("================================================================\n")
    
    # Fallback URLs directas masivas para Chile (por si Google bloquea el script)
    contingencia_chile = [
        "https://www.sernatur.cl/wp-content/uploads/2018/11/Estrategia-Nacional-de-Turismo-2012-2020.pdf",
        "https://subturismo.gob.cl/wp-content/uploads/2015/10/Plan-Nacional-de-Desarrollo-Turistico-Sustentable.pdf",
        "https://www.sernatur.cl/wp-content/uploads/2021/08/Plan-de-Accion-Turismo-Atacama.pdf",
        "https://www.mop.cl/wp-content/uploads/2023/05/Plan-Nacional-de-Infraestructura-para-la-Movilidad-2020-2050.pdf",
        "https://senapred.cl/wp-content/uploads/2023/01/Plan-Estrategico-Nacional-para-la-Reduccion-del-Riesgo-de-Desastres.pdf"
    ]
    
    with_ai = True  # Para control
    
    for query in queries:
        print(f"[*] Buscando en Google: '{query}'")
        try:
            # googlesearch retorna iterador de URLs
            # usar sleep_interval=2 para evitar bloqueos
            results = list(search(query, num_results=max_results_per_query, sleep_interval=2))
            
            if not results:
                print("    No se encontraron resultados en Google (posible bloqueo de IP). Usando fuentes directas de contingencia...")
                results = contingencia_chile
                
            for url in results:
                if url in urls_descargadas:
                    print(f"  - [OMITIDO] Ya descargado: {url}")
                    continue
                    
                # Extraemos un titulo crudo de la URL
                title = os.path.basename(urlparse(url).path)
                if not title:
                    title = "documento"
                    
                print(f"  -> Analizando candidato URL: {url[:60]}...")
                
                # Para simplificar la prueba y no saturar a Google, omitimos la búsqueda de snippet,
                # usamos la url para que la IA decida.
                es_relevante = evaluar_relevancia_con_ia(title, url, "Documento encontrado en Google Búsqueda.")
                
                if es_relevante:
                    print(f"    [APROBADO por IA] Procediendo a descargar...")
                    exito = descargar_pdf(url, title)
                    if exito:
                        historial.append({
                            "titulo": title,
                            "url": url,
                            "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "pais": "Chile"
                        })
                        guardar_historial(historial)
                        urls_descargadas.append(url)
                else:
                    print(f"    [RECHAZADO por IA] No es relevante.")
                
                time.sleep(2)
                
        except Exception as e:
            print(f"[!] Error ejecutando la búsqueda para '{query}': {str(e)}")

if __name__ == "__main__":
    # Búsquedas estratégicas para minería en Chile
    busquedas = [
        "Estrategia Nacional de Turismo Chile 2030 pdf",
        "Plan de Desarrollo Turistico Atacama pdf",
        "Plan Nacional Infraestructura Movilidad Chile pdf MOP"
    ]
    
    run_spider(busquedas, max_results_per_query=2)
    print("\n[OK] Escaneo autonomo finalizado. Revisa la carpeta data/raw_pdfs/chile.")
