import asyncio
import httpx
import os
from ingest_normativas import process_pdf

async def main():
    pdf_path = r"C:\Users\ASUS\OneDrive\VARIOS\Documentos\GPTS IA\BIOVET AI\Lifextreme-Web-AI\data\normativas_descargadas\CODIGO PENAL ULTIMO.pdf"
    print(f"Iniciando ingesta única de: {pdf_path}")
    sem = asyncio.Semaphore(5)
    async with httpx.AsyncClient() as http_client:
        await process_pdf(pdf_path, http_client, sem)
    print("\n¡Ingesta del Código Penal finalizada con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
