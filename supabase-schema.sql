-- TABLAS SUPABASE - LIFEXTREME
-- Ejecutar en: https://supabase.com/dashboard/project/YOUR_PROJECT/editor

-- 1. Tabla de reservas
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_phone VARCHAR(50),
    tour_id INTEGER NOT NULL,
    tour_name VARCHAR(255) NOT NULL,
    tour_date DATE NOT NULL,
    participants INTEGER DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. Tabla de perfiles IA
CREATE TABLE ai_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_email VARCHAR(255) UNIQUE NOT NULL,
    profile_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. Índices para performance
CREATE INDEX idx_bookings_email ON bookings(user_email);
CREATE INDEX idx_bookings_status ON bookings(payment_status);
CREATE INDEX idx_bookings_date ON bookings(tour_date);
CREATE INDEX idx_ai_profiles_email ON ai_profiles(user_email);

-- 4. Row Level Security (RLS)
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_profiles ENABLE ROW LEVEL SECURITY;

-- Políticas: Permitir INSERT/SELECT público
CREATE POLICY "Permitir insert público" ON bookings FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir select público" ON bookings FOR SELECT USING (true);
CREATE POLICY "Permitir insert público" ON ai_profiles FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir upsert público" ON ai_profiles FOR UPDATE USING (true);
