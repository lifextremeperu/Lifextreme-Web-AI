"""
test_rag_live.py - Prueba el RAG real sin necesitar el servidor completo
"""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(__file__))

# Simular estructura de modulo backend
import importlib.util, pathlib

async def main():
    print("\n=== TEST RAG LIFEXTREME ===\n")
    
    # Test 1: Embedding con Ollama
    print("[1] Probando embedding con nomic-embed-text...")
    import httpx
    try:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.post("http://localhost:11434/api/embeddings",
                           json={"model": "nomic-embed-text", "prompt": "tour ausangate"})
            emb = r.json()["embedding"]
            print(f"    OK: embedding generado, dims={len(emb)}, sample={emb[:3]}")
    except Exception as e:
        print(f"    ERROR: {e}")
        print("    Asegurate de que Ollama este corriendo: ollama serve")
        return

    # Test 2: Busqueda RAG directa en Supabase
    print("\n[2] Probando busqueda RAG en Supabase (knowledge_vectors)...")
    from dotenv import load_dotenv
    load_dotenv()
    
    # Import rag_service
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rag_service",
        "backend/src/rag_service.py"
    )
    rag = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rag)
    
    query = "¿Qué tours tienen al Ausangate en Cusco?"
    print(f"    Query: '{query}'")
    
    try:
        context = await rag.get_rag_context(query, region="cusco")
        print(f"\n    RESULTADO RAG:")
        print("-" * 60)
        print(context[:1500])
        print("-" * 60)
        print(f"\n    OK: RAG funcionando correctamente.")
    except Exception as e:
        print(f"    ERROR: {e}")
    
    # Test 3: Verificar que el server.py se puede importar
    print("\n[3] Verificando estructura del backend...")
    try:
        files = [
            "backend/src/server.py",
            "backend/src/max_agent.py",
            "backend/src/rag_service.py",
            "backend/src/models.py"
        ]
        for f in files:
            exists = os.path.exists(f)
            print(f"    {'OK' if exists else 'FALTA'}: {f}")
    except Exception as e:
        print(f"    ERROR: {e}")

    print("\n=== FIN TEST ===\n")

asyncio.run(main())
