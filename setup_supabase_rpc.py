"""
setup_supabase_rpc.py
Crea la funcion RPC match_knowledge_vectors en Supabase usando httpx directo.
Ejecutar UNA SOLA VEZ para habilitar la busqueda vectorial.
"""
import os, httpx, json
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")  # https://xxx.supabase.co
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # anon o service_role key

# Extraer project ref de la URL
# URL formato: https://zobpkmiqrvhbepqnjshr.supabase.co
PROJECT_REF = SUPABASE_URL.replace("https://", "").replace(".supabase.co", "")

SQL = """
CREATE OR REPLACE FUNCTION match_knowledge_vectors(
  query_embedding vector(768),
  match_count int DEFAULT 5,
  filter_region text DEFAULT NULL,
  min_similarity float DEFAULT 0.3
)
RETURNS TABLE (
  id uuid,
  vector_id text,
  region text,
  tier int,
  modulo_nombre text,
  text_content text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    kv.id,
    kv.vector_id,
    kv.region,
    kv.tier,
    kv.modulo_nombre,
    kv.text_content,
    1 - (kv.embedding <=> query_embedding) AS similarity
  FROM knowledge_vectors kv
  WHERE
    (filter_region IS NULL OR kv.region ILIKE filter_region)
    AND (1 - (kv.embedding <=> query_embedding)) >= min_similarity
  ORDER BY kv.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
"""

print(f"\n=== CREANDO FUNCION RPC EN SUPABASE ===")
print(f"Proyecto: {PROJECT_REF}")
print(f"Funcion: match_knowledge_vectors\n")

# Intentar con Management API de Supabase
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Metodo 1: via pg endpoint de Supabase (si disponible)
try:
    resp = httpx.post(
        f"{SUPABASE_URL}/rest/v1/rpc/exec",
        headers=headers,
        json={"query": SQL},
        timeout=30
    )
    if resp.status_code < 400:
        print("EXITO via /rpc/exec")
    else:
        raise Exception(resp.text)
except Exception as e1:
    print(f"Metodo 1 fallo: {str(e1)[:100]}")
    
    # Metodo 2: via la API Management
    try:
        mgmt_headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        resp2 = httpx.post(
            f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query",
            headers=mgmt_headers,
            json={"query": SQL},
            timeout=30
        )
        if resp2.status_code < 400:
            print("EXITO via Management API")
        else:
            raise Exception(resp2.text)
    except Exception as e2:
        print(f"Metodo 2 fallo: {str(e2)[:100]}")
        print("\n" + "="*50)
        print("ACCION MANUAL REQUERIDA:")
        print("1. Ve a https://supabase.com/dashboard")
        print(f"2. Proyecto: {PROJECT_REF}")
        print("3. SQL Editor > New query")
        print("4. Pega el SQL de: sql/match_knowledge_vectors.sql")
        print("5. Click 'Run'")
        print("="*50)

# Verificar si la funcion existe ahora
print("\nVerificando existencia de la funcion...")
from supabase import create_client
sb = create_client(SUPABASE_URL, SUPABASE_KEY)
try:
    fake_emb = [0.0] * 768
    res = sb.rpc("match_knowledge_vectors", {
        "query_embedding": fake_emb,
        "match_count": 1,
        "min_similarity": 0.0
    }).execute()
    print(f"FUNCION ACTIVA: retorno {len(res.data)} filas con embedding cero.")
    if res.data:
        print(f"  Columnas: {list(res.data[0].keys())}")
except Exception as e:
    print(f"Funcion AUN NO EXISTE: {str(e)[:200]}")
    print("\nDebes ejecutar el SQL manualmente en el Dashboard de Supabase.")
