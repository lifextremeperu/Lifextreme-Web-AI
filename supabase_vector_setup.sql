-- ============================================
-- LIFEXTREME SUPABASE - CONFIGURACIÓN DE VECTORES (IA)
-- Este script habilita pgvector y crea la bóveda de conocimiento B2B/B2C
-- ============================================

-- 1. Habilitar la extensión de vectores
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Crear la tabla de conocimiento
CREATE TABLE IF NOT EXISTS knowledge_vectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vector_id TEXT UNIQUE NOT NULL,       -- ID único generado en el script Python
    region TEXT NOT NULL,                 -- Ejemplo: 'peru', 'arequipa'
    tier INTEGER DEFAULT 3,               -- Nivel comercial
    modulo_nombre TEXT NOT NULL,          -- Nombre del módulo/destino
    text_content TEXT NOT NULL,           -- El texto en crudo (Pregunta + Respuesta)
    embedding vector(768) NOT NULL,       -- Vector de 768 dimensiones (Google text-embedding-004)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Crear índice para búsquedas semánticas ultra-rápidas
-- Usamos HNSW (Hierarchical Navigable Small World) recomendado por Supabase
CREATE INDEX ON knowledge_vectors USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- 4. Habilitar Row Level Security (opcional, por seguridad)
ALTER TABLE knowledge_vectors ENABLE ROW LEVEL SECURITY;

-- Permitir lectura pública (para que el Agente IA pueda leer desde el backend/frontend sin auth)
CREATE POLICY "Public read access for AI vectors"
ON knowledge_vectors FOR SELECT
USING (true);

-- La inserción solo la haremos con la Service Role Key, así que no necesita policy pública de INSERT

SELECT '✅ Tabla knowledge_vectors y extensión pgvector configuradas correctamente' as status;
