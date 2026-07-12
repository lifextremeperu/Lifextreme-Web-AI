import os
import sys
import re
import json
import glob
import requests
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import time

def init_qdrant():
    client = QdrantClient("http://localhost:6333")
    collection_name = "Lifextreme_Knowledge"
    
    # Crear coleccion si no existe
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"[*] Colección '{collection_name}' creada en Qdrant.")
    return client, collection_name

def is_peru_file(filename):
    # Excluir documentos internacionales
    international_keywords = ['bolivia', 'chile', 'argentina', 'ecuador', 'colombia', 'brasil']
    lower_name = filename.lower()
    for kw in international_keywords:
        if kw in lower_name:
            return False
    return True

def extract_department(filename):
    # Intentar extraer el nombre del departamento del archivo
    # Ej: "Ontología Turística de Ancash.pdf" -> "ancash"
    match = re.search(r'de\s([A-Za-záéíóúÁÉÍÓÚñÑ]+)(?:\.|\s)', filename, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    # Si no tiene "de", buscar la primera palabra despues de Turística
    match = re.search(r'Turística\s([A-Za-záéíóúÁÉÍÓÚñÑ]+)', filename, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return "peru"

def extract_knowledge_llama3(pdf_text, region):
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""
🚨 DIRECTIVA DE INTELIGENCIA (EXTRACCIÓN COMPLETA DE ECOSISTEMA TURÍSTICO):
Eres el Asesor Experto en Turismo de Aventura de Lifextreme. 
Analiza este extracto de Investigación de Mercado / Ontología de {region.upper()}.

OBJETIVO CRÍTICO:
Extrae absolutamente TODA la información relevante sobre el destino, sin repetir datos obvios ni alucinar. Analiza a fondo y extrae:
1. Destinos turísticos específicos y rutas detalladas.
2. Parques de Aventura, Palestras (muros de escalada) y zonas de camping.
3. Deportes de aventura que se practican en la zona (escalada, trekking, sandboard, etc.).
4. Logística, tiempos de viaje, distancias y vías de transporte (carreteras, estado de las vías).
5. Proveedores, operadores locales y precios de servicios o infraestructura técnica disponible.

Genera un JSON con la clave "insights" que contenga una lista de textos. 
Cada texto debe ser un dato real y específico extraído del texto, detallando como experto.
Ej: {{"insights": ["El parque de aventura Y tiene palestras de 15 metros y se llega por la vía Z en 2 horas.", "El deporte X se practica en la locación W, operado por la empresa V a un costo promedio de..."]}}

No devuelvas NADA MÁS que el objeto JSON puro, sin explicaciones ni alucinaciones. Extrae SOLO lo que está en el texto original.

TEXTO DEL PDF (Fragmento):
{pdf_text}
"""

    payload = {
        "model": "llama3:8b",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_ctx": 8192}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json().get("response", "{}")
        data = json.loads(result)
        return data.get("insights", [])
    except requests.exceptions.Timeout:
        print(f"[-] Llama3 tardó demasiado (Timeout). Saltando bloque para evitar congelamiento.")
        return []
    except requests.exceptions.ConnectionError:
        print(f"[-] Ollama se desconectó (Probable límite de memoria). Esperando 5 segundos...")
        time.sleep(5)
        return []
    except Exception as e:
        print(f"[-] Error extrayendo conocimiento con Llama3: {e}")
        return []

def generate_local_embeddings(texts):
    url = "http://localhost:11434/api/embed"
    payload = {
        "model": "nomic-embed-text:latest",
        "input": texts
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("embeddings", [])
    except Exception as e:
        print(f"[-] Error generando vectores con Nomic: {e}")
        return []

def process_pdf(pdf_path, qdrant_info, test_mode=False):
    qclient, collection_name = qdrant_info
    filename = os.path.basename(pdf_path)
    region = extract_department(filename)
    print(f"\n[>>>] PROCESANDO: {filename} (Región: {region.upper()})")
    
    try:
        region_count = qclient.count(
            collection_name=collection_name,
            count_filter=Filter(
                must=[
                    FieldCondition(key="region", match=MatchValue(value=region))
                ]
            )
        ).count
        
        if region_count > 0:
            print(f"[*] La región '{region.upper()}' ya tiene {region_count} vectores en Qdrant. ¡Saltando para ahorrar tiempo!")
            return
    except Exception as e:
        print(f"[-] Error verificando vectores existentes: {e}")


    try:
        reader = PdfReader(pdf_path)
        pages = reader.pages
    except Exception as e:
        print(f"[-] Error leyendo PDF: {e}")
        return
    
    all_insights = []
    chunk_size = 3
    
    print(f"[*] El documento tiene {len(pages)} páginas. Procesando en bloques de {chunk_size} páginas...")
    
    for i in range(0, len(pages), chunk_size):
        chunk_pages = pages[i:i+chunk_size]
        pdf_text_chunk = ""
        for page in chunk_pages:
            try:
                pdf_text_chunk += page.extract_text() + "\n"
            except:
                pass
                
        print(f"    [+] Extrayendo Insights del bloque (págs {i+1} a {min(i+chunk_size, len(pages))})...")
        # Asegurar no rebasar el contexto límite cortando a 25000 chars por bloque por seguridad
        insights_chunk = extract_knowledge_llama3(pdf_text_chunk[:25000], region)
        
        if insights_chunk:
            all_insights.extend(insights_chunk)
            print(f"        -> Se extrajeron {len(insights_chunk)} datos de este bloque.")
            
    if not all_insights:
        print("[-] No se pudo extraer conocimiento nuevo de todo el documento.")
        return
        
    print(f"[+] Se encontraron {len(all_insights)} insights en TOTAL. Generando Vectores (Nomic)...")
    insights = all_insights
    
    # Preparar el contenido textual de cada insight para el RAG
    formatted_texts = [f"Investigación de Mercado ({region.upper()}): {insight}" for insight in insights]
    
    embeddings = generate_local_embeddings(formatted_texts)
    
    if not embeddings or len(embeddings) != len(formatted_texts):
        print("[-] Error: Falló la vectorización.")
        return
        
    print("[+] Inyectando en Qdrant...")
    points = []
    
    for idx, (text, emb) in enumerate(zip(formatted_texts, embeddings)):
        # Limpiar caracteres raros del nombre de archivo para usarlo de base
        safe_name = re.sub(r'[^a-zA-Z0-9]', '', filename.lower())
        string_id = f"mkt_{safe_name}_idx{idx}"
        # Generar un UUID determinista válido para Qdrant basado en la cadena original
        vector_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, string_id))
        
        payload = {
            "vector_id": string_id,
            "region": region,
            "tier": 1, # Tier alto porque es investigacion validada
            "modulo_nombre": "MarketResearch",
            "text_content": text
        }
        
        points.append(PointStruct(id=vector_uuid, vector=emb, payload=payload))
        
    try:
        qclient.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"[+] ÉXITO: {len(points)} vectores inyectados para {region.upper()} en Qdrant!")
    except Exception as e:
        print(f"[-] Error guardando en Qdrant: {e}")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("===================================================================")
    print(" 🚀 INGESTA LOCAL: PDFs DE MERCADO A CEREBRO VECTORIAL ")
    print("===================================================================")
    
    qdrant_info = init_qdrant()
    pdf_dir = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\INV DE MERCADO"
    
    if not os.path.exists(pdf_dir):
        print(f"[-] La carpeta no existe: {pdf_dir}")
        return
        
    pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    peru_pdfs = [p for p in pdfs if is_peru_file(os.path.basename(p))]
    
    print(f"[*] Encontrados {len(pdfs)} PDFs. Filtrados para PERÚ: {len(peru_pdfs)}")
    
    # MODO PRODUCCIÓN: Procesar todos
    test_mode = False
    if test_mode:
        print("⚠️ MODO PRUEBA ACTIVADO: Solo procesaremos 1 documento (Loreto si existe, o el primero).")
        # Buscar Loreto
        test_pdf = next((p for p in peru_pdfs if "loreto" in p.lower()), None)
        if not test_pdf and peru_pdfs:
            test_pdf = peru_pdfs[0]
            
        if test_pdf:
            process_pdf(test_pdf, qdrant_info, test_mode=True)
    else:
        for pdf_path in peru_pdfs:
            process_pdf(pdf_path, qdrant_info)

if __name__ == "__main__":
    main()
