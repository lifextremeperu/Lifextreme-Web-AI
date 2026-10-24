-- ==============================================================================
-- LIFEXTREME SENTINEL VIP: GESTIÓN DE SUSCRIPTORES Y CONTROL DE ACCESO TELEGRAM
-- Ejecutar en el SQL Editor de Supabase (Dashboard -> SQL Editor -> New Query)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS public.sentinel_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_user TEXT,
    telegram_user_id BIGINT,
    email TEXT,
    stripe_customer_id TEXT,
    stripe_sub_id TEXT UNIQUE,
    invite_link TEXT,
    status TEXT NOT NULL DEFAULT 'active', -- 'active', 'canceled', 'payment_failed', 'trial'
    plan_name TEXT DEFAULT 'Sentinel VIP Machu Picchu 24/7',
    plan_price_pen NUMERIC DEFAULT 180.00,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices de alto rendimiento para búsqueda rápida en webhooks
CREATE INDEX IF NOT EXISTS idx_sentinel_stripe_sub ON public.sentinel_members (stripe_sub_id);
CREATE INDEX IF NOT EXISTS idx_sentinel_telegram_user ON public.sentinel_members (telegram_user);
CREATE INDEX IF NOT EXISTS idx_sentinel_status ON public.sentinel_members (status);

-- Trigger para actualización automática de updated_at
CREATE OR REPLACE FUNCTION public.handle_sentinel_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_sentinel_updated_at ON public.sentinel_members;
CREATE TRIGGER tr_sentinel_updated_at
    BEFORE UPDATE ON public.sentinel_members
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_sentinel_updated_at();

-- Habilitar Row Level Security (RLS)
ALTER TABLE public.sentinel_members ENABLE ROW LEVEL SECURITY;

-- Política de lectura para Service Role (API Backend)
CREATE POLICY "Service Role Full Access Sentinel"
    ON public.sentinel_members
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

COMMENT ON TABLE public.sentinel_members IS 'Registro de agencias y guías con membresía VIP activa al radar TuBoleto';
