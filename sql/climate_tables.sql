-- sql/climate_tables.sql
-- Tabla para almacenar el caché de datos climáticos (NOAA, SENAMHI, IGP/ENFEN)
-- Esto permite que el frontend lea de Supabase y no bloquee ni sature las APIs públicas.

CREATE TABLE IF NOT EXISTS public.climate_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name VARCHAR(50) NOT NULL, -- Ej: 'NOAA', 'SENAMHI', 'ENFEN'
    metric_type VARCHAR(50) NOT NULL, -- Ej: 'SST_ANOMALY', 'PRECIPITATION', 'ICEN_ALERT'
    raw_value JSONB, -- Datos crudos extraídos de la API
    alert_level VARCHAR(50), -- Ej: 'NORMAL', 'ALERTA AMARILLA', 'EL NIÑO'
    location VARCHAR(100), -- Ej: 'Niño 3.4', 'Arequipa', 'Costa Norte'
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear un índice para buscar rápidamente por fuente
CREATE INDEX IF NOT EXISTS idx_climate_cache_source ON public.climate_cache(source_name);

-- Agregar políticas de seguridad (RLS) para que el frontend pueda leer
ALTER TABLE public.climate_cache ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Permitir lectura pública de climate_cache" 
ON public.climate_cache 
FOR SELECT 
USING (true);
