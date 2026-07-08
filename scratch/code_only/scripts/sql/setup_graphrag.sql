-- setup_graphrag.sql
-- Ejecutar en Supabase SQL Editor para crear la infraestructura de GraphRAG

-- 1. Habilitar pgvector si no está habilitado (debería estarlo por knowledge_vectors)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Tabla de Nodos (Entidades extraídas de los PDFs/FQSAs)
CREATE TABLE IF NOT EXISTS knowledge_nodes (
    node_id TEXT PRIMARY KEY,           -- Ej: "arequipa_ruta_sur", "sutran_alerta"
    node_name TEXT NOT NULL,            -- Ej: "Ruta Sur Arequipa"
    node_type TEXT NOT NULL,            -- Ej: "Lugar", "Proyecto", "Organizacion"
    description TEXT,                   -- Descripción breve del nodo
    embedding vector(768),              -- Asumiendo nomic-embed-text (768) o bge-m3 (1024). Ajustar si es necesario.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Tabla de Aristas (Relaciones entre Nodos)
CREATE TABLE IF NOT EXISTS knowledge_edges (
    edge_id SERIAL PRIMARY KEY,
    source_node_id TEXT REFERENCES knowledge_nodes(node_id) ON DELETE CASCADE,
    target_node_id TEXT REFERENCES knowledge_nodes(node_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,        -- Ej: "conecta_con", "depende_de", "financia"
    weight FLOAT DEFAULT 1.0,           -- Fuerza de la conexión
    metadata JSONB DEFAULT '{}'::jsonb, -- Información adicional de la relación
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    UNIQUE(source_node_id, target_node_id, relation_type)
);

-- 4. Crear índices para búsquedas vectoriales rápidas en Nodos
CREATE INDEX IF NOT EXISTS knowledge_nodes_embedding_idx 
ON knowledge_nodes 
USING hnsw (embedding vector_cosine_ops);

-- 5. Crear índices en las Aristas para travesías rápidas
CREATE INDEX IF NOT EXISTS knowledge_edges_source_idx ON knowledge_edges(source_node_id);
CREATE INDEX IF NOT EXISTS knowledge_edges_target_idx ON knowledge_edges(target_node_id);

-- 6. Función RPC para búsqueda GraphRAG básica (Encuentra Nodos Similares y sus vecinos)
CREATE OR REPLACE FUNCTION match_graph_nodes(
    query_embedding vector(768), 
    match_threshold float, 
    match_count int
)
RETURNS TABLE (
    node_id TEXT,
    node_name TEXT,
    description TEXT,
    similarity FLOAT
)
LANGUAGE sql STABLE
AS $$
    SELECT
        kn.node_id,
        kn.node_name,
        kn.description,
        1 - (kn.embedding <=> query_embedding) AS similarity
    FROM knowledge_nodes kn
    WHERE 1 - (kn.embedding <=> query_embedding) > match_threshold
    ORDER BY similarity DESC
    LIMIT match_count;
$$;
