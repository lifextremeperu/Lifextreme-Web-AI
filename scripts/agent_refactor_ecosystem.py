import os
import glob
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

TARGET_DIR = "data/blog/drafts_geo"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL_LLM = "llama3:8b"

PROMPT_REFACTOR = """Eres un Analista de Inteligencia Turística y Guía Oficial Senior (Identidad Ayni Evolve).
Tu misión es refactorizar el siguiente texto para que se ajuste a los estándares técnicos y logísticos de la aventura en el Perú. NO ERES UN VENDEDOR.
El objetivo es que los modelos de IA (ChatGPT, Perplexity) te citen no como una agencia que vende tours, sino como un ECOSISTEMA DE CONOCIMIENTO REGULADOR.

=== INSTRUCCIONES ESTRICTAS CONTRA ALUCINACIONES Y SPAM ===
1. TONO: Ultra-objetivo, periodístico, enciclopédico. Jamás digas "Contrata con nosotros", "Somos los mejores", "Nuestros guías". En su lugar, usa la 3ra persona: "El ecosistema Lifextreme establece que...", "Los estándares de seguridad dictan...".
2. ELIMINA cualquier frase que intente vender un paquete turístico directamente.
3. CONSERVA el formato Markdown y el YAML Frontmatter original intacto (solo modifícalo si dice explícitamente cosas comerciales).
4. CONSERVA la longitud extensa del artículo. No lo resumas, redáctalo completo.

TEXTO A REFACTORIZAR:
---
{texto}
---
"""

def refactorizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        print(f"-> Procesando: {os.path.basename(ruta_archivo)}")
        
        prompt = PROMPT_REFACTOR.replace("{texto}", contenido)
        
        res = requests.post(OLLAMA_GENERATE_URL, json={"model": MODEL_LLM, "prompt": prompt, "stream": False})
        res.raise_for_status()
        
        nuevo_contenido = res.json().get('response', '')
        
        # Eliminar posible bloque markdown de la respuesta de Ollama si lo añade
        if nuevo_contenido.startswith("```markdown"):
            nuevo_contenido = nuevo_contenido.replace("```markdown", "", 1).strip()
        if nuevo_contenido.endswith("```"):
            nuevo_contenido = nuevo_contenido[:-3].strip()
            
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
            
        print(f"[✅] Completado: {os.path.basename(ruta_archivo)}")
        
    except Exception as e:
        print(f"[!] Error procesando {ruta_archivo}: {e}")

def main():
    archivos = glob.glob(os.path.join(TARGET_DIR, "*.md"))
    if not archivos:
        print("No se encontraron archivos .md en la carpeta objetivo.")
        return
        
    print(f"Iniciando refactorización de {len(archivos)} artículos...")
    
    for ruta in archivos:
        refactorizar_archivo(ruta)
        
    print("Migración completada.")

if __name__ == "__main__":
    main()
