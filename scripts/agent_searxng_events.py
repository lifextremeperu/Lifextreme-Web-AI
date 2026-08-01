import os
import re
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Forzar codificación en Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

# Importar funciones compartidas de flyer_hunter (ahorramos código)
try:
    import agent_flyer_hunter as hunter
except ImportError:
    print("Error: agent_flyer_hunter.py no encontrado en el mismo directorio. Se requiere para bajar imágenes.")
    sys.exit(1)

# CONFIGURACIÓN
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OLLAMA_BASE = "http://localhost:11434"
# SearXNG o OpenSERP
SEARXNG_URL = "http://localhost:8080/search" 
DATA_JS_PATH = Path(__file__).parent.parent / "js" / "data.js"
TEXT_MODEL = "mistral:latest" # o llama3

def search_events_searxng(query):
    """Busca eventos usando SearXNG en local (sin límites de API)."""
    params = {
        "q": query,
        "format": "json",
        "language": "es"
    }
    try:
        res = requests.get(SEARXNG_URL, params=params, timeout=15)
        if res.status_code == 200:
            return res.json().get("results", [])
    except Exception as e:
        print(f"Error conectando a SearXNG: {e}")
    return []

def extract_events_with_ollama(text_content):
    """Usa Ollama para extraer eventos estructurados de los resultados de búsqueda."""
    prompt = f"""
Eres un asistente que extrae información de eventos deportivos outdoor (Trail running, MTB, ciclismo, trekking) en Perú.
Revisa el siguiente texto y extrae TODOS los eventos que encuentres en formato JSON estricto.
El JSON debe ser una lista de objetos, cada uno con las siguientes claves:
"name" (nombre del evento, string),
"date" (fecha, string),
"location" (lugar o departamento en Perú, string),
"category" (ej: "Trail Running", "MTB", string).

Texto a analizar:
{text_content}

Responde ÚNICAMENTE con el array JSON válido, sin texto adicional.
"""
    payload = {
        "model": TEXT_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    try:
        res = requests.post(f"{OLLAMA_BASE}/api/generate", json=payload, timeout=60)
        if res.status_code == 200:
            content = res.json().get("response", "").strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "")
            return json.loads(content)
    except Exception as e:
        print(f"Error procesando con Ollama: {e}")
    return []

def is_duplicate(event_name, data_js_content):
    """Verifica si el evento ya existe en data.js"""
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', event_name).lower()
    clean_content = re.sub(r'[^a-zA-Z0-9]', '', data_js_content).lower()
    return clean_name in clean_content

def generate_new_id(data_js_content):
    """Busca el ID más alto de eventos y suma 1"""
    ids = re.findall(r'id:\s*(2\d{2,3})', data_js_content)
    if not ids:
        return 300
    return max([int(i) for i in ids]) + 1

def append_event_to_data_js(event_data, image_url):
    """Inserta el nuevo evento en data.js"""
    try:
        content = DATA_JS_PATH.read_text(encoding="utf-8")
        event_id = generate_new_id(content)
        
        new_event_js = f"""
    {{
        id: {event_id},
        dept: '{event_data.get("location", "Perú")}',
        name: '{event_data.get("name")}',
        price: 0,
        img: '{image_url}',
        desc: 'Categoría: {event_data.get("category")}. Evento programado para {event_data.get("date")}.',
        specialty: '{event_data.get("category")}',
        inc: ['Ruta señalizada', 'Hidratación', 'Dorsal'],
        whatYouDo: ['Participar en {event_data.get("name")}'],
        meetingPoint: '{event_data.get("location")}'
    }},"""
        
        if "const tours = [" in content:
            new_content = content.replace("const tours = [", "const tours = [" + new_event_js)
            DATA_JS_PATH.write_text(new_content, encoding="utf-8")
            return event_id
        return None
    except Exception as e:
        print(f"Error escribiendo en data.js: {e}")
        return None

def main():
    print("=== INICIANDO BÚSQUEDA SEMANAL DE EVENTOS ===")
    
    query = "calendario carreras trail running MTB Perú 2026 inscripciones"
    print(f"1. Buscando en SearXNG: '{query}'")
    search_results = search_events_searxng(query)
    
    if not search_results:
        print("No se encontraron resultados en SearXNG.")
        return
        
    compiled_text = ""
    for r in search_results[:10]:
        compiled_text += f"- Titulo: {r.get('title')}\n  Detalle: {r.get('content')}\n\n"
        
    print("2. Procesando texto con Ollama para extraer JSON...")
    extracted_events = extract_events_with_ollama(compiled_text)
    
    if not extracted_events:
        print("Ollama no encontró eventos válidos.")
        return
        
    print(f"Ollama detectó {len(extracted_events)} posibles eventos.")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    vision_model = hunter.check_vision_available()
    data_js_content = DATA_JS_PATH.read_text(encoding="utf-8")
    
    for ev in extracted_events:
        name = ev.get("name")
        print(f"\nProcesando evento: {name}")
        
        if is_duplicate(name, data_js_content):
            print("  -> Ya existe en data.js, omitiendo para evitar duplicados.")
            continue
            
        print("  -> Evento nuevo. Buscando flyer...")
        candidates = hunter.agent_search(name, ev.get("location", "Peru"), ev.get("date", "2026"))
        
        best_url = "https://images.unsplash.com/photo-1541252879014-416684724db3?auto=format&fit=crop&q=80&w=800"
        best_image_bytes = None
        
        for cand in candidates:
            img_b = hunter.download_image(cand["url"])
            if img_b:
                if vision_model:
                    valid, _ = hunter.validate_with_ollama(img_b, name, vision_model)
                else:
                    valid, _ = hunter.heuristic_validate(img_b, cand["url"])
                
                if valid:
                    best_image_bytes = img_b
                    break
        
        if best_image_bytes:
            temp_id = int(time.time() % 100000)
            uploaded_url = hunter.process_and_upload(best_image_bytes, temp_id, name, supabase)
            if uploaded_url:
                best_url = uploaded_url
                
        new_id = append_event_to_data_js(ev, best_url)
        if new_id:
            print(f"  [ÉXITO] Evento '{name}' agregado!")
            data_js_content = DATA_JS_PATH.read_text(encoding="utf-8")

if __name__ == "__main__":
    main()
