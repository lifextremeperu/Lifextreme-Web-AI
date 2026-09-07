import time
import os

try:
    from duckduckgo_search import DDGS
except ImportError:
    os.system("pip install duckduckgo-search")
    from duckduckgo_search import DDGS

DEPARTAMENTOS = [
    "Amazonas", "Ancash", "Apurimac", "Arequipa", "Ayacucho", "Cajamarca",
    "Cusco", "Ica", "Junin", "Lima", "Madre de Dios", "Pasco", "Puno", "San Martin"
]

TERMS = [
    "parque de aventura", 
    "zipline tirolesa", 
    "puente colgante tibetano", 
    "columpio extremo puenting"
]

def spider_nacional():
    print("=========================================================")
    print("[+] INICIANDO SPIDER V2: MAPEO NACIONAL DE AVENTURA PERU [+]")
    print("=========================================================\n")
    
    results_compiled = []
    
    with DDGS() as ddgs:
        for depto in DEPARTAMENTOS:
            for term in TERMS:
                query = f"{depto} peru {term} -wikipedia -noticias -facebook -youtube"
                print(f"[*] Rastreador en {depto.upper()} -> Buscando: {term}")
                try:
                    results = ddgs.text(query, region='pe-es', max_results=3)
                    for r in results:
                        title = r.get('title', '')
                        body = r.get('body', '')
                        href = r.get('href', '')
                        print(f"   -> [HALLAZGO] {title[:60]}...")
                        results_compiled.append({
                            "depto": depto,
                            "term": term,
                            "title": title, 
                            "body": body, 
                            "url": href
                        })
                except Exception as e:
                    print(f"   [!] Error de conexion: {e}")
                time.sleep(1.5) 
                
    print("\n[*] Generando base de datos maestra nacional...")
    md_path = "mapa_nacional_aventura_peru.md"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🗺️ MAPA NACIONAL: Infraestructura de Aventura Perú\n\n")
        
        current_depto = ""
        for item in results_compiled:
            if item['depto'] != current_depto:
                current_depto = item['depto']
                f.write(f"\n## 📍 DEPARTAMENTO: {current_depto.upper()}\n")
            
            f.write(f"### {item['title']}\n")
            f.write(f"- **Tipo:** {item['term']}\n")
            f.write(f"- **Detalle:** {item['body']}\n")
            f.write(f"- **Link:** [{item['url']}]({item['url']})\n\n")

    print(f"\n[EXITO] Mapeo nacional finalizado. Archivo: {md_path}")
    print("=========================================================")

if __name__ == "__main__":
    spider_nacional()
