"""
check_qdrant_brain.py - Auditoría del Conocimiento Vectorial
Consulta Qdrant para resumir qué entidades y dominios están realmente en la base de datos.
"""
import asyncio
from qdrant_client import AsyncQdrantClient

QDRANT_URL = "http://localhost:6333"
KNOWLEDGE_VAULT = "Lifextreme_Knowledge"

async def check():
    client = AsyncQdrantClient(url=QDRANT_URL)
    try:
        info = await client.get_collection(KNOWLEDGE_VAULT)
        print(f"====== REPORTE DE CEREBRO QDRANT ======")
        print(f"Colección: {KNOWLEDGE_VAULT}")
        print(f"Total Chunks: {info.points_count}")
        print(f"=======================================\n")
        
        # We need to scroll through to get unique entities and sources
        entidades = {}
        fuentes = set()
        dominios = set()
        
        offset = None
        while True:
            result = await client.scroll(
                collection_name=KNOWLEDGE_VAULT,
                limit=1000,
                with_payload=True,
                with_vectors=False,
                offset=offset
            )
            records, next_page_offset = result
            for record in records:
                p = record.payload or {}
                if "source" in p:
                    fuentes.add(p["source"])
                if "entidad" in p:
                    ent = p["entidad"]
                    entidades[ent] = entidades.get(ent, 0) + 1
                if "dominio" in p:
                    dominios.add(p["dominio"])
                    
            if next_page_offset is None:
                break
            offset = next_page_offset
            
        print("📁 ENTIDADES INDEXADAS (Chunks):")
        for k, v in sorted(entidades.items()):
            if k:
                print(f" - {k}: {v} fragmentos")
        
        print("\n🔍 DOMINIOS ABARCADOS:")
        for d in sorted(dominios):
            if d:
                print(f" - {d}")
                
        print("\n📄 ARCHIVOS NORMATIVOS (Muestra de 15 fuentes PYME o con Entidad):")
        # Mostrar solo fuentes que tengan entidad inyectada o que estén en nuestro manifiesto
        # para no listar los 6000 archivos de turismo.
        # Ya que `fuentes` tiene miles, listaremos algunas.
        pyme_sources = [s for s in fuentes if "pdf" in s.lower() or "md" in s.lower()]
        for s in sorted(list(pyme_sources))[:15]:
            print(f" - {s}")

    except Exception as e:
        print(f"Error consultando Qdrant: {e}")

if __name__ == "__main__":
    asyncio.run(check())
