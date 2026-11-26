# Data Cleaning and ETL Methodology

## 1. Overview

This document describes the data cleaning methodology and reusable ETL pipeline developed for the Customer Intelligence & Revenue Optimization project.

The pipeline processes the UCI Online Retail II dataset, applies documented data quality decisions, classifies transaction records, and produces validated analytical datasets for downstream database engineering and customer analytics.

The implementation uses Python and Pandas, with separate modules for extraction, transformation, and validation.

## 2. Source Data

**Dataset:** UCI Online Retail II  
**Source:** https://archive.ics.uci.edu/dataset/502/online+retail+ii

The original workbook contains two sheets covering December 2009 to December 2011.

| Attribute | Value |
|---|---|
| Original records | 1,067,371 |
| Original columns | 8 |
| Source sheets | 2 |
| Period covered | December 2009 – December 2011 |

The original columns are preserved during extraction:

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

## 3. Data Quality Assessment and Cleaning Decisions

Cleaning decisions were based on investigation findings rather than automatic removal of unusual records.

### 3.1 Missing Values

**Customer ID**

- 243,007 records had missing Customer IDs.
- No Customer ID imputation was performed.
- Anonymous transactions were retained for transaction-level and appropriate aggregate analysis.
- Records without reliable customer identification were excluded from customer-level analysis requiring a known customer.

**Description**

- 4,382 records originally had missing descriptions.
- An approved mapping was constructed using StockCode and consistent known descriptions.
- A minimum evidence threshold of five known records per StockCode was applied.
- 2,740 missing descriptions were recovered before duplicate exclusion.
- 2,653 recovered descriptions remained in the final cleaned dataset.
- The original missing-description status was retained through an indicator column.

### 3.2 Duplicate Records

A total of 34,335 excess exact duplicate records were identified using all eight original source columns.

The primary analytical dataset excludes excess exact duplicates using a first-occurrence retention policy.

The original records remain preserved in the raw source, while excluded records are retained separately in the duplicate audit dataset.

The investigation identified an unusually high concentration of duplicates in December 2010. The exact underlying cause was not conclusively established.

### 3.3 Transaction Anomalies

Unusual transaction records were investigated and classified rather than indiscriminately deleted.

Key decisions included:

- Cancellation records were retained and identified using cancellation invoice identifiers.
- Negative quantities outside cancellation invoices were preserved and excluded from customer-level purchasing analysis.
- Negative-price bad-debt adjustments were separated from merchandise revenue.
- Zero-price activity was retained but distinguished from qualifying paid purchases.
- Extreme quantities were investigated for possible wholesale transactions, cancellation relationships, and operational adjustments.
- Delivery charges, packing charges, discounts, financial adjustments, platform fees, bank charges, samples, and test transactions were separated from ordinary merchandise purchases.

These decisions preserve transaction information while establishing explicit rules for downstream analytical use.

## 4. Transaction Classification

The pipeline applies a documented transaction taxonomy containing 16 categories.

The classification distinguishes:

- Merchandise revenue records
- Anonymous merchandise transactions
- Merchandise cancellations
- Delivery and packing charges
- Zero-price activity
- Operational adjustments
- Manual transactions
- Discounts and financial adjustments
- Bank charges and platform fees
- Bad-debt adjustments
- Samples and test transactions

Each category has defined revenue treatment, customer-level eligibility, and qualifying-purchase status.

The taxonomy is maintained separately in:

`data/reference/transaction_taxonomy.csv`

This separation makes classification rules more transparent and maintainable.

## 5. Analytical Definitions

The pipeline derives several fields used by downstream analysis.

**Line value**

Quantity multiplied by unit price.

**Merchandise revenue**

Includes classified positive and negative merchandise revenue records, including identified merchandise cancellations.

**Qualifying purchase**

A positive-quantity, positive-price merchandise transaction associated with an identified customer and classified as eligible for customer purchasing analysis.

**Customer analytics eligibility**

Indicates whether a transaction is eligible for customer-level analysis and has a known Customer ID.

These definitions distinguish merchandise revenue, recorded activity, and qualifying paid purchases. They are important for avoiding incorrect customer activity and inactivity calculations.

## 6. Reusable ETL Architecture

The implementation is organized into three modules.

| Module | Responsibility |
|---|---|
| `src/data/extract.py` | Extracts and combines both source workbook sheets |
| `src/data/transform.py` | Applies cleaning, standardization, classification, and duplicate handling |
| `src/data/validate.py` | Validates schemas, record reconciliation, transformations, and analytical rules |

### Extraction

The extraction module:

1. Reads both workbook sheets.
2. Checks that all required source columns exist.
3. Preserves the expected column order.
4. Combines the sheets into one DataFrame.

### Transformation

The transformation module:

1. Loads the approved description mapping and transaction taxonomy.
2. Derives standardized fields and analytical indicators.
3. Applies description recovery rules.
4. Classifies transaction records.
5. Calculates transaction values and revenue measures.
6. Identifies excess exact duplicates.
7. Produces the cleaned analytical dataset and duplicate audit dataset.

### Validation

The validation module checks:

- Required source columns and expected schemas.
- Record counts and reconciliation.
- Duplicate identification and original row positions.
- Preservation of original source fields.
- Description imputation consistency.
- Transaction classification and taxonomy consistency.
- Customer analytics eligibility.
- Qualifying purchase eligibility.
- Line value and revenue calculations.

The validation implementation contains 29 checks.

## 7. Final Dataset Outputs

The completed pipeline produces three principal DataFrames:

| Output | Dimensions | Purpose |
|---|---:|---|
| Classified dataset | 1,067,371 × 32 | Full classified dataset before duplicate exclusion |
| Cleaned analytical dataset | 1,033,036 × 33 | Primary dataset for downstream analysis |
| Duplicate audit dataset | 34,335 × 33 | Records excluded under the exact duplicate policy |

The cleaned analytical dataset and duplicate audit dataset reconcile to the original record count:

1,033,036 + 34,335 = 1,067,371.

The final cleaned dataset contains no remaining exact duplicate records under the eight-column source definition.

## 8. Exported Artifacts

The pipeline outputs are stored in the project repository as follows:

**Processed datasets**
- `data/processed/online_retail_clean.csv`
- `data/processed/online_retail_clean.parquet`
- `data/processed/duplicate_audit.csv`

**Reference data**
- `data/reference/description_mapping.csv`
- `data/reference/transaction_taxonomy.csv`

The Parquet export was read back successfully, preserving the expected record count and column structure.

Raw and processed datasets are maintained separately from source code and documentation. Large data files should not be committed to GitHub unless their inclusion is explicitly justified.

## 9. Validation Results

The reusable ETL pipeline was tested against the original notebook outputs.

Results:

- Extraction reproduced the original 1,067,371 × 8 source dataset.
- Transformation reproduced the original classified, cleaned, and duplicate audit datasets.
- All 32 classified columns matched the notebook results.
- All 33 cleaned dataset columns matched the notebook results.
- All 33 duplicate audit columns matched the notebook results.
- Values and data types matched across the compared outputs.
- All 29 validation checks passed.

These results establish that the reusable pipeline reproduces the documented cleaning and classification workflow.

## 10. Limitations and Analytical Considerations

The cleaning process does not establish that every unusual transaction has a known business explanation.

In particular:

- Some anonymous transactions cannot be attributed to individual customers.
- Some operational adjustments have uncertain underlying causes.
- The duplicate investigation identified a significant December 2010 anomaly, but its cause remains unconfirmed.
- Merchandise revenue is not equivalent to profit.
- Customer inactivity must be defined using qualifying paid purchases rather than all recorded transaction activity.
- Future inactivity labels must account for the observation window and dataset coverage.

These limitations must be considered in subsequent customer analytics and predictive modeling.