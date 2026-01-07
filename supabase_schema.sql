-- ============================================
-- LIFEXTREME SUPABASE DATABASE SCHEMA
-- Versión: 1.0
-- Fecha: 06 Enero 2026
-- ============================================

-- ============================================
-- 1. EXTENSIONES
-- ============================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 2. TABLAS PRINCIPALES
-- ============================================

-- Tabla: users_profiles
-- Información extendida de usuarios
CREATE TABLE IF NOT EXISTS users_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  age INTEGER,
  experience_level TEXT CHECK (experience_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
  interests TEXT[], -- Array de intereses: trekking, climbing, rafting, etc.
  budget_range TEXT CHECK (budget_range IN ('budget', 'mid', 'premium')),
  travel_frequency TEXT CHECK (travel_frequency IN ('monthly', 'quarterly', 'biannual', 'annual')),
  group_type TEXT CHECK (group_type IN ('solo', 'couple', 'friends', 'family')),
  preferred_regions TEXT[], -- Cusco, Huaraz, Arequipa, etc.
  motivation TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: tours
-- Catálogo de tours y experiencias
CREATE TABLE IF NOT EXISTS tours (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  long_description TEXT,
  region TEXT NOT NULL,
  difficulty TEXT CHECK (difficulty IN ('easy', 'moderate', 'challenging', 'extreme')) NOT NULL,
  duration_days INTEGER NOT NULL,
  price_pen DECIMAL(10,2) NOT NULL,
  max_group_size INTEGER DEFAULT 15,
  min_age INTEGER DEFAULT 18,
  category TEXT NOT NULL, -- trekking, climbing, rafting, biking, etc.
  images TEXT[], -- URLs de imágenes
  includes TEXT[],
  excludes TEXT[],
  itinerary JSONB, -- Itinerario detallado por días
  meeting_point TEXT,
  important_info TEXT,
  restrictions TEXT[],
  active BOOLEAN DEFAULT true,
  featured BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: bookings
-- Reservas de tours
CREATE TABLE IF NOT EXISTS bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_code TEXT UNIQUE NOT NULL DEFAULT 'LX-' || LPAD(FLOOR(RANDOM() * 999999)::TEXT, 6, '0'),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE RESTRICT,
  booking_date DATE NOT NULL,
  num_people INTEGER NOT NULL DEFAULT 1 CHECK (num_people > 0),
  total_price DECIMAL(10,2) NOT NULL,
  discount_percent DECIMAL(5,2) DEFAULT 0,
  final_price DECIMAL(10,2) NOT NULL,
  status TEXT CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')) DEFAULT 'pending',
  payment_status TEXT CHECK (payment_status IN ('pending', 'partial', 'paid', 'refunded')) DEFAULT 'pending',
  payment_method TEXT,
  special_requests TEXT,
  contact_name TEXT NOT NULL,
  contact_email TEXT NOT NULL,
  contact_phone TEXT NOT NULL,
  emergency_contact TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: partners
-- Operadores de aventura (Portal Partners)
CREATE TABLE IF NOT EXISTS partners (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  company_name TEXT NOT NULL,
  company_email TEXT UNIQUE NOT NULL,
  company_phone TEXT,
  description TEXT,
  logo_url TEXT,
  website TEXT,
  social_media JSONB, -- {facebook, instagram, twitter, youtube}
  address TEXT,
  city TEXT,
  region TEXT,
  certifications TEXT[],
  insurance_info TEXT,
  plan_type TEXT CHECK (plan_type IN ('starter', 'pro', 'elite')) DEFAULT 'starter',
  commission_rate DECIMAL(5,2) DEFAULT 22.00,
  status TEXT CHECK (status IN ('pending', 'approved', 'suspended', 'rejected')) DEFAULT 'pending',
  approved_at TIMESTAMPTZ,
  approved_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: partner_activities
-- Actividades ofrecidas por partners
CREATE TABLE IF NOT EXISTS partner_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  partner_id UUID REFERENCES partners(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE CASCADE,
  custom_price DECIMAL(10,2), -- Precio personalizado del partner
  availability_calendar JSONB, -- {date: available_slots}
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(partner_id, tour_id)
);

-- Tabla: reviews
-- Reseñas de tours
CREATE TABLE IF NOT EXISTS reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID UNIQUE REFERENCES bookings(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE CASCADE,
  rating INTEGER CHECK (rating >= 1 AND rating <= 5) NOT NULL,
  title TEXT,
  comment TEXT,
  images TEXT[],
  verified BOOLEAN DEFAULT false,
  helpful_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: ai_recommendations
-- Recomendaciones generadas por IA
CREATE TABLE IF NOT EXISTS ai_recommendations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE CASCADE,
  score DECIMAL(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
  reasoning TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, tour_id)
);

-- Tabla: analytics_events
-- Eventos de analytics (backup de GA4)
CREATE TABLE IF NOT EXISTS analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  session_id TEXT,
  event_name TEXT NOT NULL,
  event_category TEXT,
  event_label TEXT,
  event_value DECIMAL(10,2),
  metadata JSONB,
  user_agent TEXT,
  ip_address INET,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: payments
-- Registro de pagos
CREATE TABLE IF NOT EXISTS payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID REFERENCES bookings(id) ON DELETE CASCADE,
  amount DECIMAL(10,2) NOT NULL,
  currency TEXT DEFAULT 'PEN',
  payment_method TEXT NOT NULL,
  transaction_id TEXT UNIQUE,
  status TEXT CHECK (status IN ('pending', 'completed', 'failed', 'refunded')) DEFAULT 'pending',
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 3. ÍNDICES PARA PERFORMANCE
-- ============================================

CREATE INDEX IF NOT EXISTS idx_tours_region ON tours(region);
CREATE INDEX IF NOT EXISTS idx_tours_category ON tours(category);
CREATE INDEX IF NOT EXISTS idx_tours_active ON tours(active) WHERE active = true;
CREATE INDEX IF NOT EXISTS idx_tours_featured ON tours(featured) WHERE featured = true;

CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_bookings_tour_id ON bookings(tour_id);
CREATE INDEX IF NOT EXISTS idx_bookings_status ON bookings(status);
CREATE INDEX IF NOT EXISTS idx_bookings_date ON bookings(booking_date);

CREATE INDEX IF NOT EXISTS idx_partners_status ON partners(status);
CREATE INDEX IF NOT EXISTS idx_partners_user_id ON partners(user_id);

CREATE INDEX IF NOT EXISTS idx_reviews_tour_id ON reviews(tour_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

CREATE INDEX IF NOT EXISTS idx_analytics_event_name ON analytics_events(event_name);
CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON analytics_events(created_at);

-- ============================================
-- 4. FUNCIONES Y TRIGGERS
-- ============================================

-- Función: Actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas relevantes
CREATE TRIGGER update_users_profiles_updated_at
  BEFORE UPDATE ON users_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tours_updated_at
  BEFORE UPDATE ON tours
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at
  BEFORE UPDATE ON bookings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_partners_updated_at
  BEFORE UPDATE ON partners
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_partner_activities_updated_at
  BEFORE UPDATE ON partner_activities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at
  BEFORE UPDATE ON reviews
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función: Calcular precio final con descuento
CREATE OR REPLACE FUNCTION calculate_final_price()
RETURNS TRIGGER AS $$
BEGIN
  NEW.final_price = NEW.total_price * (1 - NEW.discount_percent / 100);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER calculate_booking_final_price
  BEFORE INSERT OR UPDATE ON bookings
  FOR EACH ROW EXECUTE FUNCTION calculate_final_price();

-- Función: Generar recomendaciones de IA para un usuario
CREATE OR REPLACE FUNCTION calculate_ai_recommendations(p_user_id UUID)
RETURNS TABLE (
  tour_id UUID,
  score DECIMAL,
  reasoning TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    t.id,
    (
      -- Score basado en región (30 puntos)
      CASE WHEN up.preferred_regions @> ARRAY[t.region] THEN 30 ELSE 0 END +
      -- Score basado en dificultad (25 puntos)
      CASE 
        WHEN up.experience_level = 'beginner' AND t.difficulty = 'easy' THEN 25
        WHEN up.experience_level = 'intermediate' AND t.difficulty IN ('easy', 'moderate') THEN 25
        WHEN up.experience_level = 'advanced' AND t.difficulty IN ('moderate', 'challenging') THEN 25
        WHEN up.experience_level = 'expert' AND t.difficulty = 'extreme' THEN 25
        ELSE 10
      END +
      -- Score basado en intereses (20 puntos)
      CASE WHEN up.interests && ARRAY[t.category] THEN 20 ELSE 0 END +
      -- Score basado en precio (15 puntos)
      CASE 
        WHEN up.budget_range = 'budget' AND t.price_pen < 500 THEN 15
        WHEN up.budget_range = 'mid' AND t.price_pen BETWEEN 500 AND 2000 THEN 15
        WHEN up.budget_range = 'premium' AND t.price_pen > 2000 THEN 15
        ELSE 5
      END +
      -- Score por tour destacado (10 puntos)
      CASE WHEN t.featured THEN 10 ELSE 0 END
    )::DECIMAL AS score,
    'Recomendado por IA basado en tu perfil de aventurero' AS reasoning
  FROM tours t
  CROSS JOIN users_profiles up
  WHERE up.id = p_user_id
    AND t.active = true
  ORDER BY score DESC
  LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 5. VISTAS ÚTILES
-- ============================================

-- Vista: Dashboard de Partners
CREATE OR REPLACE VIEW partner_dashboard AS
SELECT 
  p.id AS partner_id,
  p.company_name,
  p.plan_type,
  p.commission_rate,
  COUNT(DISTINCT b.id) AS total_bookings,
  COUNT(DISTINCT CASE WHEN b.status = 'confirmed' THEN b.id END) AS confirmed_bookings,
  COUNT(DISTINCT CASE WHEN b.status = 'completed' THEN b.id END) AS completed_bookings,
  SUM(CASE WHEN b.payment_status = 'paid' THEN b.final_price ELSE 0 END) AS total_revenue,
  SUM(CASE WHEN b.payment_status = 'paid' THEN b.final_price * p.commission_rate / 100 ELSE 0 END) AS total_commission,
  AVG(r.rating) AS average_rating,
  COUNT(DISTINCT r.id) AS total_reviews
FROM partners p
LEFT JOIN partner_activities pa ON p.id = pa.partner_id
LEFT JOIN bookings b ON pa.tour_id = b.tour_id
LEFT JOIN reviews r ON b.tour_id = r.tour_id
WHERE p.status = 'approved'
GROUP BY p.id, p.company_name, p.plan_type, p.commission_rate;

-- Vista: Tours populares
CREATE OR REPLACE VIEW popular_tours AS
SELECT 
  t.id,
  t.title,
  t.region,
  t.category,
  t.price_pen,
  COUNT(DISTINCT b.id) AS booking_count,
  AVG(r.rating) AS average_rating,
  COUNT(DISTINCT r.id) AS review_count
FROM tours t
LEFT JOIN bookings b ON t.id = b.tour_id
LEFT JOIN reviews r ON t.id = r.tour_id
WHERE t.active = true
GROUP BY t.id, t.title, t.region, t.category, t.price_pen
ORDER BY booking_count DESC, average_rating DESC;

-- ============================================
-- SCRIPT COMPLETADO
-- ============================================

-- Verificar que todo se creó correctamente
SELECT 'Database schema created successfully!' AS status;
