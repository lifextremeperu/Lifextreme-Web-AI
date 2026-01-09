-- LIFECOIN PRESALE DATABASE SCHEMA
-- Run this in your Supabase SQL Editor

-- ============================================
-- PRESALE INVESTORS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS presale_investors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Personal Information
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    country TEXT NOT NULL DEFAULT 'Peru',
    
    -- Investment Details
    package_name TEXT NOT NULL CHECK (package_name IN ('explorador', 'aventurero', 'pionero')),
    amount_usd DECIMAL(10,2) NOT NULL CHECK (amount_usd >= 100),
    lifecoins_purchased BIGINT NOT NULL,
    lifecoins_balance BIGINT NOT NULL, -- Decreases as they use them
    
    -- Payment Information
    payment_method TEXT NOT NULL CHECK (payment_method IN ('yape', 'paypal', 'crypto')),
    payment_proof_url TEXT, -- URL to uploaded receipt/screenshot
    payment_status TEXT NOT NULL DEFAULT 'pending' CHECK (payment_status IN ('pending', 'verified', 'rejected')),
    transaction_reference TEXT, -- PayPal transaction ID or Yape reference
    
    -- Founder Benefits
    founder_badge TEXT NOT NULL DEFAULT 'bronze' CHECK (founder_badge IN ('bronze', 'gold', 'platinum')),
    lifetime_discount_percent INTEGER NOT NULL DEFAULT 50,
    exclusive_access BOOLEAN DEFAULT true,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified_at TIMESTAMP WITH TIME ZONE,
    verified_by UUID REFERENCES auth.users(id),
    notes TEXT,
    
    -- Future DAO Migration
    wallet_address TEXT UNIQUE, -- For future blockchain migration
    converted_to_equity BOOLEAN DEFAULT false
);

-- ============================================
-- LIFECOIN TRANSACTIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS lifecoin_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    investor_id UUID NOT NULL REFERENCES presale_investors(id) ON DELETE CASCADE,
    
    -- Transaction Details
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('purchase', 'spend', 'bonus', 'refund')),
    amount BIGINT NOT NULL, -- Positive for credits, negative for debits
    balance_after BIGINT NOT NULL,
    
    -- Reference
    reference_type TEXT CHECK (reference_type IN ('presale', 'booking', 'referral', 'admin_adjustment')),
    reference_id UUID, -- Links to booking_id or other tables
    description TEXT,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id)
);

-- ============================================
-- PRESALE STATS TABLE (For Dashboard)
-- ============================================
CREATE TABLE IF NOT EXISTS presale_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Aggregate Stats
    total_investors INTEGER NOT NULL DEFAULT 0,
    total_raised_usd DECIMAL(12,2) NOT NULL DEFAULT 0,
    total_lifecoins_sold BIGINT NOT NULL DEFAULT 0,
    
    -- Package Breakdown
    exploradores_count INTEGER NOT NULL DEFAULT 0,
    aventureros_count INTEGER NOT NULL DEFAULT 0,
    pioneros_count INTEGER NOT NULL DEFAULT 0,
    
    -- Payment Method Breakdown
    yape_count INTEGER NOT NULL DEFAULT 0,
    paypal_count INTEGER NOT NULL DEFAULT 0,
    crypto_count INTEGER NOT NULL DEFAULT 0,
    
    -- Status
    spots_remaining INTEGER NOT NULL DEFAULT 100,
    presale_active BOOLEAN DEFAULT true,
    
    -- Metadata
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Initialize stats table with default values
INSERT INTO presale_stats (id, spots_remaining, presale_active)
VALUES (gen_random_uuid(), 100, true)
ON CONFLICT DO NOTHING;

-- ============================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE presale_investors ENABLE ROW LEVEL SECURITY;
ALTER TABLE lifecoin_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE presale_stats ENABLE ROW LEVEL SECURITY;

-- Presale Investors Policies
-- Allow public to insert (for registration)
CREATE POLICY "Allow public insert for presale investors"
ON presale_investors FOR INSERT
TO public
WITH CHECK (true);

-- Allow users to view their own investment
CREATE POLICY "Users can view own investment"
ON presale_investors FOR SELECT
TO authenticated
USING (auth.uid() IN (SELECT id FROM auth.users WHERE email = presale_investors.email));

-- Allow admins to view all
CREATE POLICY "Admins can view all investors"
ON presale_investors FOR SELECT
TO authenticated
USING (
    auth.uid() IN (
        SELECT id FROM auth.users 
        WHERE email IN ('admin@lifextreme.com', 'alex@lifextreme.com')
    )
);

-- Allow admins to update (verify payments)
CREATE POLICY "Admins can update investors"
ON presale_investors FOR UPDATE
TO authenticated
USING (
    auth.uid() IN (
        SELECT id FROM auth.users 
        WHERE email IN ('admin@lifextreme.com', 'alex@lifextreme.com')
    )
);

-- Lifecoin Transactions Policies
-- Users can view their own transactions
CREATE POLICY "Users can view own transactions"
ON lifecoin_transactions FOR SELECT
TO authenticated
USING (
    investor_id IN (
        SELECT id FROM presale_investors 
        WHERE email IN (SELECT email FROM auth.users WHERE id = auth.uid())
    )
);

-- Admins can view all transactions
CREATE POLICY "Admins can view all transactions"
ON lifecoin_transactions FOR SELECT
TO authenticated
USING (
    auth.uid() IN (
        SELECT id FROM auth.users 
        WHERE email IN ('admin@lifextreme.com', 'alex@lifextreme.com')
    )
);

-- Presale Stats Policies
-- Allow public to view stats (for homepage)
CREATE POLICY "Allow public to view presale stats"
ON presale_stats FOR SELECT
TO public
USING (true);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Function to update presale stats
CREATE OR REPLACE FUNCTION update_presale_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE presale_stats
    SET 
        total_investors = (SELECT COUNT(*) FROM presale_investors WHERE payment_status = 'verified'),
        total_raised_usd = (SELECT COALESCE(SUM(amount_usd), 0) FROM presale_investors WHERE payment_status = 'verified'),
        total_lifecoins_sold = (SELECT COALESCE(SUM(lifecoins_purchased), 0) FROM presale_investors WHERE payment_status = 'verified'),
        exploradores_count = (SELECT COUNT(*) FROM presale_investors WHERE package_name = 'explorador' AND payment_status = 'verified'),
        aventureros_count = (SELECT COUNT(*) FROM presale_investors WHERE package_name = 'aventurero' AND payment_status = 'verified'),
        pioneros_count = (SELECT COUNT(*) FROM presale_investors WHERE package_name = 'pionero' AND payment_status = 'verified'),
        spots_remaining = 100 - (SELECT COUNT(*) FROM presale_investors WHERE payment_status = 'verified'),
        updated_at = NOW()
    WHERE id = (SELECT id FROM presale_stats LIMIT 1);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update stats on investor changes
CREATE TRIGGER update_stats_on_investor_change
AFTER INSERT OR UPDATE ON presale_investors
FOR EACH ROW
EXECUTE FUNCTION update_presale_stats();

-- Function to record lifecoin transaction
CREATE OR REPLACE FUNCTION record_lifecoin_transaction(
    p_investor_id UUID,
    p_amount BIGINT,
    p_type TEXT,
    p_reference_type TEXT DEFAULT NULL,
    p_reference_id UUID DEFAULT NULL,
    p_description TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_new_balance BIGINT;
    v_transaction_id UUID;
BEGIN
    -- Get current balance and calculate new balance
    SELECT lifecoins_balance INTO v_new_balance
    FROM presale_investors
    WHERE id = p_investor_id;
    
    v_new_balance := v_new_balance + p_amount;
    
    -- Update investor balance
    UPDATE presale_investors
    SET lifecoins_balance = v_new_balance
    WHERE id = p_investor_id;
    
    -- Insert transaction record
    INSERT INTO lifecoin_transactions (
        investor_id,
        transaction_type,
        amount,
        balance_after,
        reference_type,
        reference_id,
        description
    ) VALUES (
        p_investor_id,
        p_type,
        p_amount,
        v_new_balance,
        p_reference_type,
        p_reference_id,
        p_description
    ) RETURNING id INTO v_transaction_id;
    
    RETURN v_transaction_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_presale_investors_email ON presale_investors(email);
CREATE INDEX idx_presale_investors_payment_status ON presale_investors(payment_status);
CREATE INDEX idx_presale_investors_created_at ON presale_investors(created_at DESC);
CREATE INDEX idx_lifecoin_transactions_investor_id ON lifecoin_transactions(investor_id);
CREATE INDEX idx_lifecoin_transactions_created_at ON lifecoin_transactions(created_at DESC);

-- ============================================
-- SAMPLE DATA (FOR TESTING)
-- ============================================
-- Uncomment to insert test data

/*
INSERT INTO presale_investors (
    full_name, email, phone, country,
    package_name, amount_usd, lifecoins_purchased, lifecoins_balance,
    payment_method, payment_status, founder_badge
) VALUES
    ('Juan Pérez', 'juan@example.com', '+51999999001', 'Peru', 'aventurero', 500, 10000, 10000, 'yape', 'verified', 'gold'),
    ('María García', 'maria@example.com', '+51999999002', 'Peru', 'explorador', 100, 2000, 2000, 'paypal', 'verified', 'bronze'),
    ('Carlos López', 'carlos@example.com', '+51999999003', 'Peru', 'pionero', 1000, 25000, 25000, 'yape', 'verified', 'platinum');
*/

-- ============================================
-- ADMIN QUERIES (USEFUL FOR MANAGEMENT)
-- ============================================

-- View all pending payments
-- SELECT * FROM presale_investors WHERE payment_status = 'pending' ORDER BY created_at DESC;

-- View total raised
-- SELECT SUM(amount_usd) as total_raised FROM presale_investors WHERE payment_status = 'verified';

-- View investor breakdown by package
-- SELECT package_name, COUNT(*) as count, SUM(amount_usd) as total 
-- FROM presale_investors 
-- WHERE payment_status = 'verified' 
-- GROUP BY package_name;

-- View recent transactions
-- SELECT t.*, i.full_name, i.email 
-- FROM lifecoin_transactions t
-- JOIN presale_investors i ON t.investor_id = i.id
-- ORDER BY t.created_at DESC
-- LIMIT 20;
