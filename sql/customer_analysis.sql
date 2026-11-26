-- 1. Highest-revenue customers

SELECT
    customer_id,
    COUNT(DISTINCT invoice) AS purchase_count,
    SUM(qualifying_purchase_revenue) AS total_revenue,
    MIN(invoice_date) AS first_purchase_date,
    MAX(invoice_date) AS last_purchase_date
FROM public.retail_transactions
WHERE customer_id IS NOT NULL
  AND is_qualifying_purchase = TRUE
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 20;


-- 2. Customer purchase frequency distribution

WITH customer_frequency AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice) AS purchase_count
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN purchase_count = 1 THEN '1 purchase'
        WHEN purchase_count BETWEEN 2 AND 5 THEN '2-5 purchases'
        WHEN purchase_count BETWEEN 6 AND 10 THEN '6-10 purchases'
        WHEN purchase_count BETWEEN 11 AND 20 THEN '11-20 purchases'
        ELSE 'More than 20 purchases'
    END AS purchase_frequency_group,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM customer_frequency
GROUP BY
    CASE
        WHEN purchase_count = 1 THEN '1 purchase'
        WHEN purchase_count BETWEEN 2 AND 5 THEN '2-5 purchases'
        WHEN purchase_count BETWEEN 6 AND 10 THEN '6-10 purchases'
        WHEN purchase_count BETWEEN 11 AND 20 THEN '11-20 purchases'
        ELSE 'More than 20 purchases'
    END
ORDER BY MIN(purchase_count);


-- 3. Customer revenue distribution

WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(qualifying_purchase_revenue) AS total_revenue
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT
        customer_id,
        total_revenue,
        NTILE(10) OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_decile
    FROM customer_revenue
)
SELECT
    revenue_decile,
    COUNT(*) AS customer_count,
    ROUND(SUM(total_revenue)::NUMERIC, 2) AS segment_revenue,
    ROUND(
        (
            SUM(total_revenue) * 100.0
            / SUM(SUM(total_revenue)) OVER ()
        )::NUMERIC,
        2
    ) AS revenue_percentage,
    ROUND(
        AVG(total_revenue)::NUMERIC,
        2
    ) AS average_customer_revenue
FROM ranked_customers
GROUP BY revenue_decile
ORDER BY revenue_decile;

-- 4. Customer purchase recency

WITH customer_recency AS (
    SELECT
        customer_id,
        MAX(invoice_date) AS last_purchase_date,
        DATE '2011-12-09' - MAX(invoice_date)::DATE
            AS recency_days,
        SUM(qualifying_purchase_revenue) AS total_revenue,
        COUNT(DISTINCT invoice) AS purchase_count
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN recency_days <= 30 THEN '0-30 days'
        WHEN recency_days <= 60 THEN '31-60 days'
        WHEN recency_days <= 90 THEN '61-90 days'
        WHEN recency_days <= 180 THEN '91-180 days'
        WHEN recency_days <= 365 THEN '181-365 days'
        ELSE 'More than 365 days'
    END AS recency_group,
    COUNT(*) AS customer_count,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER ()::NUMERIC,
        2
    ) AS customer_percentage,
    ROUND(
        SUM(total_revenue)::NUMERIC,
        2
    ) AS segment_revenue,
    ROUND(
        AVG(total_revenue)::NUMERIC,
        2
    ) AS average_customer_revenue
FROM customer_recency
GROUP BY
    CASE
        WHEN recency_days <= 30 THEN '0-30 days'
        WHEN recency_days <= 60 THEN '31-60 days'
        WHEN recency_days <= 90 THEN '61-90 days'
        WHEN recency_days <= 180 THEN '91-180 days'
        WHEN recency_days <= 365 THEN '181-365 days'
        ELSE 'More than 365 days'
    END
ORDER BY MIN(recency_days);


-- 5. Revenue by country

SELECT
    country,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT invoice) AS invoice_count,
    ROUND(
        SUM(qualifying_purchase_revenue)::NUMERIC,
        2
    ) AS total_revenue,
    ROUND(
        (
            SUM(qualifying_purchase_revenue) * 100.0
            / SUM(SUM(qualifying_purchase_revenue)) OVER ()
        )::NUMERIC,
        2
    ) AS revenue_percentage
FROM public.retail_transactions
WHERE customer_id IS NOT NULL
  AND is_qualifying_purchase = TRUE
GROUP BY country
ORDER BY total_revenue DESC;


-- 6. Monthly revenue trends and month-over-month changes

WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', invoice_date)::DATE AS revenue_month,
        COUNT(DISTINCT invoice) AS invoice_count,
        COUNT(DISTINCT customer_id) AS customer_count,
        SUM(qualifying_purchase_revenue) AS total_revenue
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY DATE_TRUNC('month', invoice_date)
),
monthly_comparison AS (
    SELECT
        revenue_month,
        invoice_count,
        customer_count,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY revenue_month
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    revenue_month,
    invoice_count,
    customer_count,
    ROUND(total_revenue::NUMERIC, 2) AS total_revenue,
    ROUND(previous_month_revenue::NUMERIC, 2)
        AS previous_month_revenue,
    ROUND(
        (
            (total_revenue - previous_month_revenue)
            / NULLIF(previous_month_revenue, 0) * 100
        )::NUMERIC,
        2
    ) AS revenue_change_percentage
FROM monthly_comparison
ORDER BY revenue_month;


-- 7. Customer revenue ranking and cumulative contribution

WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(qualifying_purchase_revenue) AS total_revenue
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT
        customer_id,
        total_revenue,

        RANK() OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_rank,

        ROW_NUMBER() OVER (
            ORDER BY total_revenue DESC, customer_id
        ) AS row_number,

        SUM(total_revenue) OVER (
            ORDER BY total_revenue DESC, customer_id
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS cumulative_revenue,

        SUM(total_revenue) OVER () AS overall_revenue

    FROM customer_revenue
)
SELECT
    customer_id,
    revenue_rank,
    row_number,
    ROUND(total_revenue::NUMERIC, 2) AS total_revenue,
    ROUND(cumulative_revenue::NUMERIC, 2) AS cumulative_revenue,
    ROUND(
        (cumulative_revenue * 100.0 / overall_revenue)::NUMERIC,
        2
    ) AS cumulative_revenue_percentage
FROM ranked_customers
ORDER BY revenue_rank
LIMIT 20;


-- 8. Customer purchasing behavior by transaction category

SELECT
    customer_id,

    COUNT(DISTINCT invoice) AS total_invoices,

    COUNT(*) FILTER (
        WHERE transaction_category = 'merchandise_candidate'
    ) AS merchandise_records,

    SUM(
        CASE
            WHEN transaction_category = 'merchandise_candidate'
            THEN line_value
            ELSE 0
        END
    ) AS merchandise_line_value,

    COUNT(*) FILTER (
        WHERE transaction_category = 'merchandise_cancellation_candidate'
    ) AS cancellation_records,

    SUM(
        CASE
            WHEN transaction_category = 'merchandise_cancellation_candidate'
            THEN line_value
            ELSE 0
        END
    ) AS cancellation_line_value,

    SUM(qualifying_purchase_revenue) AS qualifying_purchase_revenue

FROM public.retail_transactions
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY qualifying_purchase_revenue DESC
LIMIT 20;


-- 9. Customer purchase and cancellation analysis using JOINs

WITH purchase_metrics AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice) AS purchase_invoice_count,
        SUM(qualifying_purchase_revenue) AS purchase_revenue
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND is_qualifying_purchase = TRUE
    GROUP BY customer_id
),
cancellation_metrics AS (
    SELECT
        customer_id,
        COUNT(*) AS cancellation_record_count,
        SUM(line_value) AS cancellation_value
    FROM public.retail_transactions
    WHERE customer_id IS NOT NULL
      AND transaction_category = 'merchandise_cancellation_candidate'
    GROUP BY customer_id
)
SELECT
    COALESCE(p.customer_id, c.customer_id) AS customer_id,

    COALESCE(p.purchase_invoice_count, 0) AS purchase_invoice_count,

    COALESCE(p.purchase_revenue, 0) AS purchase_revenue,

    COALESCE(c.cancellation_record_count, 0) AS cancellation_record_count,

    COALESCE(c.cancellation_value, 0) AS cancellation_value,

    ROUND(
        (
            ABS(COALESCE(c.cancellation_value, 0))
            * 100.0
            / NULLIF(p.purchase_revenue, 0)
        )::NUMERIC,
        2
    ) AS cancellation_value_percentage

FROM purchase_metrics p
FULL OUTER JOIN cancellation_metrics c
    ON p.customer_id = c.customer_id
ORDER BY
    COALESCE(p.purchase_revenue, 0) DESC NULLS LAST
LIMIT 20;