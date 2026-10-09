import os
import asyncio
from playwright.async_api import async_playwright
import csv

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = r"D:\Playwright"

async def scrape_b2b_agencies():
    print("INICIANDO CACERIA B2B: Extrayendo Agencias de Turismo en Cusco...")
    
    agencias = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Búsqueda en DuckDuckGo (Menos bloqueos antibot que Google)
        search_url = "https://html.duckduckgo.com/html/?q=agencia+de+viajes+cusco+whatsapp+contacto"
        print(f"Conectando al motor de busqueda...")
        await page.goto(search_url)
        
        # Extraer resultados
        resultados = await page.query_selector_all('.result')
        
        print(f"Se encontraron {len(resultados)} prospectos potenciales en la primera pagina.")
        
        for result in resultados:
            try:
                title_elem = await result.query_selector('.result__title')
                snippet_elem = await result.query_selector('.result__snippet')
                
                title = await title_elem.inner_text() if title_elem else "Agencia Desconocida"
                snippet = await snippet_elem.inner_text() if snippet_elem else ""
                
                # Filtrar basura
                if "viaje" in title.lower() or "tour" in title.lower() or "cusco" in title.lower() or "peru" in title.lower():
                    agencias.append({
                        "Nombre": title.strip(),
                        "Informacion": snippet.strip()
                    })
            except Exception as e:
                continue
                
        await browser.close()
        
    # Guardar en CSV
    csv_path = os.path.abspath("B2B_Prospectos_Cusco.csv")
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Nombre", "Informacion"])
        writer.writeheader()
        writer.writerows(agencias)
        
    print(f"\nCACERIA EXITOSA!")
    print(f"Se han guardado {len(agencias)} agencias listas para contactar en: {csv_path}")
    
    if len(agencias) > 0:
        print("\nTOP 3 PROSPECTOS ENCONTRADOS:")
        for i in range(min(3, len(agencias))):
            print(f"- {agencias[i]['Nombre']}")

if __name__ == "__main__":
    try:
        asyncio.run(scrape_b2b_agencies())
    except Exception as e:
        print(f"Error en la extracción: {e}")
