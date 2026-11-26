-- 1. Record-count reconciliation

WITH expected_counts AS (
    SELECT *
    FROM (VALUES
        ('retail_transactions', 1033036::BIGINT),
        ('duplicate_transaction_audit', 34335::BIGINT),
        ('transaction_taxonomy', 16::BIGINT),
        ('description_mapping', 1387::BIGINT)
    ) AS expected(table_name, expected_count)
),
actual_counts AS (
    SELECT 'retail_transactions' AS table_name,
           COUNT(*) AS actual_count
    FROM public.retail_transactions

    UNION ALL

    SELECT 'duplicate_transaction_audit',
           COUNT(*)
    FROM public.duplicate_transaction_audit

    UNION ALL

    SELECT 'transaction_taxonomy',
           COUNT(*)
    FROM public.transaction_taxonomy

    UNION ALL

    SELECT 'description_mapping',
           COUNT(*)
    FROM public.description_mapping
)
SELECT
    e.table_name,
    e.expected_count,
    a.actual_count,
    a.actual_count - e.expected_count AS difference,
    CASE
        WHEN a.actual_count = e.expected_count THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM expected_counts e
JOIN actual_counts a
    ON e.table_name = a.table_name
ORDER BY e.table_name;


-- 2. Primary-key integrity and null validation

SELECT
    'retail_transactions' AS table_name,
    COUNT(*) AS total_records,
    COUNT(original_row_position) AS non_null_primary_keys,
    COUNT(DISTINCT original_row_position) AS unique_primary_keys,
    CASE
        WHEN COUNT(*) = COUNT(original_row_position)
         AND COUNT(*) = COUNT(DISTINCT original_row_position)
        THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM public.retail_transactions

UNION ALL

SELECT
    'duplicate_transaction_audit',
    COUNT(*),
    COUNT(original_row_position),
    COUNT(DISTINCT original_row_position),
    CASE
        WHEN COUNT(*) = COUNT(original_row_position)
         AND COUNT(*) = COUNT(DISTINCT original_row_position)
        THEN 'PASS'
        ELSE 'FAIL'
    END
FROM public.duplicate_transaction_audit

UNION ALL

SELECT
    'transaction_taxonomy',
    COUNT(*),
    COUNT(transaction_category),
    COUNT(DISTINCT transaction_category),
    CASE
        WHEN COUNT(*) = COUNT(transaction_category)
         AND COUNT(*) = COUNT(DISTINCT transaction_category)
        THEN 'PASS'
        ELSE 'FAIL'
    END
FROM public.transaction_taxonomy

UNION ALL

SELECT
    'description_mapping',
    COUNT(*),
    COUNT(stock_code),
    COUNT(DISTINCT stock_code),
    CASE
        WHEN COUNT(*) = COUNT(stock_code)
         AND COUNT(*) = COUNT(DISTINCT stock_code)
        THEN 'PASS'
        ELSE 'FAIL'
    END
FROM public.description_mapping;


-- 3. Foreign-key and taxonomy consistency

SELECT
    'retail_transactions' AS table_name,
    COUNT(*) AS unmatched_records,
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS validation_status
FROM public.retail_transactions t
LEFT JOIN public.transaction_taxonomy tax
    ON t.transaction_category = tax.transaction_category
WHERE tax.transaction_category IS NULL

UNION ALL

SELECT
    'duplicate_transaction_audit',
    COUNT(*),
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END
FROM public.duplicate_transaction_audit d
LEFT JOIN public.transaction_taxonomy tax
    ON d.transaction_category = tax.transaction_category
WHERE tax.transaction_category IS NULL;

-- 4. Financial reconciliation

SELECT
    COUNT(*) AS total_records,

    SUM(merchandise_revenue) AS total_merchandise_revenue,

    SUM(qualifying_purchase_revenue) AS total_qualifying_purchase_revenue,

    SUM(
        CASE
            WHEN is_merchandise_revenue_record
            THEN merchandise_revenue
            ELSE 0
        END
    ) AS recalculated_merchandise_revenue,

    SUM(
        CASE
            WHEN is_qualifying_purchase
            THEN line_value
            ELSE 0
        END
    ) AS recalculated_qualifying_purchase_revenue

FROM public.retail_transactions;