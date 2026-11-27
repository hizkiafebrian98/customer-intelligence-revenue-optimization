# Customer Intelligence & Revenue Optimization

An applied data science project focused on understanding retail customer purchasing behavior, identifying customers with lower repeat-purchase propensity, and supporting data-driven retention prioritization.

## Project Overview

Retail businesses generate large volumes of transaction data, but transaction records alone do not provide a complete understanding of customer behavior.

This project develops a customer intelligence solution using historical retail transactions to investigate:

- Which customers generate the most revenue?
- Which customers exhibit signs of purchasing inactivity?
- What purchasing behaviors are associated with customer inactivity?
- Can future repeat-purchase behavior be predicted using historical purchasing behavior?
- Which customer characteristics contribute most to predictive outcomes?
- How is historical purchase value distributed among customers with different repeat-purchase outcomes?
- Which customer segments should receive retention attention first?

The project combines data engineering, exploratory data analysis, customer analytics, statistical methods, machine learning, and business-oriented prioritization into an end-to-end analytical workflow.

## Dataset

**UCI Online Retail II**

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- Citation: Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.
- License: CC BY 4.0
- Original records: 1,067,371 transaction line items
- Original columns: 8
- Period: December 2009 – December 2011

The dataset contains transaction records from a UK-based, non-store online retailer.

The original workbook is not included in this repository. Download it from the official UCI source and place it in `data/raw/`.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data manipulation | Pandas, NumPy |
| Data extraction | Excel, OpenPyXL |
| Database engineering | PostgreSQL, SQLAlchemy, Psycopg |
| Statistical analysis | Python statistical libraries |
| Visualization | Matplotlib, Seaborn |
| Machine learning | Scikit-learn |
| Model explainability | Logistic Regression coefficients, odds ratios |
| Application | Streamlit |
| Version control | Git, GitHub |

Some technologies are planned for later phases and have not yet been implemented.

## Project Structure

```text
customer-intelligence-revenue-optimization/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_assessment.ipynb
│   ├── 03_database_integration.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_customer_analytics_and_segmentation.ipynb
│   ├── 06_feature_engineering_and_target_construction.ipynb
│   ├── 07_predictive_model_development.ipynb
│   ├── 08_model_evaluation_and_explainability.ipynb
│   └── 09_business_impact_and_retention_prioritization.ipynb
├── sql/
│   ├── schema.sql
│   ├── data_quality.sql
│   └── customer_analysis.sql
├── src/
│   └── data/
│       ├── extract.py
│       ├── transform.py
│       ├── validate.py
│       └── load.py
├── app/
├── tests/
├── reports/
├── docs/
│   ├── dataset_feasibility_assessment.md
│   ├── data_cleaning_and_etl.md
│   ├── database_engineering_and_sql_analytics.md
│   ├── exploratory_data_analysis.md
│   ├── customer_analytics_and_segmentation.md
│   ├── feature_engineering_and_target_construction.md
│   ├── predictive_model_development.md
│   ├── model_evaluation_and_explainability.md
│   └── business_impact_and_retention_prioritization.md
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Development Progress

### Phase 1 — Business Understanding & Problem Formulation

**Status: Completed**

Defined the business context, management questions, analytical objectives, and project scope.

### Phase 2 — Dataset Acquisition & Feasibility Assessment

**Status: Completed**

Selected and assessed the UCI Online Retail II dataset, including its structure, coverage, data quality characteristics, and analytical limitations.

Documentation: `docs/dataset_feasibility_assessment.md`

### Phase 3 — Data Quality Assessment, Cleaning & ETL Preparation

**Status: Completed**

Key accomplishments:

- Assessed missing values, duplicate records, transaction anomalies, and unusual quantities and prices.
- Investigated and documented data cleaning decisions.
- Developed a 16-category transaction classification taxonomy.
- Created an approved product-description mapping for selected missing descriptions.
- Excluded 34,335 excess exact duplicate records from the primary analytical dataset while preserving them in a separate audit dataset.
- Produced a cleaned analytical dataset containing 1,033,036 records and 33 columns.
- Implemented reusable extraction, transformation, and validation modules.
- Reproduced the notebook transformation results exactly.
- Passed all 29 automated data validation checks.

The reusable ETL modules are located in `src/data/`.

Documentation: `docs/data_cleaning_and_etl.md`

### Phase 4 — Database Engineering & SQL Analytics

**Status: Completed**

Key accomplishments:

- Designed and implemented a PostgreSQL relational database.
- Loaded the cleaned transaction dataset and supporting reference tables.
- Implemented primary-key and referential integrity checks.
- Reconciled source and database record counts and financial measures.
- Developed SQL queries using joins, common table expressions, window functions, and conditional aggregation.
- Investigated customer revenue contribution, purchase frequency, revenue concentration, recency, country performance, and cancellation-related patterns.

The database contains four tables:

- `retail_transactions`
- `duplicate_transaction_audit`
- `transaction_taxonomy`
- `description_mapping`

Documentation: `docs/database_engineering_and_sql_analytics.md`

### Phase 5 — Exploratory Data Analysis

**Status: Completed**

Key accomplishments:

- Examined dataset structure, missing values, and numerical and categorical distributions.
- Investigated quantity, price, and transaction-value relationships.
- Analyzed monthly, weekday, and hourly transaction patterns.
- Examined product performance, revenue concentration, and geographic differences.
- Investigated extreme transactions, unusual prices, repeated invoice identifiers, and cancellation patterns.
- Conducted purchase-to-cancellation candidate matching while documenting the limitations of source-level linkage.
- Developed evidence-based findings and analytical limitations to inform subsequent customer analytics.

Documentation: `docs/exploratory_data_analysis.md`

### Phase 6 — Customer Analytics & Segmentation

**Status: Completed**

Constructed a customer-level analytical dataset containing 5,852 identified customers with at least one qualifying purchase.

Key accomplishments:

- Defined customer-level analytical metrics, including Recency, Frequency, and Monetary value (RFM).
- Analyzed customer purchasing behavior, frequency distributions, and revenue concentration.
- Examined customer cancellation activity separately from qualifying purchases.
- Developed six rule-based RFM segments:
  - Champions
  - Loyal customers
  - Recent high-value
  - At-risk valuable
  - Hibernating
  - Other customers
- Applied K-Means clustering using transformed purchasing frequency and monetary values, alongside recency.
- Evaluated candidate cluster counts using inertia and silhouette scores.
- Selected a four-cluster solution based on a practical balance between cluster separation and business interpretability.
- Compared RFM and K-Means segmentation results using Adjusted Rand Index and Normalized Mutual Information.
- Developed segment profiles and preliminary retention prioritization recommendations.

**Selected findings:**

- The top 10% of customers contributed 63.90% of qualifying purchase revenue.
- Customers with nine or more purchase invoices contributed 69.84% of qualifying purchase revenue.
- RFM Champions represented 21.43% of customers and contributed 67.71% of qualifying purchase revenue.
- The highest-value K-Means cluster represented 15.99% of customers and contributed 70.83% of qualifying purchase revenue.
- RFM and K-Means produced partially overlapping but distinct customer groupings.

Cancellation activity was examined as supplementary customer behavior. Cancellation-to-purchase-value ratios are descriptive indicators and should not be interpreted as verified return rates.

**Key outputs:**

- `notebooks/05_customer_analytics_and_segmentation.ipynb`
- `data/processed/customer_analytics.parquet`
- `data/processed/rfm_segment_profile.csv`
- `data/processed/kmeans_cluster_profile.csv`
- `data/processed/rfm_cancellation_concentration.csv`
- `data/processed/top_cancellation_customers_by_rfm.csv`

Documentation: `docs/customer_analytics_and_segmentation.md`

### Phase 7 — Feature Engineering & Target Construction

**Status: Completed**

Transformed historical transaction data into a supervised learning dataset for predicting customer repeat-purchase behavior.

The prediction objective is to estimate whether an existing customer will make at least one qualifying purchase within the next 90 days, based on purchasing behavior during the preceding 180 days.

Key accomplishments:

- Defined the prediction unit, eligible customer population, historical feature window, and future target window.
- Generated 16 monthly customer snapshots covering June 2010 through September 2011.
- Constructed 47,933 customer-snapshot observations representing 5,212 distinct customers.
- Engineered historical purchasing features, including recency, frequency, monetary value, purchase-line count, product variety, and average invoice value.
- Engineered separate historical cancellation features to capture cancellation activity without automatically subtracting cancellations from gross purchase revenue.
- Investigated extreme customer observations and preserved legitimate high-value purchasing behavior.
- Applied `log1p` transformations to strongly right-skewed features.
- Examined Spearman correlations to identify redundant features and establish an initial five-feature baseline.
- Constructed the binary target `repeat_purchase_90d`, representing whether a qualifying purchase occurred during the subsequent 90-day period.
- Reconciled target counts against the preliminary snapshot audit across all 16 snapshots.
- Designed chronological training, validation, and test partitions with temporal embargo periods to prevent target-window overlap across partitions.
- Completed feature integrity, cancellation feature, and temporal leakage validation checks.
- Saved the complete modeling dataset and temporal partition summary.

**Selected findings:**

- The modeling dataset contains 47,933 customer-snapshot observations and 5,212 distinct customers.
- The target contains 23,533 positive observations (49.10%) and 24,400 negative observations (50.90%).
- The initial baseline uses five features: `recency_days`, `log1p_frequency`, `log1p_monetary`, `log1p_unique_products`, and `log1p_cancellation_value`.
- The training partition contains 17,119 observations, the validation partition 9,985, and the test partition 5,534.
- An additional 15,295 observations are retained in temporal embargo periods and excluded from the selected modeling partitions.
- All 16 snapshot-level target reconciliations matched, and all 24 feature, cancellation, and final leakage validation checks passed.

**Temporal partition design:**

| Partition | Snapshot Period | Observations | Positive Rate |
|---|---|---:|---:|
| Training | June–November 2010 | 17,119 | 54.51% |
| Validation | February–April 2011 | 9,985 | 41.96% |
| Test | August–September 2011 | 5,534 | 58.19% |
| Embargo | December 2010–July 2011 | 15,295 | 44.40% |

Customer observations may overlap across partitions because the prediction objective concerns future purchasing behavior among existing customers. Temporal embargo periods prevent target-window overlap between the selected modeling partitions.

**Key outputs:**

- `notebooks/06_feature_engineering_and_target_construction.ipynb`
- `data/processed/customer_purchase_propensity_dataset.parquet`
- `data/processed/temporal_partition_summary.csv`

Documentation: `docs/feature_engineering_and_target_construction.md`

### Phase 8 — Predictive Model Development

**Status: Completed**

Developed and compared classification models to estimate whether an eligible customer would make at least one qualifying purchase within the next 90 days.

Four candidate algorithms were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Key accomplishments:

- Established Logistic Regression as the initial interpretable baseline using standardized features.
- Developed tree-based models to investigate nonlinear purchasing behavior.
- Compared models using ROC-AUC, PR-AUC, accuracy, precision, recall, F1-score, and confusion matrices.
- Examined training-validation performance differences to assess generalization and potential overfitting.
- Investigated Logistic Regression coefficients and Gradient Boosting feature importance.
- Tuned Logistic Regression regularization and Gradient Boosting hyperparameters using the validation partition.
- Compared the tuned candidate models and selected a primary model and an alternative.
- Evaluated classification thresholds to examine precision-recall trade-offs and operational prediction volumes.

**Selected findings:**

- Tuned Logistic Regression achieved validation ROC-AUC 0.7472, PR-AUC 0.7190, and F1-score 0.6442.
- Tuned Gradient Boosting achieved validation ROC-AUC 0.7476, PR-AUC 0.7215, and F1-score 0.6406.
- Historical purchase frequency and monetary value were the strongest predictive signals across the two examined models.
- Logistic Regression was selected as the primary candidate because of its slightly stronger recall and F1-score, alongside its simpler and more interpretable structure.
- Gradient Boosting was retained as an alternative candidate because of its marginally higher ROC-AUC and PR-AUC.

**Selected primary model:**

- Algorithm: Logistic Regression
- Regularization parameter: `C=0.01`
- Classification threshold: `0.50`
- Scaling: StandardScaler
- Predictors: five Phase 7 baseline features

**Threshold analysis:**

| Threshold | Precision | Recall | F1-score |
|---:|---:|---:|---:|
| 0.40 | 51.59% | 83.17% | 0.6368 |
| 0.50 | 58.26% | 72.03% | 0.6442 |
| 0.60 | 67.08% | 59.14% | 0.6286 |

The threshold of 0.50 was retained as the primary operating threshold because it achieved the highest F1-score among the tested thresholds. A threshold of 0.40 was retained as a higher-recall alternative.

The test partition was not used for model training, hyperparameter tuning, or threshold selection. Final test-set evaluation and model explainability were addressed in Phase 9.

**Key outputs:**

- `notebooks/07_predictive_model_development.ipynb`
- `docs/predictive_model_development.md`

Documentation: `docs/predictive_model_development.md`

### Phase 9 — Model Evaluation & Explainability

**Status: Completed**

Evaluated the selected Tuned Logistic Regression model using the untouched chronological test partition and investigated its predictive behavior, feature associations, and temporal generalization.

Key accomplishments:

- Reconstructed the selected Phase 8 Logistic Regression pipeline using training data only.
- Reproduced the Phase 8 validation metrics to four decimal places before final test evaluation.
- Evaluated the frozen model on 5,534 test observations using ROC-AUC, PR-AUC, accuracy, precision, recall, specificity, F1-score, and Brier score.
- Examined the test confusion matrix and classification errors.
- Evaluated probability calibration using a ten-bin quantile-based calibration curve.
- Interpreted standardized Logistic Regression coefficients and odds ratios.
- Compared false positives, false negatives, true positives, and true negatives to investigate prediction error patterns.
- Compared model performance across training, validation, and test partitions.
- Documented temporal variation, calibration limitations, and constraints on model interpretation.

**Final test-set performance:**

| Metric | Test Result |
|---|---:|
| ROC-AUC | 0.7413 |
| PR-AUC | 0.8139 |
| Accuracy | 0.6765 |
| Precision | 0.7555 |
| Recall | 0.6565 |
| Specificity | 0.7044 |
| F1-score | 0.7026 |
| Brier score | 0.2031 |

**Test confusion matrix:**

| | Predicted non-repeat | Predicted repeat |
|---|---:|---:|
| Actual non-repeat | 1,630 | 684 |
| Actual repeat | 1,106 | 2,114 |

**Selected explainability findings:**

- `log1p_frequency` was the strongest positive predictive feature, with a standardized coefficient of 0.5922 and odds ratio of 1.8080.
- `log1p_monetary` had a positive coefficient of 0.2601 and odds ratio of 1.2971.
- `log1p_unique_products` had a positive coefficient of 0.1737 and odds ratio of 1.1897.
- `recency_days` had a negative coefficient of -0.0886 and odds ratio of 0.9152.
- `log1p_cancellation_value` had a small positive coefficient of 0.0481 and odds ratio of 1.0493.

The coefficients represent conditional predictive associations rather than causal effects.

**Temporal generalization findings:**

- ROC-AUC remained relatively stable across training (0.7267), validation (0.7472), and test (0.7413).
- Test precision was higher than validation precision (75.55% versus 58.26%), while test recall was lower (65.65% versus 72.03%).
- Positive-class prevalence varied across the three partitions, influencing the interpretation of precision and PR-AUC.
- The test calibration curve indicated systematic underestimation of observed repeat-purchase rates.
- The model demonstrated reasonably stable temporal ranking performance, but classification behavior and probability calibration varied across periods.

**Key outputs:**

- `notebooks/08_model_evaluation_and_explainability.ipynb`
- `docs/model_evaluation_and_explainability.md`

Documentation: `docs/model_evaluation_and_explainability.md`

### Phase 10 — Business Impact & Retention Prioritization

**Status: Completed**

Translated predictive model outputs into a customer prioritization framework by combining predicted repeat-purchase probability with historical monetary value.

Key accomplishments:

- Reconstructed the selected Phase 9 Logistic Regression model and generated predictions for the held-out test partition.
- Created a customer-level prioritization dataset containing 2,968 unique customers, retaining each customer's latest available test-period snapshot.
- Reconstructed historical qualifying purchase value from the preceding 180-day feature window.
- Developed a 2 × 2 priority matrix using median predicted probability (0.4791) and median historical monetary value (454.18).
- Profiled priority groups using snapshot-specific recency, frequency, and monetary metrics, avoiding the use of full-history customer segments that could introduce future information.
- Evaluated the groups retrospectively using actual 90-day repeat-purchase outcomes.
- Compared four customer coverage scenarios to examine trade-offs between customer coverage, predicted propensity, and historical monetary value.
- Examined historical monetary value associated with customers who did and did not repeat purchase.
- Developed differentiated retention and engagement recommendations for each priority group.
- Documented analytical limitations, including the absence of intervention outcomes, campaign costs, profit margins, and causal uplift estimates.

**Priority groups:**

| Priority group | Customers | Customer share | Historical value share | Actual repeat rate |
|---|---:|---:|---:|---:|
| P1 — High value, low propensity | 228 | 7.68% | 4.49% | 41.67% |
| P2 — High value, high propensity | 1,256 | 42.32% | 85.64% | 78.90% |
| P3 — Low value, low propensity | 1,256 | 42.32% | 7.76% | 40.61% |
| P4 — Low value, high propensity | 228 | 7.68% | 2.11% | 57.89% |

**Selected findings:**

- P1 represented a focused group of 228 customers with relatively high historical monetary value and lower predicted repeat-purchase propensity.
- P1 had the highest proportion of group historical monetary value associated with non-repeat outcomes (59.60%).
- P3 had a similar non-repeat historical value share (57.16%), but contained a larger population of 1,256 customers with lower historical monetary value per customer.
- P2 represented 85.64% of total historical monetary value, making it important for relationship maintenance despite its relatively high repeat-purchase propensity.
- A high-value customer coverage scenario containing P1 and P2 covered 50% of customers and represented 90.13% of historical monetary value.
- A broad risk coverage scenario containing P1 and P3 covered 50% of customers but represented 12.25% of historical monetary value.

**Business recommendations:**

- P1: Focused retention review and potentially personalized engagement.
- P3: Scalable, lower-cost engagement initiatives.
- P2: Relationship maintenance and ongoing monitoring.
- P4: Routine engagement and potential growth opportunities.

These recommendations are analytical hypotheses, not proven interventions. Historical monetary value is not lifetime value, profit, revenue at risk, or recoverable revenue. The analysis does not establish campaign effectiveness, incremental repeat purchases, or retention ROI.

**Key outputs:**

- `notebooks/09_business_impact_and_retention_prioritization.ipynb`
- `docs/business_impact_and_retention_prioritization.md`

Documentation: `docs/business_impact_and_retention_prioritization.md`

### Upcoming Phases

| Phase | Focus | Status |
|---|---|---|
| 11 | Streamlit Application | Planned |
| 12 | Testing, Refactoring & Documentation | Planned |
| 13 | Final Portfolio Presentation | Planned |

## Important Analytical Considerations

This project investigates behavioral purchase inactivity and repeat-purchase propensity, not subscription cancellation or permanent customer churn.

The dataset does not contain explicit churn labels, customer demographics, product costs, profit margins, or retention campaign costs.

Consequently:

- Inactivity must be defined using an explicit observation window.
- Predictive labels must account for the dataset's temporal coverage.
- The repeat-purchase target represents future purchasing behavior within a defined 90-day window, not permanent customer retention or churn.
- Historical revenue must not be interpreted as profit or customer lifetime value.
- Predictive associations must not be interpreted as causal relationships.
- Cancellation records must not automatically be treated as confirmed matches to original purchases.
- Gross qualifying purchase revenue does not automatically account for cancellations.
- Temporal variation in purchasing behavior must be considered when evaluating predictive performance.
- Test-set performance has been evaluated, but it does not establish production readiness or performance on entirely unseen customers.
- Test calibration indicated systematic underestimation of observed repeat-purchase rates; predicted probabilities should therefore be interpreted cautiously.
- Retention return on investment cannot be established without additional cost, margin, and intervention-effectiveness information.
- Classification thresholds should not be treated as financially optimal without evidence about intervention costs and business outcomes.

These limitations are considered throughout the analytical workflow.

## Repository and Data Policy

Source code, notebooks, documentation, and reference files are maintained in Git.

Raw and processed datasets are excluded from version control because of their size and data management considerations. The original dataset can be obtained from the official UCI repository. Processed analytical datasets and modeling outputs can be reproduced by running the relevant notebooks and scripts.

## Author

Developed as an independent data science portfolio project.