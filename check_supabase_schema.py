"""
check_supabase_schema.py
Inspecciona el esquema real de Supabase: tablas, columnas, funciones RPC.
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb = create_client(url, key)

print("\n=== INSPECCION SUPABASE ===\n")

# 1. Verificar columnas de knowledge_vectors
print("[1] Columnas de 'knowledge_vectors' (muestra 1 fila):")
try:
    res = sb.table("knowledge_vectors").select("*").limit(1).execute()
    if res.data:
        cols = list(res.data[0].keys())
        print(f"    Columnas: {cols}")
        for c in cols:
            val = res.data[0][c]
            tipo = type(val).__name__
            preview = str(val)[:80] if val else "NULL"
            print(f"    - {c} ({tipo}): {preview}")
    else:
        print("    Tabla vacia o sin acceso.")
except Exception as e:
    print(f"    ERROR: {e}")

# 2. Verificar columnas de knowledge_chunks
print("\n[2] Columnas de 'knowledge_chunks' (muestra 1 fila):")
try:
    res = sb.table("knowledge_chunks").select("*").limit(1).execute()
    if res.data:
        cols = list(res.data[0].keys())
        print(f"    Columnas: {cols}")
        for c in cols:
            val = res.data[0][c]
            tipo = type(val).__name__
            preview = str(val)[:80] if val else "NULL"
            print(f"    - {c} ({tipo}): {preview}")
    else:
        print("    Tabla vacia o sin acceso.")
except Exception as e:
    print(f"    ERROR: {e}")

# 3. Verificar si existe la funcion match_documents
print("\n[3] Verificando funcion RPC 'match_documents':")
try:
    # Embedding falso de 768 dims (nomic-embed-text produce 768)
    fake_embedding = [0.0] * 768
    res = sb.rpc("match_documents", {
        "query_embedding": fake_embedding,
        "match_count": 1
    }).execute()
    print(f"    EXISTE - Retorno: {res.data[:1] if res.data else 'vacio'}")
except Exception as e:
    err = str(e)
    if "does not exist" in err or "function" in err.lower():
        print(f"    NO EXISTE - Hay que crearla.")
    else:
        print(f"    ERROR inesperado: {err}")

# 4. Verificar si existen otras funciones RPC utiles
print("\n[4] Probando funcion alternativa 'match_knowledge_vectors':")
try:
    fake_embedding = [0.0] * 768
    res = sb.rpc("match_knowledge_vectors", {
        "query_embedding": fake_embedding,
        "match_count": 1
    }).execute()
    print(f"    EXISTE - Retorno: {res.data[:1] if res.data else 'vacio'}")
except Exception as e:
    err = str(e)
    if "does not exist" in err or "function" in err.lower():
        print(f"    NO EXISTE.")
    else:
        print(f"    ERROR: {err}")

# 5. Muestra de contenido real
print("\n[5] Muestra de 3 registros de 'knowledge_vectors' (sin embedding):")
try:
    cols_sin_emb = "id,content,region"
    # Intentar con columnas probables
    res = sb.table("knowledge_vectors").select(cols_sin_emb).limit(3).execute()
    if res.data:
        for row in res.data:
            print(f"    ID:{row.get('id')} | Region:{row.get('region')} | Content:{str(row.get('content',''))[:100]}")
    else:
        print("    Sin datos.")
except Exception as e:
    print(f"    ERROR con columnas 'id,content,region': {e}")
    # Intentar nombre alternativo de columna
    try:
        res = sb.table("knowledge_vectors").select("id,text,region").limit(3).execute()
        for row in res.data:
            print(f"    ID:{row.get('id')} | Region:{row.get('region')} | Text:{str(row.get('text',''))[:100]}")
    except Exception as e2:
        print(f"    ERROR con 'id,text,region': {e2}")

print("\n=== FIN INSPECCION ===\n")
