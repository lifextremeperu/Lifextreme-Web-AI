-- ============================================
-- ACTUALIZACIÓN MULTI-TENANT PARA PARTNERS (V4)
-- ============================================

-- 1. Añadir partner_id a la tabla tours
ALTER TABLE tours 
ADD COLUMN IF NOT EXISTS partner_id UUID REFERENCES partners(id) ON DELETE CASCADE;

-- 2. Añadir partner_id a la tabla bookings
ALTER TABLE bookings 
ADD COLUMN IF NOT EXISTS partner_id UUID REFERENCES partners(id) ON DELETE CASCADE;

-- 3. Crear índice para mejorar consultas del Dashboard
CREATE INDEX IF NOT EXISTS idx_tours_partner_id ON tours(partner_id);
CREATE INDEX IF NOT EXISTS idx_bookings_partner_id ON bookings(partner_id);

-- 4. Actualizar Políticas RLS para Multi-Tenant B2B
-- Un partner solo puede ver sus propias reservas
DROP POLICY IF EXISTS "Partners can view own bookings" ON bookings;
CREATE POLICY "Partners can view own bookings" 
  ON bookings FOR SELECT 
  USING (
    partner_id IN (
      SELECT id FROM partners WHERE user_id = auth.uid()
    )
    OR user_id = auth.uid() -- O es el cliente que compró
  );

-- Un partner solo puede editar sus propios tours
DROP POLICY IF EXISTS "Partners can manage own tours" ON tours;
CREATE POLICY "Partners can manage own tours" 
  ON tours FOR ALL
  USING (
    partner_id IN (
      SELECT id FROM partners WHERE user_id = auth.uid()
    )
  );

-- Confirmación visual
SELECT 'Migración Multi-Tenant completada. Tours y Bookings ahora soportan IDs de operadores.' AS status;
