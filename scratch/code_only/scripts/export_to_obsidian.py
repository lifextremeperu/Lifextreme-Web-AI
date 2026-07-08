import os
import json
import re
from pathlib import Path
import shutil

# Rutas principales
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, 'data', 'knowledge', 'peru')
VAULT_DIR = os.path.join(BASE_DIR, 'data', 'obsidian_vault')

# Conceptos clave para "Deep Linking" (estilo cerebro experto)
KEY_CONCEPTS = [
    # Geografía y Topología
    "Andes", "Cordillera Blanca", "Amazonía", "Costa", "Montaña", "Glaciar", "Nevado", "Laguna", "Desierto", "Valle", "Cañón", "Quebrada", "Bosque", "Selva", "Río", "Cascada", "Volcán",
    
    # Logística y Preparación
    "Trekking", "Aclimatación", "Soroche", "Mal de altura", "Logística", "Presupuesto", "Equipo de montaña", "Camping", "Permisos", "Ticket", "Boleto turistico",
    "Temporada seca", "Temporada de lluvias", "Temporada alta", "Temporada baja", "Transporte", "Vuelo", "Bus", "Taxi", "Colectivo", "Guía certificado", "UIAGM", "AGMP", "SERNANP",
    
    # Turismo y Ventas (Para los Inversores)
    "Ventas", "Rentabilidad", "Inversión", "Experiencia VIP", "Turismo de aventura", "Turismo cultural", "Turismo sostenible", "Ecoturismo", "ROI", "Margen", "Escalabilidad", "Conversión", "Up-selling", "Cross-selling", "Ticket promedio", "Lujo", "Exclusivo", "All-inclusive",
    
    # Seguridad y Salud
    "Seguridad", "Emergencia", "Rescate", "Seguro de viaje", "Evacuación", "Clima", "Altitud", "Oxígeno", "Botiquín", "Peligro", "Avalancha", "Deslizamiento", "Radiación UV",
    
    # Cultura y Experiencia
    "Cultura", "Historia", "Inca", "Pre-inca", "Gastronomía", "Arqueología", "Ruinas", "Pachamama", "Comunidades locales", "Auténtico", "Folclore", "Tradición", "Artesanía",
    
    # Ciudades / Nodos principales (algunos ejemplos, pero la IA lo conectará si los ve)
    "Huaraz", "Cusco", "Lima", "Arequipa", "Puno", "Machu Picchu", "Iquitos", "Piura", "Trujillo", "Chiclayo", "Nazca", "Paracas", "Ica", "Tacna", "Madre de Dios", "Cajamarca", "Chachapoyas", "Tarapoto"
]

# Ordenamos por longitud descendente para que reemplace primero los más largos y evitar sub-matches (ej. "Turismo de aventura" antes que "Turismo")
KEY_CONCEPTS.sort(key=len, reverse=True)

def sanitize_filename(name, max_length=60):
    """Limpia el nombre para que sea un archivo válido en Windows/Linux y recorta longitud"""
    clean_name = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    if len(clean_name) > max_length:
        clean_name = clean_name[:max_length].strip()
    return clean_name or "Desconocido"

def add_deep_links(text):
    """Busca conceptos clave y los envuelve en [[Concepto]] para Obsidian"""
    linked_text = text
    # Usamos un set para evitar vincular la misma palabra múltiple veces en un mismo texto denso
    conceptos_vinculados = set()
    
    for concept in KEY_CONCEPTS:
        # Regex para coincidir con la palabra exacta (case-insensitive) y que no esté ya dentro de [[ ]]
        # (?<!\[\[) asegura que no haya "[[", \b asegura borde de palabra
        # Para que re.sub funcione sin reemplazar la versión original (case), usamos una función lambda
        pattern = re.compile(r'(?<!\[\[)\b(' + re.escape(concept) + r')\b(?!\]\])', re.IGNORECASE)
        
        # Encontramos si existe
        if pattern.search(linked_text) and concept.lower() not in conceptos_vinculados:
            # Reemplazamos manteniendo la capitalización original del texto, pero como el enlace de Obsidian distingue mayúsculas en archivos, forzamos un alias o el nombre estándar.
            # Ejemplo: [[Trekking|trekking]]
            # Pero para simplificar y que el grafo junte nodos con el mismo nombre exacto, usamos el nombre del concepto.
            linked_text = pattern.sub(rf'[[{concept}|\1]]', linked_text, count=3) # Limitamos a 3 veces por respuesta para no saturar
            conceptos_vinculados.add(concept.lower())
            
    return linked_text

def build_vault():
    print(f"🚀 Iniciando construcción de Bóveda Obsidian en: {VAULT_DIR}")
    
    # Limpiar bóveda anterior si existe
    if os.path.exists(VAULT_DIR):
        shutil.rmtree(VAULT_DIR)
    os.makedirs(VAULT_DIR)
    
    # Crear un índice general
    index_path = os.path.join(VAULT_DIR, "000_CEREBRO_MAX_IA.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# Cerebro MAX IA - Knowledge Graph de Turismo\n\n")
        f.write("Bienvenido a la red neuronal de turismo de aventura. Este grafo muestra cómo la IA de Lifextreme conecta logísticas, destinos, estrategias de ventas y seguridad en tiempo real.\n\n")
        f.write("## Departamentos Procesados\n")

    total_files_created = 0
    departamentos_procesados = 0
    
    # Recorrer todos los departamentos en data/knowledge/peru/
    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"Error: No se encontró la ruta {KNOWLEDGE_DIR}")
        return

    for depto in os.listdir(KNOWLEDGE_DIR):
        depto_path = os.path.join(KNOWLEDGE_DIR, depto)
        if not os.path.isdir(depto_path):
            continue
            
        fqsas_path = os.path.join(depto_path, "fqsas_deep")
        if not os.path.exists(fqsas_path):
            continue
            
        departamentos_procesados += 1
        depto_name = depto.capitalize()
        
        # Agregar al índice
        with open(index_path, 'a', encoding='utf-8') as f:
            f.write(f"- [[{depto_name}]]\n")
            
        # Crear carpeta del departamento en la bóveda
        vault_depto_dir = os.path.join(VAULT_DIR, "Departamentos", depto_name)
        os.makedirs(vault_depto_dir, exist_ok=True)
        
        # Crear archivo hub del departamento
        depto_hub = os.path.join(vault_depto_dir, f"{depto_name}.md")
        with open(depto_hub, 'w', encoding='utf-8') as f:
            f.write(f"# Departamento: {depto_name}\n\n")
            f.write("## Destinos y Rutas\n")

        # Leer JSONs
        for json_file in os.listdir(fqsas_path):
            if not json_file.endswith(".json"):
                continue
                
            json_path = os.path.join(fqsas_path, json_file)
            try:
                with open(json_path, 'r', encoding='utf-8') as jf:
                    data = json.load(jf)
                    
                destino_id = data.get("destino_id", "Desconocido")
                modulo_contexto = data.get("modulo_contexto", "Destino Sin Nombre")
                modulo_saneado = sanitize_filename(modulo_contexto)
                fqsas = data.get("fqsas", {})
                
                # Agregar destino al hub del departamento
                with open(depto_hub, 'a', encoding='utf-8') as f:
                    f.write(f"- [[{modulo_saneado}]]\n")
                
                # Crear carpeta para el destino
                vault_destino_dir = os.path.join(vault_depto_dir, modulo_saneado)
                os.makedirs(vault_destino_dir, exist_ok=True)
                
                # Archivo hub del destino
                destino_hub = os.path.join(vault_destino_dir, f"{modulo_saneado}.md")
                with open(destino_hub, 'w', encoding='utf-8') as f:
                    f.write(f"# Destino: {modulo_contexto}\n")
                    f.write(f"**Región:** [[{depto_name}]]\n")
                    f.write(f"**ID IA:** `{destino_id}`\n\n")
                    f.write("## Categorías de Inteligencia\n")
                
                # Crear archivos de conocimiento profundo por categoría
                for categoria, qa_list in fqsas.items():
                    # Sanear nombre de categoria (ej. 1_Precios_Presupuestos_Moneda -> Precios_Presupuestos_Moneda)
                    cat_name_clean = re.sub(r'^\d+_', '', categoria)
                    cat_name_saneado = sanitize_filename(cat_name_clean)
                    
                    # Agregar al hub del destino
                    with open(destino_hub, 'a', encoding='utf-8') as f:
                        f.write(f"- [[{modulo_saneado} - {cat_name_saneado}]]\n")
                    
                    # Archivo de categoría
                    cat_file = os.path.join(vault_destino_dir, f"{modulo_saneado} - {cat_name_saneado}.md")
                    with open(cat_file, 'w', encoding='utf-8') as f:
                        f.write(f"---\n")
                        f.write(f"type: knowledge_node\n")
                        f.write(f"region: {depto_name}\n")
                        f.write(f"destino: {modulo_contexto}\n")
                        f.write(f"categoria: {cat_name_saneado}\n")
                        f.write(f"---\n\n")
                        f.write(f"# Conocimiento: {cat_name_saneado}\n\n")
                        f.write(f"**Contexto:** [[{modulo_saneado}]] | **Macro-Región:** [[{depto_name}]]\n\n")
                        f.write(f"**Conector Cognitivo:** [[{cat_name_saneado}]]\n\n") # Crea un nodo maestro por categoría para unir todos los precios, toda la logistica, etc.
                        f.write("---\n\n")
                        
                        for qa in qa_list:
                            pregunta = add_deep_links(qa.get("pregunta", ""))
                            respuesta = add_deep_links(qa.get("respuesta", ""))
                            f.write(f"### Q: {pregunta}\n")
                            f.write(f"**A:** {respuesta}\n\n")
                            
                    total_files_created += 1

            except Exception as e:
                print(f"Error procesando {json_file}: {e}")
                
    print(f"\n✅ Bóveda generada exitosamente!")
    print(f"📊 Departamentos procesados: {departamentos_procesados}")
    print(f"📄 Nodos (archivos) de conocimiento creados: {total_files_created}")
    print(f"📂 Puedes abrir la carpeta en Obsidian: {VAULT_DIR}")

if __name__ == "__main__":
    build_vault()
