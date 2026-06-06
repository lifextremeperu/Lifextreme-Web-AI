-- ============================================
-- FUNCIÓN DE BÚSQUEDA SEMÁNTICA PARA DIVS-v1
-- ============================================
CREATE OR REPLACE FUNCTION match_knowledge_chunks (
  query_embedding vector(1024),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id text,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE sql STABLE
AS $$
  SELECT
    knowledge_chunks.id,
    knowledge_chunks.content,
    knowledge_chunks.metadata,
    1 - (knowledge_chunks.embedding <=> query_embedding) AS similarity
  FROM knowledge_chunks
  WHERE 1 - (knowledge_chunks.embedding <=> query_embedding) > match_threshold
  ORDER BY knowledge_chunks.embedding <=> query_embedding
  LIMIT match_count;
$$;
