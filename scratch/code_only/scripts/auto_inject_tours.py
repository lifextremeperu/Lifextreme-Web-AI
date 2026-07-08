import os
import json
import re

def inject_into_data_js():
    data_js_path = os.path.join('js', 'data.js')
    if not os.path.exists(data_js_path):
        print(f"Error: No se encontró {data_js_path}")
        return

    # Leer todos los JSONs generados
    tours_to_inject = []
    # Buscar en la raíz donde se generaron
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    for file in os.listdir(project_root):
        if file.startswith('tours_') and file.endswith('.json'):
            file_path = os.path.join(project_root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'tours' in data:
                        tours_to_inject.extend(data['tours'])
            except Exception as e:
                print(f"Error leyendo {file}: {e}")
    
    if not tours_to_inject:
        print("No hay tours nuevos (archivos tours_*.json) para inyectar.")
        return
        
    print(f"Se encontraron {len(tours_to_inject)} tours para inyectar.")

    with open(data_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar el final del array de tours
    match = re.search(r'(\s+)\];\s*const events = \[', content)
    if not match:
        print("Error: No se pudo encontrar el punto de inyección en data.js (]; const events = [)")
        return
        
    injection_point = match.start(1)
    
    # Construir el string de los nuevos tours
    new_tours_str = ""
    for t in tours_to_inject:
        tour_str = json.dumps(t, indent=4, ensure_ascii=False)
        # Limpiar comillas en las claves para que se vea como JS nativo (opcional pero más limpio)
        tour_str = re.sub(r'"(\w+)":', r'\1:', tour_str)
        new_tours_str += ",\n" + tour_str
        
    # Inyectar
    new_content = content[:injection_point] + new_tours_str + content[injection_point:]
    
    with open(data_js_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"✅ Inyectados {len(tours_to_inject)} tours en js/data.js exitosamente.")

def main():
    print("="*60)
    print("INYECCIÓN AUTOMÁTICA DE TOURS (V10)")
    print("="*60)
    inject_into_data_js()
    print("✅ Proceso completado.")

if __name__ == "__main__":
    main()
