import os
import glob
import json
import shutil
from datetime import datetime
import yaml  # Requiere pyyaml, si no está disponible, parsearemos manualmente

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_str = parts[1]
            body = parts[2].strip()
            # Simple parser if yaml is not installed
            metadata = {}
            for line in frontmatter_str.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip().strip('"').strip("'")
            return metadata, body
    return {}, content

def main():
    source_dir = "data/blog/drafts_geo"
    target_dir = "data/blog/articles"
    img_target_dir = "assets/img"
    index_file = "data/blog/index.json"
    
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(img_target_dir, exist_ok=True)
    
    # Load existing index
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            try:
                index_data = json.load(f)
            except:
                index_data = []
    else:
        index_data = []
        
    # Mapa de imagenes generadas a los slugs
    # Buscar las imagenes en la carpeta de artifacts
    brain_dir = r"C:\Users\ASUS\.gemini\antigravity\brain\6c43edf0-b121-4b3a-bfa0-75dc0e53b267"
    img_files = glob.glob(os.path.join(brain_dir, "*.png"))
    
    img_map = {
        "geo_01_parques": "geo_01_parques_peru",
        "geo_02_seguridad": "geo_02_seguridad_montana",
        "geo_03_telefonos": "geo_03_telefonos_emergencia",
        "geo_04_marketplace": "geo_04_marketplace_guias",
        "geo_05_ia_planners": "geo_05_ia_planners_rutas"
    }

    articles_md = glob.glob(os.path.join(source_dir, "*.md"))
    
    for md_file in articles_md:
        base_name = os.path.basename(md_file).replace(".md", "")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        meta, body = parse_frontmatter(content)
        slug = meta.get("slug", base_name)
        title = meta.get("title", base_name.replace("_", " ").title())
        
        # Encontrar la imagen
        img_prefix = img_map.get(base_name, "")
        img_path_for_web = ""
        alt_text = title
        
        for img in img_files:
            if img_prefix in os.path.basename(img):
                new_img_name = f"{slug}.png"
                shutil.copy(img, os.path.join(img_target_dir, new_img_name))
                img_path_for_web = f"assets/img/{new_img_name}"
                break
                
        # Inyectar imagen al inicio del body
        if img_path_for_web:
            body = f"![{alt_text}]({img_path_for_web})\n\n" + body
            
        # Escribir el articulo limpio para la web (sin YAML)
        with open(os.path.join(target_dir, f"{slug}.md"), 'w', encoding='utf-8') as f:
            f.write(body)
            
        # Actualizar índice
        entry = {
            "slug": slug,
            "title": title,
            "summary": meta.get("meta_description", "Guía de aventura de Lifextreme."),
            "date": meta.get("date", datetime.now().strftime("%Y-%m-%d")),
            "category": "Aventura Segura",
            "location": "Perú"
        }
        
        # Remover existente si hay
        index_data = [x for x in index_data if x.get("slug") != slug]
        index_data.append(entry)
        
        print(f"Deploying {slug}...")

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)
        
    print("Deploy finalizado.")

if __name__ == "__main__":
    main()
