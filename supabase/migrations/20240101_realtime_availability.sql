-- Migration: Crear tabla de caché de disponibilidad (Scraping)
-- Uso: Centralizar el stock extraído de Cultura.pe y PeruRail

CREATE TABLE IF NOT EXISTS public.realtime_availability (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    destino VARCHAR(255) NOT NULL, -- ej: "machupicchu_llaqta", "camino_inca_4d", "tren_perurail_vistadome"
    fecha_recorrido DATE NOT NULL,
    cupos_disponibles INT NOT NULL DEFAULT 0,
    ultima_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Evitar duplicados de destino y fecha
    UNIQUE(destino, fecha_recorrido)
);

-- Índices para búsqueda ultrarrápida del chatbot
CREATE INDEX IF NOT EXISTS idx_avail_destino ON public.realtime_availability(destino);
CREATE INDEX IF NOT EXISTS idx_avail_fecha ON public.realtime_availability(fecha_recorrido);

-- Políticas de Seguridad (RLS)
ALTER TABLE public.realtime_availability ENABLE ROW LEVEL SECURITY;

-- Permitir lectura anónima (para que la API del Chatbot pueda leerlo sin trabas)
CREATE POLICY "Permitir lectura publica" 
ON public.realtime_availability FOR SELECT 
TO public
USING (true);

-- Solo los roles de servicio o scripts autenticados pueden insertar/actualizar
CREATE POLICY "Permitir modificacion a service_role" 
ON public.realtime_availability FOR ALL 
TO service_role
USING (true)
WITH CHECK (true);
