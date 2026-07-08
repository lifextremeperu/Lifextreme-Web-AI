"""
create_rpc_function.py
Crea la funcion RPC match_knowledge_vectors en Supabase via API REST.
Solo necesita ejecutarse UNA VEZ.
"""
import os, httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

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

def create_function():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    # Supabase expone /rest/v1/rpc/... pero para ejecutar SQL raw necesitamos
    # el endpoint de administracion o el SQL editor via pg connection
    # Usamos el endpoint de Supabase SQL via httpx
    resp = httpx.post(
        f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
        headers=headers,
        json={"sql": SQL},
        timeout=30
    )
    if resp.status_code == 200:
        print("EXITO: Funcion creada.")
    else:
        print(f"FALLO ({resp.status_code}): {resp.text}")
        print("\nNecesitas ejecutar el SQL manualmente en Supabase Dashboard > SQL Editor.")
        print("El archivo SQL esta en: sql/match_knowledge_vectors.sql")

if __name__ == "__main__":
    create_function()
