import re
import json

file_path = "Directorio_Nacional_Aventura.md"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

parks = []
current_region = None
current_category = None

# Images by category keyword
images = {
    "escalada indoor": "https://images.unsplash.com/photo-1522163182402-834f871fd851?q=80&w=600",
    "roca natural": "https://images.unsplash.com/photo-1563299796-17596c35a7ac?q=80&w=600",
    "zipline": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=600",
    "salto": "https://images.unsplash.com/photo-1533575936798-25110d9ab188?q=80&w=600",
    "rapel": "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=600",
    "parque": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=600",
    "atv": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?q=80&w=600",
    "paintball": "https://images.unsplash.com/photo-1627894483216-2138af692e32?q=80&w=600"
}

def get_image(cat):
    cat_lower = cat.lower()
    for key, url in images.items():
        if key in cat_lower:
            return url
    return "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?q=80&w=600"

park_id = 1

for line in lines:
    line = line.strip()
    
    # Detect region (## Region Name)
    match_region = re.match(r"^##\s+(.*)", line)
    if match_region:
        r_text = match_region.group(1).replace("Departamento de ", "").replace("Departamento del ", "")
        r_text = re.sub(r"\(.*?\)", "", r_text).strip()
        r_text = r_text.replace("🌿 ", "").replace("🌳 ", "").replace("🍃 ", "").replace("🌴 ", "").replace("🦜 ", "").strip()
        if r_text and "Macro-Región" not in r_text:
            current_region = r_text
        continue
        
    # Detect category (1. 🧗 Categoría or ### 1. 🧗 Categoría)
    match_cat = re.match(r"^(?:###\s+)?\d+\.\s*(?:[\w\u2600-\u27BF]+\s*)?(.*)", line)
    if match_cat and current_region:
        current_category = match_cat.group(1).strip()
        continue
        
    # Detect item (- **Name**: Desc or - Name)
    match_item = re.match(r"^[*-]\s+(.*)", line)
    if match_item and current_region and current_category:
        text = match_item.group(1)
        
        # Skip empty lines or "No existen", "Sin infraestructura"
        lower_text = text.lower()
        if "no existe" in lower_text or "sin infraestructura" in lower_text or "no se registra" in lower_text or "no hay" in lower_text or "ausencia de" in lower_text or "inexistente" in lower_text or "(sin " in lower_text or "no se cuenta" in lower_text:
            continue
            
        # Parse Name
        # If it has **, the name is inside **
        name_match = re.search(r"\*\*(.*?)\*\*", text)
        if name_match:
            name = name_match.group(1).strip()
            desc = text.replace(f"**{name}**", "").replace(":", "", 1).strip()
        else:
            # If no **, split by "-" or ":"
            parts = re.split(r"[-:]", text, 1)
            name = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else text
            
        # Clean up name
        name = re.sub(r"^\*+|\*+$", "", name).strip()
        
        # Determine specific type from category
        tipo_corto = "Aventura"
        if "indoor" in current_category.lower() or "palestra" in current_category.lower():
            tipo_corto = "Palestra"
        elif "roca" in current_category.lower() or "ferrata" in current_category.lower():
            tipo_corto = "Roca"
        elif "zipline" in current_category.lower() or "canopy" in current_category.lower():
            tipo_corto = "Zipline"
        elif "salto" in current_category.lower() or "bungee" in current_category.lower():
            tipo_corto = "Salto Extremo"
        elif "rapel" in current_category.lower():
            tipo_corto = "Rapel"
        elif "atv" in current_category.lower() or "logística" in current_category.lower():
            tipo_corto = "ATV / Buggy"
        elif "paintball" in current_category.lower():
            tipo_corto = "Paintball"
        elif "parque" in current_category.lower():
            tipo_corto = "Parque Aventura"
            
        parks.append({
            "id": f"INF-{current_region[:3].upper()}-{park_id:03d}",
            "nombre_infraestructura": name,
            "region": current_region,
            "tipo": tipo_corto,
            "url_foto": get_image(current_category),
            "nivel_dificultad": "Intermedio",
            "estado_actual": "Activo",
            "precio_estimado": 50.0,
            "descripcion": desc
        })
        park_id += 1

# Generate JS representation
js_content = "const parks = " + json.dumps(parks, indent=4, ensure_ascii=False) + ";\nwindow.parks = parks;\n"

# Inject into data.js, data-en.js, data-pt.js
files_to_update = ["js/data.js", "js/data-en.js", "js/data-pt.js"]

for fpath in files_to_update:
    try:
        with open(fpath, "r", encoding="utf-8") as js_file:
            content = js_file.read()
            
        # Regex to replace the parks array
        # It looks for "const parks = [ ... ]; window.parks = parks;"
        pattern = re.compile(r"const\s+parks\s*=\s*\[.*?\nwindow\.parks\s*=\s*parks;", re.DOTALL)
        
        if pattern.search(content):
            new_content = pattern.sub(js_content.strip(), content)
        else:
            # Fallback if the pattern doesn't exactly match
            new_content = content + "\n\n" + js_content
            
        with open(fpath, "w", encoding="utf-8") as js_file:
            js_file.write(new_content)
        print(f"Updated {fpath}")
    except Exception as e:
        print(f"Error reading/writing {fpath}: {e}")
