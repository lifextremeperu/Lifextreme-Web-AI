import os
import httpx
import asyncio
import fitz  # PyMuPDF
import re

PDF_PATH = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\LIFEXTREME\MODULOS TURISMO\Asesoría Ministerial de Turismo Perú.pdf"
DOWNLOAD_DIR = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas"

def extract_urls_from_pdf(pdf_path):
    print(f"Extrayendo URLs de {pdf_path}...")
    urls = []
    url_pattern = re.compile(r'https?://[^\s]+')
    
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            found_urls = url_pattern.findall(text)
            for url in found_urls:
                # Clean up URL (sometimes trailing punctuation)
                clean_url = url.rstrip('.,;')
                if clean_url not in urls:
                    urls.append(clean_url)
    
    return urls

async def descargar_pdf(url, index, client: httpx.AsyncClient):
    # Intentar obtener el nombre original del archivo desde la URL
    nombre_archivo = url.split('/')[-1].split('?')[0]
    if not nombre_archivo.endswith('.pdf'):
        nombre_archivo = f"documento_{index}.pdf"
        
    ruta_guardado = os.path.join(DOWNLOAD_DIR, nombre_archivo)
    
    if os.path.exists(ruta_guardado):
        print(f"El archivo {nombre_archivo} ya existe. Saltando...")
        return

    print(f"[{index}] Descargando desde {url}...")
    
    try:
        response = await client.get(url, timeout=30.0)
        
        # Guardaremos si es PDF o si fuerza la descarga
        content_type = response.headers.get('Content-Type', '')
        if 'application/pdf' in content_type or url.endswith('.pdf') or response.status_code == 200:
            with open(ruta_guardado, 'wb') as f:
                f.write(response.content)
            print(f"Éxito: Guardado como {nombre_archivo}")
        else:
            print(f"Advertencia: {url} no parece ser un PDF directo ({content_type}).")
            
    except Exception as e:
        print(f"Error al descargar {url}: {e}")

async def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        
    urls = extract_urls_from_pdf(PDF_PATH)
    print(f"Se encontraron {len(urls)} URLs en el documento.")
    
    # Filter URLs that are likely to be documents (some are just domains like gob.pe, but we'll try to fetch all that look like pdfs or specific routes)
    # We will just try downloading all of them for now.
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Limitamos la concurrencia para no saturar
        sem = asyncio.Semaphore(5)
        
        async def sem_descargar(url, idx):
            async with sem:
                await descargar_pdf(url, idx, client)

        tareas = [sem_descargar(url, i+1) for i, url in enumerate(urls)]
        await asyncio.gather(*tareas)
        
    print("\nProceso de descarga automatizada finalizado.")

if __name__ == "__main__":
    asyncio.run(main())
