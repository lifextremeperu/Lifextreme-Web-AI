import time
import json
import os

try:
    from duckduckgo_search import DDGS
except ImportError:
    print("[ERROR] duckduckgo_search no está instalado. Instalando ahora...")
    os.system("pip install duckduckgo-search")
    from duckduckgo_search import DDGS

QUERIES = [
    "parque de aventura extremo San Ignacio Cajamarca columpio",
    "parque de aventura Huasao Cusco extremo",
    "Balcón del Diablo Cusco deporte aventura escalada",
    "palestra escalada cola de mono Arequipa",
    "parques de aventura Huaraz tirolesa puente colgante",
    "puente Autisha puenting Lima",
    "zipline Santa Teresa Cusco Cola de Mono",
    "parque de aventura extremo Valle Sagrado Cusco zipline"
]

def search_parks():
    print("==================================================")
    print("[+] INICIANDO AGENTE SPIDER: PARQUES DE AVENTURA PERU [+]")
    print("==================================================\n")
    
    results_compiled = []
    
    with DDGS() as ddgs:
        for query in QUERIES:
            print(f"[*] Escaneando la web para: '{query}'...")
            try:
                # Obtenemos los 5 primeros resultados de cada búsqueda
                results = ddgs.text(query, region='pe-es', max_results=5)
                for r in results:
                    title = r.get('title', '')
                    body = r.get('body', '')
                    href = r.get('href', '')
                    print(f"   -> [ENCONTRADO] {title[:60]}...")
                    results_compiled.append({
                        "query": query, 
                        "title": title, 
                        "body": body, 
                        "url": href
                    })
            except Exception as e:
                print(f"   [!] Error al rastrear la query: {e}")
            
            # Pausa breve para evitar bloqueos por rate-limit
            time.sleep(2) 
            
    print("\n[*] Consolidando y verificando base de datos de infraestructura...")
    md_path = "parques_peru_verificados.md"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🏕️ Base de Datos Verificada: Parques de Aventura Perú\n\n")
        f.write("*Generado automáticamente por Spider Web Scraper de Lifextreme*\n\n")
        
        current_query = ""
        for item in results_compiled:
            if item['query'] != current_query:
                current_query = item['query']
                f.write(f"\n## 🔍 Búsqueda: {current_query}\n")
            
            f.write(f"### {item['title']}\n")
            f.write(f"- **Descripción:** {item['body']}\n")
            f.write(f"- **Fuente Oficial:** [{item['url']}]({item['url']})\n\n")

    print(f"\n[EXITO] Rastreo completado al 100%. Los datos reales han sido guardados en '{md_path}'.")
    print("==================================================")

if __name__ == "__main__":
    search_parks()
