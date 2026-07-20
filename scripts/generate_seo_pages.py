import os
import sys
import json
import xml.etree.ElementTree as ET
import requests
from qdrant_client import QdrantClient
from bs4 import BeautifulSoup
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Configuracion
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "Lifextreme_Knowledge"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3:latest" # Usando phi3 por su velocidad y sintesis comercial
BASE_URL = "https://www.lifextreme.store"

def get_unique_regions():
    try:
        client = QdrantClient(QDRANT_URL)
        # Scroll para sacar payload y encontrar regiones unicas
        records, next_page = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1000,
            with_payload=True,
            with_vectors=False
        )
        
        regions = {}
        for record in records:
            region = record.payload.get("region", "peru").lower()
            text = record.payload.get("text_content", "")
            if region not in regions:
                regions[region] = []
            regions[region].append(text)
            
        print(f"[*] Encontradas {len(regions)} regiones en Qdrant: {list(regions.keys())}")
        return regions
    except Exception as e:
        print(f"[-] Error conectando a Qdrant: {e}")
        return {}

def generate_seo_content(region, facts):
    context = "\n".join(facts[:15]) # Usar hasta 15 facts para no desbordar el contexto
    prompt = f"""
Eres un redactor experto en turismo B2B (SEO Programático) para Lifextreme.
Basado en los siguientes datos extraídos de la base de datos (Vector Qdrant):
{context}

Escribe un artículo optimizado para SEO sobre turismo de aventura en {region.upper()}.
El artículo debe estar en formato HTML (solo los tags como <h2>, <h3>, <p>, <ul>).
No incluyas etiquetas <html>, <head> o <body>, solo el contenido.
Incluye palabras clave como 'Turismo de aventura', 'Trekking', 'Operadores turísticos', y resalta la información técnica proporcionada.
"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.4}
    }
    
    try:
        print(f"[*] Generando contenido con {OLLAMA_MODEL} para {region}...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"[-] Error generando contenido: {e}")
        return "<p>Error al generar el contenido descriptivo de este destino.</p>"

def generate_json_ld(region, url, description):
    # Genera el markup schema para SEO local
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": f"Turismo Extremo en {region.upper()}",
        "description": description[:150] + "...",
        "url": url,
        "touristType": ["Adventure Traveler", "B2B Operators"]
    }
    return json.dumps(json_ld, indent=2, ensure_ascii=False)

def build_html_page(region, content_html, template_path="blog-article.html"):
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Simple replace
    page_url = f"{BASE_URL}/destinos/{region}.html"
    title = f"Turismo de Aventura en {region.upper()} | Lifextreme Destinos"
    desc = f"Descubre la inteligencia turística y rutas extremas validadas de {region.upper()} para operadores y viajeros."
    
    # Parse template
    soup = BeautifulSoup(html, 'html.parser')
    
    # Update title
    if soup.title:
        soup.title.string = title
        
    # Update meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        meta_desc['content'] = desc
        
    # Inject JSON-LD
    json_ld_script = soup.new_tag("script", type="application/ld+json")
    json_ld_script.string = generate_json_ld(region, page_url, desc)
    if soup.head:
        soup.head.append(json_ld_script)
        
    # Replace content inside main
    main_tag = soup.find('main')
    if main_tag:
        # Limpiar contenido original
        main_tag.clear()
        
        # Injectar el nuevo h1 y el contenido generado
        header_html = f'<div class="container mx-auto px-4 py-20"><h1 class="text-4xl md:text-6xl font-black italic mb-10 text-slate-900">Destino: <span class="text-primary">{region.upper()}</span></h1>'
        footer_html = '</div>'
        
        content_soup = BeautifulSoup(header_html + content_html + footer_html, 'html.parser')
        main_tag.append(content_soup)
        
    return str(soup)

def update_sitemap(new_url):
    sitemap_path = 'sitemap.xml'
    
    if not os.path.exists(sitemap_path):
        print("[-] sitemap.xml no encontrado.")
        return
        
    try:
        # Registrar namespaces para evitar ns0:
        ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Check if URL already exists
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for loc in root.findall('.//sm:loc', ns):
            if loc.text == new_url:
                print(f"[*] La URL {new_url} ya existe en el sitemap.")
                return
                
        # Create new url element
        url_tag = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        loc_tag = ET.SubElement(url_tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        loc_tag.text = new_url
        
        lastmod_tag = ET.SubElement(url_tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
        lastmod_tag.text = datetime.now().strftime("%Y-%m-%d")
        
        changefreq_tag = ET.SubElement(url_tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}changefreq')
        changefreq_tag.text = 'weekly'
        
        priority_tag = ET.SubElement(url_tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
        priority_tag.text = '0.8'
        
        root.append(url_tag)
        tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
        print(f"[+] URL inyectada en sitemap.xml: {new_url}")
    except Exception as e:
        print(f"[-] Error actualizando sitemap: {e}")

def main():
    print("==================================================")
    print(" 🚀 MOTOR SEO PROGRAMÁTICO: QDRANT -> HTML ")
    print("==================================================")
    
    destinos_dir = "destinos"
    os.makedirs(destinos_dir, exist_ok=True)
    
    regions_data = get_unique_regions()
    
    if not regions_data:
        print("[-] No hay datos en Qdrant para procesar. Asegurate de correr la ingesta primero.")
        return
        
    for region, facts in regions_data.items():
        if not region:
            continue
            
        print(f"\n[>>>] Procesando región: {region.upper()} ({len(facts)} insights disponibles)")
        
        html_content = generate_seo_content(region, facts)
        final_page = build_html_page(region, html_content)
        
        filepath = os.path.join(destinos_dir, f"{region}.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_page)
        print(f"[+] Página generada: {filepath}")
        
        page_url = f"{BASE_URL}/destinos/{region}.html"
        update_sitemap(page_url)
        
    print("\n[✔] PROCESO COMPLETADO. Todas las páginas han sido autogeneradas y el sitemap está actualizado.")

if __name__ == "__main__":
    main()
