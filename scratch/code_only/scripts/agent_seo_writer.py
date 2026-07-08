import os
import sys
import json
import time
import re
import requests
from pathlib import Path
from datetime import datetime

# Forzar codificación UTF-8 en Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

# Configuración
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:latest"
BASE_DIR = Path(__file__).parent.parent
BLOG_DIR = BASE_DIR / "data" / "blog" / "articles"
INDEX_FILE = BASE_DIR / "data" / "blog" / "index.json"
INFRA_FILE = BASE_DIR / "data" / "knowledge" / "infraestructura_seed.json"

# Crear directorios si no existen
BLOG_DIR.mkdir(parents=True, exist_ok=True)

def load_topics():
    topics = []
    # Cargar Infraestructura
    try:
        with open(INFRA_FILE, 'r', encoding='utf-8') as f:
            infra_data = json.load(f)
            for item in infra_data:
                topics.append({
                    "id": item.get("id_infraestructura"),
                    "title": item.get("nombre_oficial"),
                    "category": item.get("tipo_categoria"),
                    "location": item.get("ubicacion", {}).get("departamento", "Perú"),
                    "type": "infraestructura"
                })
    except Exception as e:
        print(f"Error cargando infraestructura: {e}")
        
    return topics

def load_blog_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_blog_index(index_data):
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=4)

def generate_article(topic):
    prompt = f"""
    Eres un experto redactor SEO y especialista en turismo de aventura extremo en Perú.
    Tu tarea es escribir un artículo de blog altamente optimizado para Google sobre el siguiente tema:
    
    Lugar/Infraestructura: {topic['title']}
    Categoría: {topic['category']}
    Ubicación: {topic['location']}
    
    El artículo debe estar formateado en Markdown válido y contener lo siguiente:
    1. Un Título principal (H1) muy atractivo (ej. "Todo lo que necesitas saber sobre...").
    2. Una breve introducción que enganche al lector.
    3. Al menos 3 secciones con subtítulos (H2).
    4. Consejos prácticos de seguridad y equipamiento.
    5. Un llamado a la acción (CTA) invitando a reservar en Lifextreme.
    
    No incluyas saludos ni comentarios adicionales, devuelve ÚNICAMENTE el código Markdown del artículo.
    """
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 1500
        }
    }
    
    print(f"\n[🤖] Solicitando artículo a {MODEL_NAME} para: {topic['title']}...")
    start_time = time.time()
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()
        content = response.json().get("response", "").strip()
        
        # Limpiar bloques de markdown si el modelo los añade
        if content.startswith("```markdown"):
            content = content[11:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        elapsed = time.time() - start_time
        print(f"[✓] Artículo generado en {elapsed:.1f} segundos.")
        return content.strip()
    except Exception as e:
        print(f"[x] Error conectando a Ollama: {e}")
        return None

def extract_title_and_summary(markdown_content):
    title = "Artículo sin título"
    summary = ""
    
    lines = markdown_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
            
    # Extraer el primer párrafo de texto normal como resumen
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('*') and not line.startswith('>'):
            summary = line.strip()[:150] + "..."
            break
            
    return title, summary

def main():
    print("===================================================================")
    print(" ✍️ AGENTE SEO MARKETING AUTÓNOMO (LIFEXTREME) ")
    print("===================================================================")
    
    topics = load_topics()
    blog_index = load_blog_index()
    existing_slugs = [item['slug'] for item in blog_index]
    
    print(f"-> Tópicos encontrados: {len(topics)}")
    print(f"-> Artículos ya existentes: {len(existing_slugs)}")
    
    articles_generated = 0
    max_articles_this_run = 10 # Limitar a 10 por corrida para no dejarlo infinito
    
    for topic in topics:
        if articles_generated >= max_articles_this_run:
            print("\n[!] Límite de artículos alcanzado por esta sesión.")
            break
            
        # Generar un slug simple
        slug = re.sub(r'[^a-z0-9]+', '-', topic['title'].lower()).strip('-')
        
        if slug in existing_slugs:
            print(f"[-] Saltando '{topic['title']}', el artículo ya existe.")
            continue
            
        content = generate_article(topic)
        
        if content:
            # Guardar archivo Markdown
            file_path = BLOG_DIR / f"{slug}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Extraer meta datos
            title, summary = extract_title_and_summary(content)
            
            # Actualizar índice
            new_entry = {
                "id": topic['id'],
                "slug": slug,
                "title": title,
                "summary": summary,
                "category": topic['category'],
                "location": topic['location'],
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            blog_index.append(new_entry)
            save_blog_index(blog_index)
            existing_slugs.append(slug)
            
            articles_generated += 1
            print(f"[✓] Artículo guardado: {slug}.md")
            
            # Pausa de enfriamiento
            if articles_generated < max_articles_this_run:
                cooldown = 15
                print(f"[⏱️] Pausa de enfriamiento de {cooldown} segundos para no sobrecargar el CPU/GPU...")
                time.sleep(cooldown)
                
    print("===================================================================")
    print(f" ✅ SESIÓN FINALIZADA. Artículos creados: {articles_generated}")
    print("===================================================================")

if __name__ == "__main__":
    main()
