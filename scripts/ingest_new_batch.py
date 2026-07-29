import asyncio
import httpx
import os
from ingest_normativas import process_pdf

async def main():
    new_pdfs = [
        r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas\2092332-9.pdf",
        r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas\2125062-3.pdf",
        r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas\ley guia_turismo.pdf"
    ]
    
    sem = asyncio.Semaphore(5)
    async with httpx.AsyncClient() as http_client:
        for pdf_path in new_pdfs:
            print(f"\nIniciando ingesta única de: {os.path.basename(pdf_path)}")
            await process_pdf(pdf_path, http_client, sem)
            
    print("\n¡Ingesta de los 3 nuevos archivos finalizada con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
