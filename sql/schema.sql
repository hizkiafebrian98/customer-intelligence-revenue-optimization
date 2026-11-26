
-- ============================================================
-- Customer Intelligence & Revenue Optimization
-- Phase 4: Database Engineering & SQL Analytics
-- File: sql/schema.sql
-- ============================================================

-- 1. Transaction taxonomy
CREATE TABLE IF NOT EXISTS public.transaction_taxonomy (
    transaction_category TEXT PRIMARY KEY,
    merchandise_revenue_treatment TEXT NOT NULL,
    customer_level_eligible BOOLEAN NOT NULL,
    qualifying_purchase BOOLEAN NOT NULL,
    notes TEXT
);

-- 2. Approved description mapping
CREATE TABLE IF NOT EXISTS public.description_mapping (
    stock_code TEXT PRIMARY KEY,
    imputed_description TEXT NOT NULL,
    evidence_count INTEGER NOT NULL
);

-- 3. Primary analytical transaction table
CREATE TABLE IF NOT EXISTS public.retail_transactions (
    original_row_position BIGINT PRIMARY KEY,

    invoice TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    description TEXT,
    quantity BIGINT NOT NULL,
    invoice_date TIMESTAMP NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    customer_id BIGINT,
    country TEXT NOT NULL,

    year_month DATE NOT NULL,
    description_was_missing BOOLEAN NOT NULL,
    is_cancellation BOOLEAN NOT NULL,
    has_customer_id BOOLEAN NOT NULL,
    has_positive_quantity BOOLEAN NOT NULL,
    has_positive_price BOOLEAN NOT NULL,
    has_positive_line_value BOOLEAN NOT NULL,
    candidate_paid_purchase BOOLEAN NOT NULL,

    description_normalized TEXT,
    is_zero_price BOOLEAN NOT NULL,
    zero_price_category TEXT,
    stock_code_normalized TEXT NOT NULL,

    transaction_category TEXT NOT NULL,
    line_value DOUBLE PRECISION NOT NULL,
    merchandise_revenue_treatment TEXT NOT NULL,
    customer_level_eligible BOOLEAN NOT NULL,
    qualifying_purchase BOOLEAN NOT NULL,
    notes TEXT,

    is_merchandise_revenue_record BOOLEAN NOT NULL,
    is_customer_analytics_eligible BOOLEAN NOT NULL,
    is_qualifying_purchase BOOLEAN NOT NULL,
    merchandise_revenue DOUBLE PRECISION NOT NULL,
    qualifying_purchase_revenue DOUBLE PRECISION NOT NULL,

    is_excess_exact_duplicate BOOLEAN NOT NULL,
    
    CONSTRAINT fk_retail_transaction_taxonomy
        FOREIGN KEY (transaction_category)
        REFERENCES public.transaction_taxonomy (transaction_category)
);

-- 4. Duplicate transaction audit
CREATE TABLE IF NOT EXISTS public.duplicate_transaction_audit (
    LIKE public.retail_transactions INCLUDING ALL
);

ALTER TABLE public.duplicate_transaction_audit
    ADD CONSTRAINT fk_duplicate_transaction_taxonomy
    FOREIGN KEY (transaction_category)
    REFERENCES public.transaction_taxonomy (transaction_category);

-- ============================================================
-- Indexes for expected analytical queries
-- ============================================================

-- Invoice-level analysis
CREATE INDEX IF NOT EXISTS idx_retail_transactions_invoice
    ON public.retail_transactions (invoice);

-- Customer purchasing history and recency analysis
CREATE INDEX IF NOT EXISTS idx_retail_transactions_customer_date
    ON public.retail_transactions (customer_id, invoice_date);

-- Time-based analysis
CREATE INDEX IF NOT EXISTS idx_retail_transactions_invoice_date
    ON public.retail_transactions (invoice_date);

-- Transaction category filtering
CREATE INDEX IF NOT EXISTS idx_retail_transactions_category
    ON public.retail_transactions (transaction_category);

-- Product-level analysis
CREATE INDEX IF NOT EXISTS idx_retail_transactions_stock_code
    ON public.retail_transactions (stock_code);

-- Audit table lookup
CREATE INDEX IF NOT EXISTS idx_duplicate_audit_invoice
    ON public.duplicate_transaction_audit (invoice);
