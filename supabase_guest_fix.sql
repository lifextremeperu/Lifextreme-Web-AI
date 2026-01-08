-- ============================================
-- FIX: PERMITIR RESERVAS DE INVITADOS (GUEST)
-- ============================================

-- 1. Eliminar la política anterior restrictiva (Solo usuarios logueados)
DROP POLICY IF EXISTS "Users can create bookings" ON bookings;

-- 2. Crear nueva política que permita INSERTS públicos (Guests + Usuarios)
-- Esto es seguro porque la tabla RLS 'bookings' protege los SELECTs (solo ver tus propias reservas)
-- pero permite que cualquiera CREÉ una reserva.
CREATE POLICY "Public can create bookings" 
  ON bookings FOR INSERT 
  WITH CHECK (true);

-- 3. (Opcional) Asegurar que el user_id pueda ser NULL en la tabla (ya lo es por defecto, pero confirmamos)
ALTER TABLE bookings ALTER COLUMN user_id DROP NOT NULL;

-- ============================================
-- VERIFICACIÓN
-- ============================================
-- Ejecuta este script en el SQL Editor de Supabase para habilitar las ventas a turistas no registrados.
