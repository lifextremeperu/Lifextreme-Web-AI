-- ============================================================
-- match_knowledge_vectors — Función RPC para RAG en MAX
-- Ejecutar en: Supabase Dashboard > SQL Editor
-- Tabla: knowledge_vectors | Embedding: nomic-embed-text (768 dims)
-- ============================================================

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

-- Verificar que funciona (embedding falso de 768 dims):
-- SELECT * FROM match_knowledge_vectors(array_fill(0::float, ARRAY[768])::vector, 3);
