import os
import sys
import pathlib
import asyncio
import httpx
import pdfplumber
from pathlib import Path

# Config
PERPLEXITY_DIR = r'C:\Users\ASUS\Downloads\PERPLEXITY'
QDRANT_URL = 'http://localhost:6333'
COLLECTION_NAME = 'Perplexity_Knowledge'
EMBED_MODEL = 'nomic-embed-text'

# Helper to ensure collection exists
async def ensure_collection():
    async with httpx.AsyncClient() as client:
        # Check if collection exists
        resp = await client.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
        if resp.status_code == 200:
            print(f'Colección {COLLECTION_NAME} ya existe')
            return
        # Create collection with 768 dims (same as nomic)
        payload = {
            "vectors": {"size": 768, "distance": "Cosine"},
            "hnsw_config": {"m": 16, "ef_construction": 100},
            "sharding_config": {"shard_count": 1}
        }
        r = await client.put(f"{QDRANT_URL}/collections/{COLLECTION_NAME}", json=payload)
        r.raise_for_status()
        print(f'Colección {COLLECTION_NAME} creada')

# Chunking by sections (simple: each page as a chunk)
async def process_pdf(pdf_path, client, point_id_start):
    points = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            if not text.strip():
                continue
            # Get embedding
            emb_resp = await client.post(
                f'http://localhost:11434/api/embeddings',
                json={'model': EMBED_MODEL, 'prompt': text[:2000]},
                timeout=30
            )
            emb_resp.raise_for_status()
            vector = emb_resp.json()['embedding']
            point = {
                "id": point_id_start + i,
                "vector": vector,
                "payload": {
                    "source": str(pdf_path),
                    "page": i,
                    "text": text
                }
            }
            points.append(point)
    return points

async def main():
    await ensure_collection()
    async with httpx.AsyncClient() as client:
        # Gather all PDF files
        pdf_files = [p for p in Path(PERPLEXITY_DIR).rglob('*.pdf')]
        print(f'Encontrados {len(pdf_files)} PDFs')
        point_id = 0
        batch = []
        for pdf_path in pdf_files:
            pts = await process_pdf(pdf_path, client, point_id)
            point_id += len(pts)
            batch.extend(pts)
            # Upload in batches of 64
            while len(batch) >= 64:
                to_send = batch[:64]
                batch = batch[64:]
                resp = await client.put(
                    f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points?wait=true",
                    json={"points": to_send}
                )
                resp.raise_for_status()
                print(f'Subidos {len(to_send)} puntos')
        # Upload remaining
        if batch:
            resp = await client.put(
                f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points?wait=true",
                json={"points": batch}
            )
            resp.raise_for_status()
            print(f'Subidos los últimos {len(batch)} puntos')
        print('Ingesta completada')

if __name__ == '__main__':
    asyncio.run(main())
