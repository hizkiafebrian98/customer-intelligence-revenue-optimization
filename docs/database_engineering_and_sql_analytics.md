# Phase 4 — Database Engineering & SQL Analytics

## 1. Overview

Phase 4 establishes a PostgreSQL database for the Online Retail II dataset and implements SQL-based customer analytics.

The objectives were to:

- Design a relational database schema.
- Load cleaned transaction data and reference datasets into PostgreSQL.
- Validate data integrity and financial consistency.
- Develop customer-level analytical queries.
- Demonstrate advanced SQL techniques, including JOINs, CTEs, conditional aggregation, and window functions.

**Database:** PostgreSQL 17.7  
**Python integration:** SQLAlchemy 2.0.48 and Psycopg 3.3.2

## 2. Database Architecture

Four relational tables were implemented.

| Table | Records | Purpose |
|---|---:|---|
| `retail_transactions` | 1,033,036 | Primary cleaned transaction dataset |
| `duplicate_transaction_audit` | 34,335 | Preserved excess exact duplicate records |
| `transaction_taxonomy` | 16 | Transaction classification reference |
| `description_mapping` | 1,387 | StockCode description mapping reference |

### Schema design

The schema uses appropriate PostgreSQL data types:

- `TEXT` for string attributes.
- `BIGINT` for integer identifiers and quantities.
- `DOUBLE PRECISION` for numerical and financial values.
- `TIMESTAMP` for transaction dates.
- `DATE` for monthly reference dates.
- `BOOLEAN` for classification and eligibility indicators.

Primary keys:

- `original_row_position` for both transaction tables.
- `transaction_category` for `transaction_taxonomy`.
- `stock_code` for `description_mapping`.

Foreign-key relationships connect both transaction tables to `transaction_taxonomy`.

Indexes were created on frequently queried transaction attributes, including invoice, customer ID, invoice date, transaction category, and stock code.

The schema implementation is maintained in `sql/schema.sql`.

## 3. Data Loading Pipeline

A reusable Python loading module was implemented in:

`src/data/load.py`

The loading pipeline performs the following operations:

1. Reads the cleaned transaction dataset from Parquet.
2. Reads the duplicate audit and reference datasets from CSV.
3. Normalizes column names for PostgreSQL compatibility.
4. Converts date and nullable identifier fields into compatible Python types.
5. Checks expected source record counts.
6. Checks destination schema compatibility.
7. Loads reference tables before dependent transaction tables.
8. Verifies destination record counts before committing the database transaction.

The pipeline uses SQLAlchemy transactions to ensure that failed loads do not leave partially committed datasets.

### Loading results

All four datasets were loaded successfully.

| Table | Expected records | Loaded records | Result |
|---|---:|---:|---|
| `retail_transactions` | 1,033,036 | 1,033,036 | PASS |
| `duplicate_transaction_audit` | 34,335 | 34,335 | PASS |
| `transaction_taxonomy` | 16 | 16 | PASS |
| `description_mapping` | 1,387 | 1,387 | PASS |

Total records loaded: **1,068,774**.

## 4. Database Validation

Database-level validation was implemented in `sql/data_quality.sql`.

The validation focused on record completeness, key integrity, taxonomy consistency, and financial reconciliation.

### 4.1 Record-count reconciliation

All four PostgreSQL tables matched their expected source record counts.

Result: **4/4 PASS**.

### 4.2 Primary-key integrity

Each table was checked for:

- Non-null primary-key values.
- Unique primary-key values.
- Consistency between total records and valid key counts.

Result: **4/4 PASS**.

### 4.3 Taxonomy consistency

Both transaction tables were checked against `transaction_taxonomy`.

No unmatched transaction categories were found.

| Table | Unmatched records | Result |
|---|---:|---|
| `retail_transactions` | 0 | PASS |
| `duplicate_transaction_audit` | 0 | PASS |

### 4.4 Financial reconciliation

Stored financial measures were compared with values recalculated from their underlying transaction fields and eligibility indicators.

| Measure | Stored total | Recalculated total |
|---|---:|---:|
| Merchandise revenue | 18,919,878.2470 | 18,919,878.2470 |
| Qualifying purchase revenue | 17,067,278.7370 | 17,067,278.7370 |

Both measures reconciled successfully.

The distinction between the measures was preserved:

- Merchandise revenue includes applicable positive and negative merchandise adjustments.
- Qualifying purchase revenue includes qualifying identified-customer paid purchases.

These measures are not interchangeable.

## 5. Customer Analytics

Customer analytics were implemented in `sql/customer_analysis.sql`.

The analysis uses identified customers and the established transaction eligibility definitions from Phase 3.

### 5.1 Highest-revenue customers

Customers were ranked by total qualifying purchase revenue.

The highest-revenue customers included:

| Customer ID | Purchase invoices | Qualifying purchase revenue |
|---|---:|---:|
| 18102 | 145 | 580,987.04 |
| 14646 | 145 | 526,751.52 |
| 14156 | 144 | 303,069.88 |
| 14911 | 373 | 272,245.29 |
| 17450 | 51 | 244,784.25 |

Customer 18102 generated the highest observed qualifying purchase revenue.

Customer 14911 demonstrated particularly high purchase frequency, with 373 distinct invoices.

### 5.2 Customer purchase frequency

Customers were grouped according to their number of distinct qualifying purchase invoices.

| Purchase frequency | Customers | Percentage |
|---|---:|---:|
| 1 purchase | 1,618 | 27.65% |
| 2–5 purchases | 2,448 | 41.83% |
| 6–10 purchases | 922 | 15.76% |
| 11–20 purchases | 574 | 9.81% |
| More than 20 purchases | 290 | 4.96% |

Approximately 69.48% of identified customers made no more than five purchases during the observation period.

Only 4.96% made more than 20 purchases.

These are observed purchase frequencies, not definitive customer lifetime classifications.

### 5.3 Customer revenue distribution

Customers were divided into ten approximately equal-sized revenue deciles using `NTILE()`.

| Revenue decile | Customers | Revenue share |
|---|---:|---:|
| 1 — Highest | 586 | 63.90% |
| 2 | 586 | 13.29% |
| 3 | 585 | 7.78% |
| 4 | 585 | 5.06% |
| 5 | 585 | 3.51% |
| 6 | 585 | 2.48% |
| 7 | 585 | 1.70% |
| 8 | 585 | 1.17% |
| 9 | 585 | 0.75% |
| 10 — Lowest | 585 | 0.36% |

The highest-revenue decile generated 63.90% of total qualifying purchase revenue.

This indicates substantial revenue concentration among a relatively small proportion of customers.

### 5.4 Customer purchase recency

Customer recency was calculated using December 9, 2011, as the fixed reference date.

| Recency group | Customers | Percentage |
|---|---:|---:|
| 0–30 days | 1,666 | 28.47% |
| 31–60 days | 742 | 12.68% |
| 61–90 days | 477 | 8.15% |
| 91–180 days | 589 | 10.06% |
| 181–365 days | 797 | 13.62% |
| More than 365 days | 1,581 | 27.02% |

Customers with a qualifying purchase within the previous 90 days represented 49.30% of identified customers.

The most recent 30-day group generated approximately 10.91 million in qualifying purchase revenue.

Recency provides a descriptive measure of customer activity and will inform later customer feature engineering and inactivity analysis.

### 5.5 Revenue by country

Qualifying purchase revenue was aggregated by country.

| Country | Revenue share |
|---|---:|
| United Kingdom | 83.71% |
| EIRE | 3.44% |
| Netherlands | 3.22% |
| Germany | 2.25% |
| France | 1.81% |

The United Kingdom accounted for 83.71% of total qualifying purchase revenue.

The top five countries represented approximately 94.43% of total qualifying purchase revenue.

This indicates substantial geographic concentration in the dataset.

### 5.6 Monthly revenue trends

Monthly qualifying purchase revenue was calculated alongside customer counts, invoice counts, and month-over-month revenue changes.

Key observations:

- November recorded the highest monthly revenue in both 2010 and 2011.
- November 2010 generated approximately 1.156 million.
- November 2011 generated approximately 1.136 million.
- September 2011 recorded a 47.73% increase compared with August 2011.
- December 2011 recorded a 54.93% decline compared with November 2011.

December 2011 contains transactions only through December 9. Therefore, its revenue should not be compared directly with complete calendar months without accounting for the partial observation period.

## 6. Advanced SQL Analytics

Additional queries demonstrated advanced SQL techniques.

### 6.1 Ranking and cumulative revenue

Customer revenue rankings were calculated using:

- `RANK()` for revenue-based ranking.
- `ROW_NUMBER()` for unique sequential ordering.
- `SUM() OVER()` for overall revenue.
- Ordered `SUM() OVER()` for cumulative revenue.

The top 10 customers accounted for 16.14% of total qualifying purchase revenue, while the top 20 accounted for 21.98%.

### 6.2 Conditional aggregation

Customer-level merchandise and cancellation metrics were calculated using conditional aggregation and PostgreSQL's `FILTER` clause.

The analysis distinguished:

- `merchandise_candidate`
- `merchandise_cancellation_candidate`

This allowed positive merchandise activity and cancellation activity to be examined separately.

### 6.3 Relational JOIN analysis

Separate CTEs were used to calculate purchase and cancellation metrics before combining them with a `FULL OUTER JOIN`.

The resulting analysis included:

- Purchase invoice counts.
- Qualifying purchase revenue.
- Cancellation record counts.
- Cancellation values.
- Cancellation-value-to-purchase-revenue ratios.

The ratios are descriptive comparisons, not verified product return rates, because individual cancellation records were not matched to their original purchases.

### 6.4 Window functions

The project demonstrates:

- `NTILE()` for revenue deciles.
- `RANK()` for customer ranking.
- `ROW_NUMBER()` for sequential ordering.
- `LAG()` for month-over-month comparisons.
- `SUM() OVER()` for total and cumulative aggregations.

## 7. Technical Implementation

The main Phase 4 files are:

| File | Responsibility |
|---|---|
| `sql/schema.sql` | Database schema and indexes |
| `sql/data_quality.sql` | Database integrity and reconciliation queries |
| `sql/customer_analysis.sql` | Customer-level analytical queries |
| `src/data/load.py` | Reusable PostgreSQL loading pipeline |
| `notebooks/03_database_integration.ipynb` | Database connection, integration, and execution |
| `docs/database_engineering_and_sql_analytics.md` | Phase 4 documentation |

## 8. Limitations and Considerations

The analysis is subject to the following limitations:

- The dataset does not contain explicit customer churn labels.
- Purchase frequency and recency describe observed activity within the dataset period.
- Revenue is not equivalent to profit because product costs and margins are unavailable.
- Cancellation records have not been individually matched to original purchases.
- December 2011 represents a partial observation period.
- Geographic revenue concentration does not independently establish market potential.
- The analysis is based on identified customers; anonymous transactions are excluded from customer-level analytics.

These limitations will be considered during subsequent customer segmentation, target construction, and predictive modeling.
