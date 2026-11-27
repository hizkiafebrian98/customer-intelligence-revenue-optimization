# Feature Engineering & Target Construction

## 1. Objective and Prediction Problem

The objective of Phase 7 is to transform historical retail transactions into a supervised learning dataset for predicting customer repeat-purchase behavior.

The prediction problem is defined as:

**Predict whether an existing customer will make at least one qualifying purchase within the next 90 days.**

This is a repeat-purchase propensity problem, not a permanent customer churn prediction problem.

### Prediction Design

| Component | Definition |
|---|---|
| Prediction unit | Customer at a monthly observation date |
| Eligible population | Customers with at least one qualifying purchase in the preceding 180 days |
| Feature window | 180 days before the observation date |
| Prediction window | 90 days starting from the observation date |
| Positive target | At least one qualifying purchase during the next 90 days |
| Negative target | No qualifying purchase during the next 90 days |
| Snapshot frequency | Monthly |

Only qualifying purchases are used to establish eligibility and target outcomes. Cancellations, zero-price activity, operational adjustments, and other non-purchase transactions are not counted as purchases.

Customers without a qualifying purchase in the preceding 180 days are excluded from the eligible population at that particular snapshot.

## 2. Temporal Dataset Construction

### Observation Period

The cleaned dataset contains qualifying purchase transactions from December 1, 2009, through December 9, 2011.

To ensure that every observation has a complete historical feature window and a complete future outcome window, monthly snapshots were constructed from:

- First snapshot: June 1, 2010
- Last snapshot: September 1, 2011
- Total snapshots: 16

Each snapshot uses the following temporal boundaries:

- Feature window: `[snapshot_date - 180 days, snapshot_date)`
- Target window: `[snapshot_date, snapshot_date + 90 days)`

The half-open intervals ensure that transactions on the snapshot date are excluded from historical features and included in the future outcome window.

### Population and Coverage

| Metric | Result |
|---|---:|
| Monthly snapshots | 16 |
| Customer-snapshot observations | 47,933 |
| Distinct customers across snapshots | 5,212 |
| Qualifying purchase records in source data | 776,504 |
| Customers with qualifying purchases in source data | 5,852 |

The 5,212 distinct customers represent customers eligible in at least one of the 16 snapshot periods. This is narrower than the full population of 5,852 customers identified in Phase 6.

Customers may appear in multiple snapshots. Each appearance represents a separate customer-period observation with its own historical features and future target.

## 3. Feature Engineering

Customer-level features were calculated independently for each snapshot using only qualifying purchases within the preceding 180 days.

### 3.1 Purchasing Behavior Features

The initial feature construction included:

| Feature | Definition |
|---|---|
| `recency_days` | Days between the snapshot date and the customer's most recent qualifying purchase |
| `frequency` | Number of distinct analytical purchase invoices |
| `monetary` | Total qualifying purchase revenue within the feature window |
| `purchase_line_count` | Number of qualifying purchase transaction lines |
| `unique_products` | Number of distinct products purchased |
| `customer_history_days` | Days between the first and most recent qualifying purchase within the feature window |
| `avg_invoice_value` | Historical monetary value divided by distinct purchase invoices |

Analytical invoice groups were reconstructed using the same grouping definition established in earlier phases:

- Invoice
- InvoiceDate
- Customer ID
- Country

Frequency therefore represents distinct analytical invoice groups rather than raw transaction-row counts.

### 3.2 Cancellation Behavior Features

Cancellation activity was incorporated separately from purchase behavior.

Three historical cancellation features were constructed within the same 180-day feature window:

| Feature | Definition |
|---|---|
| `cancellation_line_count` | Number of merchandise cancellation transaction lines |
| `cancellation_invoice_count` | Number of distinct cancellation invoices |
| `cancellation_value` | Absolute value of the summed negative merchandise cancellation revenue |

Customers without cancellation activity received zero values.

Cancellation features were not subtracted from monetary value. Earlier analysis identified cases where cancellation records could not be confidently matched to original purchases. Treating gross purchase revenue as net revenue would therefore introduce unsupported assumptions.

The cancellation features provide supplementary behavioral information, not a confirmed measure of customer dissatisfaction or lost revenue.

### 3.3 Distribution Analysis and Transformations

Several engineered features exhibited substantial right skewness.

| Feature | Original skewness | Skewness after `log1p` |
|---|---:|---:|
| Frequency | 8.99 | 1.55 |
| Monetary | 18.18 | 0.35 |
| Purchase line count | 10.99 | -0.08 |
| Unique products | 6.20 | -0.28 |
| Average invoice value | 57.39 | -0.04 |
| Cancellation line count | 8.96 | 1.87 |
| Cancellation invoice count | 5.92 | 1.63 |
| Cancellation value | 70.78 | 1.39 |

The `log1p(x)` transformation, equivalent to `log(1 + x)`, was applied to non-negative, right-skewed features.

The transformation reduced the influence of extreme values while preserving zero observations.

Recency and customer history duration were retained in their original scales because their distributions were comparatively moderate.

No legitimate extreme observations were removed or capped.

### 3.4 Extreme Value Investigation

Extreme customer observations were investigated before finalizing the baseline feature set.

Customers 18102 and 14646 repeatedly appeared among the highest historical monetary values. Their high purchase values were accompanied by substantial purchasing frequency, transaction lines, and product variety.

These observations were retained as potentially meaningful high-value customer behavior.

Customer 12346 had a historical monetary value of £77,183.60 associated with a single purchase invoice. Phase 5 had previously identified a full cancellation of this purchase 16 minutes later.

This illustrates an important limitation of gross qualifying purchase revenue: it does not automatically reflect the economic value retained after cancellations.

The observation was preserved, and cancellation behavior was represented separately.

## 4. Target Construction

The target variable is:

`repeat_purchase_90d`

Its definition is:

- `1`: the customer makes at least one qualifying purchase during the 90-day target window.
- `0`: the customer makes no qualifying purchase during the 90-day target window.

The target was constructed by identifying customers with qualifying purchases during each snapshot's future window and matching them against the eligible customers in that snapshot.

### Target Distribution

| Target | Observations | Share |
|---|---:|---:|
| No purchase (0) | 24,400 | 50.90% |
| Repeat purchase (1) | 23,533 | 49.10% |
| **Total** | **47,933** | **100.00%** |

The overall target distribution is relatively balanced.

Monthly positive rates varied between 37.73% and 62.01%, indicating temporal variation in repeat-purchase behavior.

The target construction was independently reconciled against the preliminary snapshot audit. All 16 snapshot-level eligible, positive, and negative customer counts matched exactly.

## 5. Baseline Feature Selection

Spearman correlation was used to investigate monotonic relationships among engineered features and the target.

Several feature pairs exhibited strong correlations:

| Feature Pair | Spearman Correlation |
|---|---:|
| Purchase line count and unique products | 0.987 |
| Cancellation line count and cancellation invoice count | 0.988 |
| Cancellation line count and cancellation value | 0.983 |
| Cancellation invoice count and cancellation value | 0.979 |
| Customer history days and frequency | 0.914 |
| Monetary and average invoice value | 0.725 |

The strongest individual associations with the target included:

| Feature | Spearman Correlation with Target |
|---|---:|
| Log frequency | 0.390 |
| Customer history days | 0.380 |
| Log monetary | 0.369 |
| Log purchase line count | 0.320 |
| Log unique products | 0.289 |
| Recency days | -0.272 |

These correlations are descriptive and do not establish causal relationships or predictive performance.

### Selected Baseline Features

Five features were selected for the initial modeling baseline:

| Feature | Purpose |
|---|---|
| `recency_days` | Captures purchase recency |
| `log1p_frequency` | Captures repeat-purchase frequency |
| `log1p_monetary` | Captures historical purchase value |
| `log1p_unique_products` | Captures product variety |
| `log1p_cancellation_value` | Captures historical cancellation magnitude |

Other engineered features were excluded from the initial baseline because of redundancy or derived relationships:

- `customer_history_days`: strongly correlated with frequency within the observation window.
- `log1p_purchase_line_count`: highly correlated with unique product count.
- `log1p_cancellation_line_count` and `log1p_cancellation_invoice_count`: highly correlated with cancellation value.
- `log1p_avg_invoice_value`: derived from monetary value divided by frequency.

These exclusions are baseline modeling decisions, not claims that the variables have no predictive value. Alternative feature sets can be evaluated in Phase 8.

The resulting baseline dataset contains 47,933 observations, five features, customer identifiers, snapshot dates, and the target.

## 6. Temporal Train, Validation, and Test Design

Random row-level splitting was avoided because monthly customer snapshots have overlapping historical and future windows.

A chronological split was designed with temporal embargo periods to prevent target-window overlap across the modeling partitions.

### Partition Definitions

| Partition | Snapshot Period | Observations | Distinct Customers | Positive Rate |
|---|---|---:|---:|---:|
| Training | June–November 2010 | 17,119 | 3,893 | 54.51% |
| Validation | February–April 2011 | 9,985 | 3,745 | 41.96% |
| Test | August–September 2011 | 5,534 | 2,968 | 58.19% |
| Embargo | December 2010–July 2011 | 15,295 | 4,435 | 44.40% |
| **Total** | | **47,933** | | |

Distinct customer counts are calculated independently for each partition and therefore are not additive.

### Temporal Boundaries

| Partition | Last Snapshot | Last Target Window Date |
|---|---|---|
| Training | November 1, 2010 | January 30, 2011 |
| Validation | April 1, 2011 | June 30, 2011 |
| Test | September 1, 2011 | November 30, 2011 |

The training outcome window ends before validation begins. The validation outcome window ends before testing begins.

The test outcome window ends November 30, 2011, within the available dataset period. The final qualifying purchase date is December 9, 2011.

### Embargo Strategy

Two temporal gaps were retained:

- December 2010–January 2011 between training and validation.
- May–July 2011 between validation and test.

These observations remain in the saved dataset and are labeled `embargo`. They are excluded from the three selected modeling partitions.

The embargo observations are retained for auditability and future analysis, not treated as missing data.

### Customer Overlap

The same customer can appear in multiple partitions. This is intentional because the prediction objective concerns future purchasing behavior among existing customers.

Consequently, the evaluation measures future-period performance for a population that can include customers observed during training. It does not establish generalization to entirely unseen customers.

Customer-snapshot observations within a partition also have overlapping historical and target windows. The temporal embargo specifically prevents target-window overlap across the three selected partitions.

## 7. Validation and Limitations

### Validation Results

The following validation stages were completed:

| Validation Stage | Checks Passed |
|---|---:|
| Initial feature integrity | 7 / 7 |
| Historical cancellation features | 6 / 6 |
| Final temporal leakage audit | 11 / 11 |

The final audit confirmed:

- All historical feature transactions precede their snapshot dates.
- Feature windows begin at the defined 180-day boundary.
- Recency values are non-negative.
- Baseline features and target have no missing values.
- Customer-snapshot observations are unique.
- Training target windows end before validation begins.
- Validation target windows end before testing begins.
- The test target window is covered by available data.
- All partition labels are valid.
- The saved dataset retains all original observations.
- Saved partition assignments match the intended definitions.

The saved dataset was read back from Parquet and reconciled to the original 47,933 observations.

### Limitations

1. **Historical dataset coverage:** The analysis uses a historical dataset ending December 9, 2011. Results cannot establish performance on contemporary retail behavior.

2. **Temporal variation:** Positive target rates differ across training, validation, and test periods. Seasonality and changes in purchasing behavior may affect model performance.

3. **Gross purchase value:** Monetary features represent gross qualifying purchase revenue and do not subtract cancellation activity.

4. **Cancellation matching:** Cancellation records cannot always be matched confidently to their original purchases. Cancellation value should not be interpreted as a verified return or loss amount.

5. **Repeated customers:** Customers may appear in multiple temporal partitions. The evaluation therefore focuses on future observations for an existing-customer population, not entirely new customers.

6. **Eligible population:** Customers without a qualifying purchase during the preceding 180 days are excluded at a given snapshot. The model does not directly predict reactivation among customers already inactive beyond this period.

7. **No predictive performance established:** Phase 7 constructs and validates the supervised learning dataset. Predictive performance, model calibration, feature importance, and business utility will be assessed in subsequent phases.

## 8. Artifacts and Next Phase

### Created Artifacts

| Artifact | Path |
|---|---|
| Phase 7 notebook | `notebooks/06_feature_engineering_and_target_construction.ipynb` |
| Modeling dataset | `data/processed/customer_purchase_propensity_dataset.parquet` |
| Temporal partition summary | `data/processed/temporal_partition_summary.csv` |
| Technical documentation | `docs/feature_engineering_and_target_construction.md` |

The processed dataset and partition summary are generated outputs and are excluded from GitHub by the project's data-handling rules. They can be reproduced by running the notebook.

### Phase 7 Outcome

Phase 7 established a reproducible customer-period modeling dataset with:

- A clearly defined repeat-purchase propensity objective.
- Monthly customer snapshots and historical behavioral features.
- Separate historical cancellation features.
- A validated 90-day target.
- A five-feature baseline.
- Chronological training, validation, and test partitions.
- Temporal embargo periods and leakage safeguards.
- Reconciled and documented output artifacts.

### Next Phase: Phase 8 — Predictive Model Development

Phase 8 will use the frozen temporal partitions to develop and compare predictive models.

The next stage will include baseline model development, model comparison, preprocessing, hyperparameter tuning, and validation-based model selection.

No predictive performance claims are made at the conclusion of Phase 7.