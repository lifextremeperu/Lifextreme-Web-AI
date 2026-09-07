import asyncio
import httpx
from qdrant_client import AsyncQdrantClient

async def main():
    qdrant = AsyncQdrantClient(url="http://localhost:6333")
    
    with open('qdrant_results.txt', 'w', encoding='utf-8') as f:
        async def search(query):
            f.write(f"\n--- Buscando: {query} ---\n")
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": query}
                )
                vec = resp.json()["embedding"]
                
            res = await qdrant.query_points(
                collection_name="Lifextreme_Knowledge",
                query=vec,
                limit=10
            )
            for p in res.points:
                f.write(f"\nScore: {p.score}\n")
                f.write(p.payload.get("text_content", ""))
                f.write("\n" + "="*50 + "\n")

        await search("parque de aventura infraestructura")
        await search("palestra muro de escalada artificial")
        await search("puente tibetano canopy zipline circuito")
        await search("circuitos de escalada infraestructura turistica")

asyncio.run(main())
