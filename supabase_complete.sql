-- ============================================
-- LIFEXTREME SUPABASE - CONFIGURACIÓN COMPLETA
-- Script único para crear toda la base de datos
-- Versión: 2.0 - Simplificada y Funcional
-- ============================================

-- ============================================
-- 1. EXTENSIONES
-- ============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- 2. TABLAS PRINCIPALES
-- ============================================

-- Tabla: users_profiles
CREATE TABLE users_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  age INTEGER,
  experience_level TEXT,
  interests TEXT[],
  budget_range TEXT,
  travel_frequency TEXT,
  group_type TEXT,
  preferred_regions TEXT[],
  motivation TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: tours
CREATE TABLE tours (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  region TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  duration_days INTEGER NOT NULL,
  price_pen DECIMAL(10,2) NOT NULL,
  category TEXT NOT NULL,
  images TEXT[],
  active BOOLEAN DEFAULT true,
  featured BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: bookings
CREATE TABLE bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE RESTRICT,
  booking_date DATE NOT NULL,
  num_people INTEGER NOT NULL DEFAULT 1,
  total_price DECIMAL(10,2) NOT NULL,
  status TEXT DEFAULT 'pending',
  contact_name TEXT NOT NULL,
  contact_email TEXT NOT NULL,
  contact_phone TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: partners
CREATE TABLE partners (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  company_name TEXT NOT NULL,
  company_email TEXT UNIQUE NOT NULL,
  company_phone TEXT,
  description TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: reviews
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  tour_id UUID REFERENCES tours(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL,
  comment TEXT,
  verified BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 3. ÍNDICES
-- ============================================
CREATE INDEX idx_tours_region ON tours(region);
CREATE INDEX idx_tours_active ON tours(active);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_tour_id ON bookings(tour_id);

-- ============================================
-- 4. ROW LEVEL SECURITY (RLS)
-- ============================================

-- Habilitar RLS
ALTER TABLE users_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE tours ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE partners ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Políticas para users_profiles
CREATE POLICY "Users can view own profile" 
  ON users_profiles FOR SELECT 
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
  ON users_profiles FOR UPDATE 
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" 
  ON users_profiles FOR INSERT 
  WITH CHECK (auth.uid() = id);

-- Políticas para tours (público)
CREATE POLICY "Anyone can view active tours" 
  ON tours FOR SELECT 
  USING (active = true);

-- Políticas para bookings
CREATE POLICY "Users can view own bookings" 
  ON bookings FOR SELECT 
  USING (user_id = auth.uid());

CREATE POLICY "Users can create bookings" 
  ON bookings FOR INSERT 
  WITH CHECK (user_id = auth.uid());

-- Políticas para partners
CREATE POLICY "Users can view own partner profile" 
  ON partners FOR SELECT 
  USING (user_id = auth.uid());

CREATE POLICY "Users can create partner profile" 
  ON partners FOR INSERT 
  WITH CHECK (user_id = auth.uid());

-- Políticas para reviews (público para verificadas)
CREATE POLICY "Anyone can view verified reviews" 
  ON reviews FOR SELECT 
  USING (verified = true);

CREATE POLICY "Users can create reviews" 
  ON reviews FOR INSERT 
  WITH CHECK (user_id = auth.uid());

-- ============================================
-- 5. DATOS DE EJEMPLO
-- ============================================

-- Insertar tours de ejemplo
INSERT INTO tours (title, slug, description, region, difficulty, duration_days, price_pen, category, active, featured) VALUES
('Camino Inca 4 Días', 'camino-inca-4d', 'La ruta más famosa a Machu Picchu', 'Cusco', 'challenging', 4, 2800, 'trekking', true, true),
('Rafting Urubamba', 'rafting-urubamba', 'Adrenalina en rápidos nivel 3-4', 'Cusco', 'moderate', 1, 350, 'rafting', true, true),
('Escalada Huaraz', 'escalada-huaraz', 'Conquista los Andes', 'Huaraz', 'extreme', 3, 1500, 'climbing', true, false),
('Salkantay Trek 5D', 'salkantay-5d', 'Ruta alternativa a Machu Picchu', 'Cusco', 'challenging', 5, 1800, 'trekking', true, true),
('Sandboarding Huacachina', 'sandboarding-huacachina', 'Aventura en las dunas', 'Ica', 'easy', 1, 250, 'sandboarding', true, false);

-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================

-- Contar tablas creadas
SELECT 
  'users_profiles' as table_name, COUNT(*) as count FROM users_profiles
UNION ALL
SELECT 'tours', COUNT(*) FROM tours
UNION ALL
SELECT 'bookings', COUNT(*) FROM bookings
UNION ALL
SELECT 'partners', COUNT(*) FROM partners
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews;

-- Mensaje de éxito
SELECT '✅ Base de datos Lifextreme configurada exitosamente!' AS status;
