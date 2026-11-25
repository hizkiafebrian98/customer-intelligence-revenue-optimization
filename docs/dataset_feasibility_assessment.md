# Dataset Feasibility Assessment

**Project:** Customer Intelligence & Revenue Optimization  
**Phase:** Phase 2 — Dataset Acquisition & Feasibility Assessment  
**Status:** Completed  
**Assessment date:** November 26, 2026  
**Dataset:** UCI Online Retail II

---

## 1. Executive Summary

The UCI Online Retail II dataset has been selected for this project and successfully loaded into Jupyter Notebook using Pandas.

The dataset contains 1,067,371 transaction line items across two worksheets, covering December 1, 2009, to December 9, 2011. It provides sufficient transaction history and customer identifiers for customer behavior analysis, revenue analysis, segmentation, and the development of a purchase-inactivity prediction model.

The initial investigation identified several data-quality considerations, including missing customer identifiers, cancellation invoices, negative quantities, zero or negative prices, unusually large transactions, and non-merchandise financial entries.

The dataset is considered feasible for the project, subject to further data-quality assessment, transaction classification, cleaning, and target-definition work.

## 2. Dataset Information

| Attribute | Details |
|---|---|
| Dataset name | Online Retail II |
| Source | UCI Machine Learning Repository |
| Dataset URL | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| DOI | https://doi.org/10.24432/C5CG6D |
| Original publication year | 2012 |
| License | CC BY 4.0 |
| Business context | UK-based non-store online retailer |
| Dataset format | Excel workbook |
| Local filename | `online_retail_II.xlsx` |
| File size | Approximately 43.51 MB |
| Observation period | December 1, 2009 – December 9, 2011 |
| Total records | 1,067,371 transaction line items |

**Dataset citation:**

Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.

Attribution must be retained in project documentation in accordance with the dataset license.

## 3. Dataset Structure and Initial Inspection

The workbook contains two worksheets:

- `Year 2009-2010`
- `Year 2010-2011`

Both worksheets contain the same eight columns:

| Column | Initial data type | Description |
|---|---|---|
| Invoice | Object | Invoice identifier |
| StockCode | Object | Product or stock identifier |
| Description | Object | Product description |
| Quantity | Integer | Quantity recorded on the transaction line |
| InvoiceDate | Datetime | Transaction date and time |
| Price | Float | Price recorded for the transaction line |
| Customer ID | Float | Customer identifier |
| Country | String | Customer country |

The worksheets were successfully loaded and concatenated into a single Pandas DataFrame.

```python
df_2009_2010 = pd.read_excel(
    DATA_PATH,
    sheet_name="Year 2009-2010"
)

df_2010_2011 = pd.read_excel(
    DATA_PATH,
    sheet_name="Year 2010-2011"
)

df = pd.concat(
    [df_2009_2010, df_2010_2011],
    ignore_index=True
)
```

**Combined dataset dimensions:** 1,067,371 rows × 8 columns.

Each row represents a transaction line item, not necessarily an individual invoice or complete order. A single invoice can contain multiple product lines.

## 4. Initial Dataset Profile

### 4.1 General statistics

| Metric | Result |
|---|---:|
| Transaction line items | 1,067,371 |
| Unique invoice identifiers | 53,628 |
| Identifiable customers | 5,942 |
| Earliest transaction | 2009-12-01 07:45:00 |
| Latest transaction | 2011-12-09 12:50:00 |
| Unique observation months | 25 |

The average invoice contains approximately 19.90 transaction line items, while the median is 9. The maximum observed number of line items associated with one invoice identifier is 1,350.

### 4.2 Missing values

| Column | Missing records | Percentage |
|---|---:|---:|
| Description | 4,382 | 0.41% |
| Customer ID | 243,007 | 22.77% |
| Other columns | 0 | 0% |

Missing customer identifiers prevent reliable attribution of those records to individual customers.

**Preliminary handling decision:** Do not automatically delete records with missing Customer IDs. They may still contribute to overall transaction, product, and revenue analysis where appropriate. However, they cannot be used for customer-level analysis without a valid customer identifier.

Missing descriptions also require investigation before deciding whether records should be excluded or retained.

## 5. Transaction and Data Quality Findings

The following findings are based on initial inspection. They are not yet final cleaning rules.

### 5.1 Cancellation invoices and negative quantities

An initial check identified:

| Metric | Records |
|---|---:|
| Invoice identifiers beginning with `C` | 19,494 line items |
| Unique cancellation invoice identifiers | 8,292 |
| Negative-quantity line items | 22,950 |
| Unique invoices containing negative quantities | 11,684 |
| Negative quantities under non-cancellation invoice identifiers | 3,457 |
| Non-negative quantities under cancellation invoice identifiers | 1 |

These results show that cancellation invoice identifiers and negative quantities are related but not interchangeable classifications.

**Preliminary decision:** Investigate and maintain separate indicators for cancellation invoice identifiers and negative quantities. Do not assume that every negative quantity is a cancellation or that every cancellation invoice follows the same transaction pattern.

### 5.2 Quantity anomalies

| Statistic | Quantity |
|---|---:|
| Mean | 9.94 |
| Standard deviation | 172.71 |
| Minimum | -80,995 |
| Median | 3 |
| Maximum | 80,995 |

Some unusually large quantities appear in matching positive and negative transaction pairs.

Examples include:

- Customer `12346`: 74,215 units recorded on an invoice and -74,215 units on a cancellation invoice two minutes later.
- Customer `16446`: 80,995 units recorded on an invoice and -80,995 units on a cancellation invoice twelve minutes later.

Other high-quantity records include large quantities of products priced at relatively low unit prices, which may reflect wholesale purchasing behavior.

**Preliminary decision:** Do not remove extreme quantities solely because they are statistically unusual. Investigate their transaction context and retain legitimate wholesale transactions where appropriate.

### 5.3 Price anomalies

| Statistic | Price |
|---|---:|
| Mean | 4.65 |
| Standard deviation | 123.55 |
| Minimum | -53,594.36 |
| Median | 2.10 |
| Maximum | 38,970.00 |
| Zero-price records | 6,202 |
| Negative-price records | 5 |

The five negative-price records all have:

- StockCode: `B`
- Description: `Adjust bad debt`
- Missing Customer ID
- Country: United Kingdom

These are accounting adjustments rather than ordinary merchandise sales.

The initial inspection also identified high-value entries associated with descriptions such as `AMAZON FEE`, `BANK CHARGES`, and `Manual`.

Zero-price records include descriptions such as `short`, `lost`, `damages`, and other operational notes. They should not automatically be interpreted as free merchandise or invalid transactions.

**Preliminary decision:** Separate ordinary merchandise transactions from accounting and administrative entries before calculating customer revenue or constructing purchase features.

### 5.4 Negative quantities under non-cancellation invoices

A targeted investigation checked negative quantities under invoice identifiers that do not begin with `C`, with positive prices.

Result:

- Records found: 0
- Unique invoices: 0

This indicates that the 3,457 negative-quantity records under non-cancellation invoice identifiers have non-positive prices. Most may represent zero-price operational adjustments, but this interpretation requires further verification.

## 6. Monthly Data Coverage

The dataset contains 25 consecutive calendar months, from December 2009 through December 2011. No completely missing calendar month was identified.

November has the highest recorded activity in both years:

| Month | Transaction line items | Unique invoices | Identifiable customers |
|---|---:|---:|---:|
| November 2010 | 78,015 | 3,669 | 1,683 |
| November 2011 | 84,711 | 3,462 | 1,711 |

This may indicate seasonal activity, but further analysis is required before drawing conclusions about seasonality or its causes.

**Important limitation:** December 2011 is incomplete because the dataset ends on December 9. Its monthly totals should not be compared directly with full calendar months.

Monthly counts from this initial investigation include all recorded line items, including cancellations and operational or non-merchandise entries. They are not yet counts of qualifying purchases.

## 7. Customer Observation Coverage

The dataset contains 5,942 customers with identifiable Customer IDs.

| Metric | Result |
|---|---:|
| Mean recorded line items per customer | 138.74 |
| Median recorded line items per customer | 53 |
| Maximum recorded line items per customer | 13,097 |
| Mean unique invoices per customer | 7.55 |
| Median unique invoices per customer | 4 |
| Maximum unique invoices per customer | 510 |

Customer activity is highly uneven. The mean number of line items is considerably higher than the median, suggesting that a relatively small number of customers have substantially larger recorded transaction histories.

Customers also have different first and last recorded activity dates. These dates represent the customer's presence in the available dataset, not necessarily their actual acquisition date or confirmed churn date.

## 8. Preliminary Prediction Window Feasibility

The project intends to investigate whether historical customer behavior can predict future purchase inactivity.

A preliminary target concept is:

> A customer is classified as purchase-inactive if they make no qualifying purchase during the 90-day period following a defined prediction snapshot.

This is a behavioral inactivity definition, not proof of permanent customer churn.

### 8.1 Candidate snapshot

The dataset's final transaction timestamp is December 9, 2011, at 12:50:00.

To ensure a complete 90-calendar-day future observation window, September 9, 2011, was selected as a conservative candidate snapshot.

| Component | Date |
|---|---|
| Prediction snapshot | September 9, 2011, 23:59:59 |
| Observation window starts | September 10, 2011 |
| Observation window ends | December 8, 2011, 23:59:59 |
| Dataset end | December 9, 2011, 12:50:00 |
| Complete observation window | Yes |

The 90-day observation window is fully covered by the dataset.

### 8.2 Customer coverage at the September 10 boundary

Using September 10, 2011, as the preliminary boundary for the initial customer coverage check:

| Measure | Customers |
|---|---:|
| Total identifiable customers | 5,942 |
| First observed by the boundary | 5,346 |
| First observed after the boundary | 596 |
| Last recorded activity by the boundary | 3,024 |
| Recorded activity after the boundary | 2,918 |

Of the 5,346 customers already observed by the boundary, 2,322 also have recorded activity afterward.

These are raw recorded-activity counts. They must not be interpreted as confirmed active or inactive customer labels because the transaction records have not yet been classified into qualifying purchases.

Customers first observed after the prediction snapshot cannot be included in a model as if their customer histories were available at that snapshot.

### 8.3 Target-definition limitations

The following decisions remain open:

1. Define which transaction records qualify as actual purchases.
2. Define customer eligibility based on available historical purchase information.
3. Finalize the inactivity-label construction and observation-window convention.
4. Prevent data leakage by ensuring all model features use information available at or before the prediction snapshot.
5. Consider whether a 180-day inactivity definition should be examined as a sensitivity analysis, subject to data coverage and methodology.

## 9. Known Dataset Limitations

The dataset does not contain:

- Subscription status or explicit customer cancellation labels.
- Marketing campaign exposure or campaign costs.
- Product acquisition costs or profit margins.
- Customer acquisition costs.
- Customer demographic attributes.

Consequently:

- The project must not claim to predict subscription cancellations.
- The predictive target must be framed as future purchase inactivity.
- Revenue must not be described as profit.
- Customer lifetime value estimates must disclose their assumptions.
- Retention ROI cannot be calculated reliably without cost and margin information.
- Revenue-at-risk estimates must be clearly qualified as historical revenue associated with customers meeting a defined risk criterion, not guaranteed future losses.

## 10. Phase 2 Technical Decisions

| Area | Decision |
|---|---|
| Dataset | Use UCI Online Retail II |
| Workbook handling | Load both worksheets with Pandas and concatenate them |
| Raw data preservation | Keep the original Excel workbook unchanged |
| Missing customer identifiers | Do not automatically delete |
| Cancellation records | Investigate separately from ordinary transactions |
| Negative quantities | Investigate transaction context before exclusion |
| Extreme quantities | Do not remove solely based on magnitude |
| Zero and negative prices | Investigate and classify before revenue calculations |
| Accounting and administrative entries | Separate from ordinary merchandise sales |
| Prediction target | Future purchase inactivity, provisionally 90 days |
| Candidate snapshot | September 9, 2011, subject to final methodology |
| Main development environment | Jupyter Notebook |
| Data processing | Python and Pandas |
| Database | PostgreSQL, introduced in Phase 4 |

No permanent cleaning rules or transformed production dataset have been finalized during Phase 2.
