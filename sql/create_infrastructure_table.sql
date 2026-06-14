-- ==========================================
-- LIFEXTREME - INFRASTRUCTURE CATALOG SCHEMA
-- ==========================================

-- 1. Create the infrastructure table
CREATE TABLE IF NOT EXISTS infrastructure (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_infraestructura VARCHAR(50) UNIQUE NOT NULL,
    nombre_oficial VARCHAR(255) NOT NULL,
    tipo_categoria VARCHAR(100) NOT NULL,
    descripcion_corta TEXT,
    
    -- Ubicación JSONB para mayor flexibilidad
    ubicacion JSONB NOT NULL,
    
    website VARCHAR(255),
    operador_responsable VARCHAR(255),
    estado_actual VARCHAR(50) DEFAULT 'Activo',
    
    -- Array de certificaciones
    certificaciones_seguridad TEXT[] DEFAULT '{}',
    
    -- Tiempos de control
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create indices for faster filtering
CREATE INDEX IF NOT EXISTS idx_infra_categoria ON infrastructure(tipo_categoria);
CREATE INDEX IF NOT EXISTS idx_infra_estado ON infrastructure(estado_actual);
-- Create a GIN index on the JSONB location to search by department efficiently
CREATE INDEX IF NOT EXISTS idx_infra_ubicacion ON infrastructure USING GIN (ubicacion);

-- 3. Row Level Security (RLS)
ALTER TABLE infrastructure ENABLE ROW LEVEL SECURITY;

-- 4. Policies
-- Anyone can view active infrastructure (Public Access for the catalog)
CREATE POLICY "Public can view active infrastructure" 
    ON infrastructure 
    FOR SELECT 
    USING (estado_actual = 'Activo');

-- Only authenticated admins or service roles can insert/update (Handled by the Supabase Service Key)
