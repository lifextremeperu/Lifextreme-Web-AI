-- ============================================
-- LIFEXTREME SUPABASE - DIRECTIVA DIVS-v1
-- Nueva tabla para acomodar BGE-M3 (1024 dimensiones) y la estructura Pydantic
-- ============================================

-- 1. Crear la nueva tabla de conocimiento (DIVS-v1)
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id TEXT PRIMARY KEY,                  -- Hash MD5 del chunk generado en Python
    content TEXT NOT NULL,                -- El texto en crudo extraído del PDF
    metadata JSONB NOT NULL,              -- Metadatos Pydantic (región, país, categoría, etc)
    embedding vector(1024) NOT NULL,      -- Vector de 1024 dimensiones (BAAI/bge-m3)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Crear índice para búsquedas semánticas (HNSW)
CREATE INDEX ON knowledge_chunks USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);

-- 3. Habilitar RLS
ALTER TABLE knowledge_chunks ENABLE ROW LEVEL SECURITY;

-- 4. Permitir lectura pública (para inferencia)
CREATE POLICY "Public read access for AI vectors (DIVS-v1)"
ON knowledge_chunks FOR SELECT
USING (true);

-- 5. Permitir inserción vía Service Key (Solo se inserta del backend, así que esto puede quedar bloqueado al público)

SELECT '✅ Tabla knowledge_chunks (DIVS-v1) creada correctamente para BGE-M3' as status;
