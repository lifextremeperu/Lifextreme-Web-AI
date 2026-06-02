-- ============================================
-- LIFEXTREME SUPABASE - FUNCIÓN DE BÚSQUEDA RAG
-- ============================================

-- Esta función es el "Buscador" de la IA. Toma la pregunta del usuario (convertida a números),
-- la compara matemáticamente con todas nuestras 35,000 preguntas, y nos devuelve las más similares.

CREATE OR REPLACE FUNCTION match_knowledge_vectors (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id uuid,
  vector_id text,
  region text,
  modulo_nombre text,
  text_content text,
  similarity float
)
LANGUAGE sql STABLE
AS $$
  SELECT
    knowledge_vectors.id,
    knowledge_vectors.vector_id,
    knowledge_vectors.region,
    knowledge_vectors.modulo_nombre,
    knowledge_vectors.text_content,
    1 - (knowledge_vectors.embedding <=> query_embedding) AS similarity
  FROM knowledge_vectors
  WHERE 1 - (knowledge_vectors.embedding <=> query_embedding) > match_threshold
  ORDER BY knowledge_vectors.embedding <=> query_embedding
  LIMIT match_count;
$$;
