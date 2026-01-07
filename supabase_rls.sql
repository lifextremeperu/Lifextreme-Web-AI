-- ============================================
-- LIFEXTREME SUPABASE ROW LEVEL SECURITY (RLS)
-- Políticas de Seguridad
-- ============================================

-- ============================================
-- 1. HABILITAR RLS EN TODAS LAS TABLAS
-- ============================================

ALTER TABLE users_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE tours ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE partners ENABLE ROW LEVEL SECURITY;
ALTER TABLE partner_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 2. POLÍTICAS PARA users_profiles
-- ============================================

-- Usuarios pueden ver su propio perfil
CREATE POLICY "Users can view own profile"
  ON users_profiles FOR SELECT
  USING (auth.uid() = id);

-- Usuarios pueden actualizar su propio perfil
CREATE POLICY "Users can update own profile"
  ON users_profiles FOR UPDATE
  USING (auth.uid() = id);

-- Usuarios pueden insertar su propio perfil
CREATE POLICY "Users can insert own profile"
  ON users_profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- ============================================
-- 3. POLÍTICAS PARA tours
-- ============================================

-- Todos pueden ver tours activos (público)
CREATE POLICY "Anyone can view active tours"
  ON tours FOR SELECT
  USING (active = true);

-- Solo partners aprobados pueden crear tours
CREATE POLICY "Approved partners can insert tours"
  ON tours FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM partners
      WHERE user_id = auth.uid() 
        AND status = 'approved'
    )
  );

-- Partners pueden actualizar sus propios tours
CREATE POLICY "Partners can update own tours"
  ON tours FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM partner_activities pa
      JOIN partners p ON pa.partner_id = p.id
      WHERE pa.tour_id = tours.id
        AND p.user_id = auth.uid()
    )
  );

-- ============================================
-- 4. POLÍTICAS PARA bookings
-- ============================================

-- Usuarios pueden ver sus propias reservas
CREATE POLICY "Users can view own bookings"
  ON bookings FOR SELECT
  USING (user_id = auth.uid());

-- Usuarios autenticados pueden crear reservas
CREATE POLICY "Authenticated users can create bookings"
  ON bookings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Usuarios pueden actualizar sus propias reservas (solo ciertos campos)
CREATE POLICY "Users can update own bookings"
  ON bookings FOR UPDATE
  USING (user_id = auth.uid());

-- Partners pueden ver reservas de sus tours
CREATE POLICY "Partners can view their tour bookings"
  ON bookings FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM partner_activities pa
      JOIN partners p ON pa.partner_id = p.id
      WHERE pa.tour_id = bookings.tour_id
        AND p.user_id = auth.uid()
        AND p.status = 'approved'
    )
  );

-- Partners pueden actualizar estado de reservas de sus tours
CREATE POLICY "Partners can update their tour bookings status"
  ON bookings FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM partner_activities pa
      JOIN partners p ON pa.partner_id = p.id
      WHERE pa.tour_id = bookings.tour_id
        AND p.user_id = auth.uid()
        AND p.status = 'approved'
    )
  );

-- ============================================
-- 5. POLÍTICAS PARA partners
-- ============================================

-- Usuarios pueden ver su propio perfil de partner
CREATE POLICY "Users can view own partner profile"
  ON partners FOR SELECT
  USING (user_id = auth.uid());

-- Todos pueden ver partners aprobados (público)
CREATE POLICY "Anyone can view approved partners"
  ON partners FOR SELECT
  USING (status = 'approved');

-- Usuarios autenticados pueden registrarse como partners
CREATE POLICY "Authenticated users can register as partners"
  ON partners FOR INSERT
  WITH CHECK (
    auth.uid() = user_id
    AND NOT EXISTS (
      SELECT 1 FROM partners WHERE user_id = auth.uid()
    )
  );

-- Partners pueden actualizar su propio perfil
CREATE POLICY "Partners can update own profile"
  ON partners FOR UPDATE
  USING (user_id = auth.uid());

-- ============================================
-- 6. POLÍTICAS PARA partner_activities
-- ============================================

-- Todos pueden ver actividades activas de partners aprobados
CREATE POLICY "Anyone can view active partner activities"
  ON partner_activities FOR SELECT
  USING (
    active = true
    AND EXISTS (
      SELECT 1 FROM partners p
      WHERE p.id = partner_activities.partner_id
        AND p.status = 'approved'
    )
  );

-- Partners pueden crear sus propias actividades
CREATE POLICY "Partners can create own activities"
  ON partner_activities FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM partners
      WHERE id = partner_activities.partner_id
        AND user_id = auth.uid()
        AND status = 'approved'
    )
  );

-- Partners pueden actualizar sus propias actividades
CREATE POLICY "Partners can update own activities"
  ON partner_activities FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM partners
      WHERE id = partner_activities.partner_id
        AND user_id = auth.uid()
    )
  );

-- Partners pueden eliminar sus propias actividades
CREATE POLICY "Partners can delete own activities"
  ON partner_activities FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM partners
      WHERE id = partner_activities.partner_id
        AND user_id = auth.uid()
    )
  );

-- ============================================
-- 7. POLÍTICAS PARA reviews
-- ============================================

-- Todos pueden ver reseñas verificadas (público)
CREATE POLICY "Anyone can view verified reviews"
  ON reviews FOR SELECT
  USING (verified = true);

-- Usuarios pueden ver sus propias reseñas
CREATE POLICY "Users can view own reviews"
  ON reviews FOR SELECT
  USING (user_id = auth.uid());

-- Usuarios pueden crear reseñas de sus propias reservas completadas
CREATE POLICY "Users can create reviews for completed bookings"
  ON reviews FOR INSERT
  WITH CHECK (
    auth.uid() = user_id
    AND EXISTS (
      SELECT 1 FROM bookings
      WHERE id = reviews.booking_id
        AND user_id = auth.uid()
        AND status = 'completed'
    )
    AND NOT EXISTS (
      SELECT 1 FROM reviews WHERE booking_id = reviews.booking_id
    )
  );

-- Usuarios pueden actualizar sus propias reseñas
CREATE POLICY "Users can update own reviews"
  ON reviews FOR UPDATE
  USING (user_id = auth.uid());

-- ============================================
-- 8. POLÍTICAS PARA ai_recommendations
-- ============================================

-- Usuarios pueden ver sus propias recomendaciones
CREATE POLICY "Users can view own recommendations"
  ON ai_recommendations FOR SELECT
  USING (user_id = auth.uid());

-- Sistema puede insertar recomendaciones (usando service_role)
-- No se permite INSERT desde el cliente

-- ============================================
-- 9. POLÍTICAS PARA analytics_events
-- ============================================

-- Usuarios pueden ver sus propios eventos
CREATE POLICY "Users can view own analytics events"
  ON analytics_events FOR SELECT
  USING (user_id = auth.uid());

-- Usuarios autenticados pueden crear eventos
CREATE POLICY "Authenticated users can create analytics events"
  ON analytics_events FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Usuarios anónimos pueden crear eventos (sin user_id)
CREATE POLICY "Anonymous users can create analytics events"
  ON analytics_events FOR INSERT
  WITH CHECK (user_id IS NULL);

-- ============================================
-- 10. POLÍTICAS PARA payments
-- ============================================

-- Usuarios pueden ver pagos de sus propias reservas
CREATE POLICY "Users can view own payments"
  ON payments FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM bookings
      WHERE id = payments.booking_id
        AND user_id = auth.uid()
    )
  );

-- Partners pueden ver pagos de reservas de sus tours
CREATE POLICY "Partners can view their tour payments"
  ON payments FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM bookings b
      JOIN partner_activities pa ON b.tour_id = pa.tour_id
      JOIN partners p ON pa.partner_id = p.id
      WHERE b.id = payments.booking_id
        AND p.user_id = auth.uid()
        AND p.status = 'approved'
    )
  );

-- Sistema puede crear pagos (usando service_role)
-- No se permite INSERT desde el cliente por seguridad

-- ============================================
-- POLÍTICAS DE SEGURIDAD CONFIGURADAS
-- ============================================

SELECT 'Row Level Security policies created successfully!' AS status;
