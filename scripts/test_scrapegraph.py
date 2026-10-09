import os
import json
from scrapegraphai.graphs import SmartScraperGraph

# 1. Le decimos al script dónde guardamos el navegador fantasma (Disco D)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

# 2. Configuramos la IA para que use TUS modelos locales (GRATIS y PRIVADOS)
graph_config = {
    "llm": {
        "model": "ollama/phi3",
        "temperature": 0.0,
        "base_url": "http://localhost:11434",
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",
    },
    "verbose": True,
    "headless": True, # Navegador oculto en segundo plano
}

# 3. La página del gobierno que queremos investigar
url = "https://www.gob.pe/mincetur"

# 4. El "Prompt" mágico. En vez de código CSS, usamos lenguaje natural.
prompt = "Busca en la página web y extrae todos los enlaces, títulos y descripciones que estén relacionados con 'estudios de mercado', 'informes de turismo', 'cifras' o 'reportes'. Devuelve una lista de objetos JSON con los campos 'titulo', 'descripcion' y 'enlace'."

print(f"Iniciando el Agente Arana con Phi3 local...\nDestino: {url}")

try:
    # Creamos el grafo de scraping
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=url,
        config=graph_config
    )

    # Ejecutamos la IA
    result = smart_scraper_graph.run()

    print("\n" + "="*50)
    print("[EXITO] EXTRACCION COMPLETADA")
    print("="*50)
    print(json.dumps(result, indent=4, ensure_ascii=False))

except Exception as e:
    print(f"\n[ERROR] Ocurrio un error al intentar raspar la pagina: {e}")
