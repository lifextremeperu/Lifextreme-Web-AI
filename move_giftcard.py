import os

def move_giftcard(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar la seccion de giftcard
    start_marker = "<!-- GIFT EXPERIENCE SECTION -->"
    end_marker = "<!-- GUIAS -->"
    
    if start_marker not in content or end_marker not in content:
        print(f"Marcadores no encontrados en {filepath}")
        return
        
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    giftcard_content = content[start_idx:end_idx]
    
    # Eliminar la seccion giftcard de su posicion original
    content = content[:start_idx] + content[end_idx:]
    
    # Encontrar el final de section-guias
    # section-guias empieza en <!-- GUIAS --> y termina en <!-- SOCIO --> o similar
    # Vamos a buscar el cierre de div antes de </section> en section-guias
    guias_marker = '<section id="section-guias"'
    socio_marker = '<!-- SOCIO -->'
    
    guias_idx = content.find(guias_marker)
    socio_idx = content.find(socio_marker)
    
    if guias_idx == -1 or socio_idx == -1:
        print(f"No se encontro seccion de guias en {filepath}")
        return
        
    # El contenido de la seccion de guias va desde guias_idx hasta socio_idx
    guias_content = content[guias_idx:socio_idx]
    
    # Buscar el ultimo </section> dentro de guias_content
    last_section_end = guias_content.rfind('</section>')
    
    if last_section_end == -1:
        print("No se encontro </section> en guias")
        return
        
    # Insertar giftcard_content justo antes del </section>
    new_guias_content = guias_content[:last_section_end] + "\n" + giftcard_content + "\n" + guias_content[last_section_end:]
    
    # Reemplazar en el contenido original
    final_content = content[:guias_idx] + new_guias_content + content[socio_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print(f"Exito en {filepath}")

for f in ['index.html', 'en/index.html', 'pt/index.html']:
    move_giftcard(f)
