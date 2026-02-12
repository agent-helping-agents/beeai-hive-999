-- Solend Lending Integration - Database Schema
-- This file defines the database tables for the Solend lending platform
-- including market data, reserves, obligations, and transaction history.

-- Enable UUID extension for unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgcrypto for encryption and hashing
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enable pgvector for vector search
CREATE EXTENSION IF NOT EXISTS "vector";

-- ==============================================================================
-- Solend Markets
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_markets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market_address TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    creator TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_markets_primary ON solend_markets(is_primary);
CREATE INDEX IF NOT EXISTS idx_solend_markets_creator ON solend_markets(creator);

-- ==============================================================================
-- Solend Reserves
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_reserves (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reserve_address TEXT NOT NULL UNIQUE,
    market_id UUID NOT NULL REFERENCES solend_markets(id) ON DELETE CASCADE,
    liquidity_mint TEXT NOT NULL,
    collateral_mint TEXT NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    supply_apy NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    borrow_apy NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    liquidity_available NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    liquidity_borrowed NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    collateral_available NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    optimal_utilization_rate NUMERIC(5, 4) NOT NULL DEFAULT 0.80,
    loan_to_value_ratio NUMERIC(5, 4) NOT NULL DEFAULT 0.75,
    liquidation_bonus NUMERIC(5, 4) NOT NULL DEFAULT 0.05,
    liquidation_threshold NUMERIC(5, 4) NOT NULL DEFAULT 0.80,
    min_borrow_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    optimal_borrow_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.05,
    max_borrow_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.20,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_reserves_market ON solend_reserves(market_id);
CREATE INDEX IF NOT EXISTS idx_solend_reserves_liquidity_mint ON solend_reserves(liquidity_mint);
CREATE INDEX IF NOT EXISTS idx_solend_reserves_symbol ON solend_reserves(symbol);

-- ==============================================================================
-- Solend Obligations (User Positions)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_obligations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    obligation_address TEXT NOT NULL UNIQUE,
    user_wallet TEXT NOT NULL,
    market_id UUID NOT NULL REFERENCES solend_markets(id) ON DELETE CASCADE,
    collateral_value NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    borrowed_value NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    health_factor NUMERIC(10, 4) NOT NULL DEFAULT 1.0,
    is_liquidatable BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_obligations_user ON solend_obligations(user_wallet);
CREATE INDEX IF NOT EXISTS idx_solend_obligations_market ON solend_obligations(market_id);
CREATE INDEX IF NOT EXISTS idx_solend_obligations_liquidatable ON solend_obligations(is_liquidatable);

-- ==============================================================================
-- Solend Obligation Collateral
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_obligation_collateral (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    obligation_id UUID NOT NULL REFERENCES solend_obligations(id) ON DELETE CASCADE,
    reserve_id UUID NOT NULL REFERENCES solend_reserves(id) ON DELETE CASCADE,
    collateral_amount NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    collateral_value NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(obligation_id, reserve_id)
);

CREATE INDEX IF NOT EXISTS idx_solend_obligation_collateral_obligation ON solend_obligation_collateral(obligation_id);
CREATE INDEX IF NOT EXISTS idx_solend_obligation_collateral_reserve ON solend_obligation_collateral(reserve_id);

-- ==============================================================================
-- Solend Obligation Borrows
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_obligation_borrows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    obligation_id UUID NOT NULL REFERENCES solend_obligations(id) ON DELETE CASCADE,
    reserve_id UUID NOT NULL REFERENCES solend_reserves(id) ON DELETE CASCADE,
    borrow_amount NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    borrow_value NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    interest_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(obligation_id, reserve_id)
);

CREATE INDEX IF NOT EXISTS idx_solend_obligation_borrows_obligation ON solend_obligation_borrows(obligation_id);
CREATE INDEX IF NOT EXISTS idx_solend_obligation_borrows_reserve ON solend_obligation_borrows(reserve_id);

-- ==============================================================================
-- Solend Transactions
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_signature TEXT NOT NULL UNIQUE,
    user_wallet TEXT NOT NULL,
    transaction_type TEXT NOT NULL, -- deposit, borrow, repay, withdraw, liquidate
    reserve_id UUID REFERENCES solend_reserves(id) ON DELETE SET NULL,
    obligation_id UUID REFERENCES solend_obligations(id) ON DELETE SET NULL,
    amount NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    value NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    fee NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    status TEXT NOT NULL DEFAULT 'pending', -- pending, confirmed, failed
    block_number BIGINT,
    block_timestamp TIMESTAMPTZ,
    signature TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_transactions_user ON solend_transactions(user_wallet);
CREATE INDEX IF NOT EXISTS idx_solend_transactions_type ON solend_transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_solend_transactions_status ON solend_transactions(status);
CREATE INDEX IF NOT EXISTS idx_solend_transactions_block ON solend_transactions(block_number);

-- ==============================================================================
-- Solend Portfolio History
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_portfolio_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_wallet TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_collateral NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    total_borrowed NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    health_factor NUMERIC(10, 4) NOT NULL DEFAULT 1.0,
    net_worth NUMERIC(20, 8) NOT NULL DEFAULT 0.0
);

CREATE INDEX IF NOT EXISTS idx_solend_portfolio_history_user ON solend_portfolio_history(user_wallet);
CREATE INDEX IF NOT EXISTS idx_solend_portfolio_history_timestamp ON solend_portfolio_history(timestamp DESC);

-- ==============================================================================
-- Solend Market Analytics
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_market_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market_id UUID NOT NULL REFERENCES solend_markets(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total_liquidity NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    total_borrowed NUMERIC(20, 8) NOT NULL DEFAULT 0.0,
    utilization_rate NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    average_supply_apy NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    average_borrow_apy NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    total_users BIGINT NOT NULL DEFAULT 0,
    active_obligations BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_solend_market_analytics_market ON solend_market_analytics(market_id);
CREATE INDEX IF NOT EXISTS idx_solend_market_analytics_timestamp ON solend_market_analytics(timestamp DESC);

-- ==============================================================================
-- Solend Risk Assessment Models
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_risk_models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name TEXT NOT NULL UNIQUE,
    model_version TEXT NOT NULL DEFAULT '1.0.0',
    description TEXT,
    parameters JSONB NOT NULL DEFAULT '{}'::JSONB,
    training_data_source TEXT,
    accuracy_score NUMERIC(5, 4) NOT NULL DEFAULT 0.0,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS solend_risk_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    obligation_id UUID NOT NULL REFERENCES solend_obligations(id) ON DELETE CASCADE,
    risk_model_id UUID NOT NULL REFERENCES solend_risk_models(id) ON DELETE CASCADE,
    risk_score NUMERIC(5, 4) NOT NULL DEFAULT 0.0,
    liquidation_probability NUMERIC(5, 4) NOT NULL DEFAULT 0.0,
    confidence_score NUMERIC(5, 4) NOT NULL DEFAULT 0.0,
    risk_factors JSONB NOT NULL DEFAULT '{}'::JSONB,
    recommendations JSONB NOT NULL DEFAULT '{}'::JSONB,
    assessed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_risk_assessments_obligation ON solend_risk_assessments(obligation_id);
CREATE INDEX IF NOT EXISTS idx_solend_risk_assessments_model ON solend_risk_assessments(risk_model_id);

-- ==============================================================================
-- Solend Strategy Recommendations
-- ==============================================================================

CREATE TABLE IF NOT EXISTS solend_strategy_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_wallet TEXT NOT NULL,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT NOT NULL, -- lending, borrowing, diversification
    recommended_action TEXT NOT NULL,
    expected_apy NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    risk_level TEXT NOT NULL DEFAULT 'medium', -- low, medium, high
    confidence_score NUMERIC(5, 4) NOT NULL DEFAULT 0.0,
    parameters JSONB NOT NULL DEFAULT '{}'::JSONB,
    is_executed BOOLEAN NOT NULL DEFAULT FALSE,
    executed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solend_strategy_recommendations_user ON solend_strategy_recommendations(user_wallet);
CREATE INDEX IF NOT EXISTS idx_solend_strategy_recommendations_type ON solend_strategy_recommendations(strategy_type);
CREATE INDEX IF NOT EXISTS idx_solend_strategy_recommendations_risk ON solend_strategy_recommendations(risk_level);

-- ==============================================================================
-- Trigger to update updated_at column
-- ==============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_solend_markets_updated_at BEFORE UPDATE ON solend_markets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_reserves_updated_at BEFORE UPDATE ON solend_reserves
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_obligations_updated_at BEFORE UPDATE ON solend_obligations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_obligation_collateral_updated_at BEFORE UPDATE ON solend_obligation_collateral
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_obligation_borrows_updated_at BEFORE UPDATE ON solend_obligation_borrows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_transactions_updated_at BEFORE UPDATE ON solend_transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_solend_risk_models_updated_at BEFORE UPDATE ON solend_risk_models
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==============================================================================
-- Initial Data Seed
-- ==============================================================================

-- Insert main market
INSERT INTO solend_markets (market_address, name, description, is_primary, creator)
VALUES ('4UpD2fh7xH3VP9QQaXtsS1YY3bxzWhtfpks7FatyKvdY', 'main', 'Solend main market', TRUE, '5pHk2TmnqQzRF9L6egy5FfiyBgS7G9cMZ5RFaJAvghzw')
ON CONFLICT DO NOTHING;

-- Insert sample reserves
INSERT INTO solend_reserves (reserve_address, market_id, liquidity_mint, collateral_mint, symbol, name, description, supply_apy, borrow_apy, liquidity_available, liquidity_borrowed, collateral_available)
SELECT 
    '4UpD2fh7xH3VP9QQaXtsS1YY3bxzWhtfpks7FatyKvdY', 
    id,
    'EPjFWdd5AufqSSqeM2qN1xzybajdD4iK6G5cX5QJQW8', -- USDC mint
    '9xQeWvL9zG9h3gF5hV9S1aYcKX9QeR7jVvZL2b5Z9cM', -- Solend collateral mint
    'USDC',
    'USD Coin',
    'USD Coin reserve on Solend',
    0.025, -- 2.5% supply APY
    0.075, -- 7.5% borrow APY
    1000000.00, -- 1,000,000 USDC available
    500000.00, -- 500,000 USDC borrowed
    1500000.00 -- $1,500,000 in collateral
FROM solend_markets
WHERE is_primary = TRUE
ON CONFLICT DO NOTHING;

-- Insert SOL reserve
INSERT INTO solend_reserves (reserve_address, market_id, liquidity_mint, collateral_mint, symbol, name, description, supply_apy, borrow_apy, liquidity_available, liquidity_borrowed, collateral_available)
SELECT 
    'So11111111111111111111111111111111111111112',
    id,
    'So11111111111111111111111111111111111111112', -- SOL mint
    'So11111111111111111111111111111111111111112', -- SOL collateral mint
    'SOL',
    'Solana',
    'Solana reserve on Solend',
    0.040, -- 4.0% supply APY
    0.100, -- 10.0% borrow APY
    50000.00, -- 50,000 SOL available
    25000.00, -- 25,000 SOL borrowed
    75000.00 -- 75,000 SOL in collateral
FROM solend_markets
WHERE is_primary = TRUE
ON CONFLICT DO NOTHING;