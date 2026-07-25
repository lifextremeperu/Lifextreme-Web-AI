import sys
import os
import requests
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')


OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL_LLM = "llama3:8b"
ARTICLES_DIR = Path("data/blog/articles")

def inject_links(markdown_text):
    prompt = f"""Eres un editor técnico de Lifextreme.
Tu ÚNICA tarea es leer el siguiente documento Markdown y agregar enlaces (URLs) a cualquier mención de:
- Leyes, Decretos Supremos, o normativas legales (Ej: D.S. 005-2016-MINCETUR -> [D.S. 005-2016-MINCETUR](https://www.gob.pe/...))
- Instituciones oficiales del estado (MINCETUR, INDECOPI, etc.)

REGLAS ESTRICTAS:
1. NO modifiques NADA MÁS en el texto.
2. NO resumas el texto.
3. Devuelve EXACTAMENTE el mismo texto, respetando el Frontmatter YAML y los encabezados, pero con los enlaces insertados donde corresponda.
4. Si no hay leyes o instituciones, devuelve el texto tal cual.

TEXTO A EDITAR:
{markdown_text}
"""
    try:
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        return res.json().get('response', markdown_text)
    except Exception as e:
        print(f"[!] Error Ollama: {e}")
        return markdown_text

def main():
    print("==================================================")
    print(" 💉 AGENTE CIRUJANO: INYECCIÓN DE ENLACES LEGALES ")
    print("==================================================")
    
    if not ARTICLES_DIR.exists():
        print(f"La carpeta {ARTICLES_DIR} no existe.")
        return

    for archivo in ARTICLES_DIR.glob("*.md"):
        print(f"-> Operando en: {archivo.name}")
        with open(archivo, "r", encoding="utf-8") as f:
            contenido_original = f.read()

        contenido_modificado = inject_links(contenido_original)
        
        # Validación de seguridad: Asegurar que el YAML no se rompió
        if "---" in contenido_original and "---" not in contenido_modificado:
            print(f"  [!] Fallo de seguridad: YAML roto en {archivo.name}. Se descarta la operación.")
            continue
            
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_modificado.strip())
        print(f"  [✅] Inyección exitosa.")
        
    print("Operación Quirúrgica Completada.")

if __name__ == "__main__":
    main()
