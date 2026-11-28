# Customer Intelligence & Revenue Optimization

An end-to-end data science project analyzing retail transaction data to understand customer purchasing behavior, identify repeat-purchase patterns, and develop data-driven retention prioritization strategies.

The project combines data engineering, exploratory data analysis, customer segmentation, predictive modeling, model evaluation, and business-oriented analytics in an interactive Streamlit application.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Business Objectives](#business-objectives)
3. [Dataset](#dataset)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Getting Started](#getting-started)
7. [Data and Model Reproduction](#data-and-model-reproduction)
8. [Streamlit Application](#streamlit-application)
9. [Key Analytical Findings](#key-analytical-findings)
10. [Model Performance](#model-performance)
11. [Retention Prioritization](#retention-prioritization)
12. [Limitations and Methodological Considerations](#limitations-and-methodological-considerations)
13. [Project Progress](#project-progress)
14. [References](#references)

---

## Project Overview

This project investigates customer purchasing behavior using the Online Retail II dataset.

The objective is to transform raw retail transaction records into actionable customer intelligence through a reproducible analytical workflow.

The project focuses on three connected questions:

- **Customer intelligence:** Who are the customers, how do their purchasing patterns differ, and which customers have become inactive?
- **Predictive analytics:** Which active customers are more or less likely to make another purchase within a defined future period?
- **Retention prioritization:** How can customers be grouped into actionable priorities using predicted repeat-purchase probability and historical customer value?

The project does not treat customer inactivity as proof of permanent churn. Instead, it examines observed purchasing behavior and future repeat-purchase propensity within explicitly defined observation windows.

## Business Objectives

The project aims to:

1. Assess and prepare historical retail transaction data for analysis.
2. Investigate customer purchasing patterns, revenue composition, and transaction behavior.
3. Segment customers using Recency, Frequency, and Monetary (RFM) analysis.
4. Develop a predictive model estimating repeat-purchase probability.
5. Evaluate model performance using appropriate classification and probability metrics.
6. Translate model predictions into customer retention priorities.
7. Present analytical findings through an interactive business-facing application.

## Dataset

**Source:** UCI Machine Learning Repository — Online Retail II

The dataset contains transactions from a UK-based online retail business between December 2009 and December 2011.

- Original records: 1,067,371 transaction line items
- Original features: 8 columns
- Period covered: December 2009 – December 2011
- Format: Excel workbook containing two sheets

Original columns:

| Column | Description |
|---|---|
| Invoice | Invoice number |
| StockCode | Product code |
| Description | Product or transaction description |
| Quantity | Quantity of items |
| InvoiceDate | Transaction date and time |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer country |

The original workbook is not included in the repository because of its size.

Download the dataset from the [UCI Machine Learning Repository](https://doi.org/10.24432/C5CG6D) and place the workbook at:

`data/raw/online_retail_II.xlsx`

The project also relies on two reference files generated during data preparation:

- `data/reference/description_mapping.csv`
- `data/reference/transaction_taxonomy.csv`

These files contain approved description mappings and transaction classification rules. They must be available when reproducing the data transformation workflow.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data manipulation | Pandas, NumPy |
| Data ingestion | OpenPyXL |
| Database | PostgreSQL |
| Database integration | SQLAlchemy, Psycopg |
| Data analysis | Descriptive statistics, statistical analysis |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine learning | Scikit-learn |
| Predictive modeling | Logistic Regression, Gradient Boosting |
| Model interpretation | Logistic Regression coefficients and odds ratios |
| Model persistence | Joblib |
| Interactive application | Streamlit |
| Data storage | CSV, Parquet |
| Development | Jupyter Notebook, VS Code |
| Version control | Git, GitHub |

## Project Structure

```text
customer-intelligence-revenue-optimization/
│
├── .streamlit/
│   └── config.toml
│
├── app/
│   ├── Home.py
│   ├── config.py
│   │
│   ├── pages/
│   │   ├── 1_Executive_Overview.py
│   │   ├── 2_Customer_Segmentation.py
│   │   ├── 3_Repeat_Purchase_Prediction.py
│   │   └── 4_Retention_Prioritization.py
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   └── metrics.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── data_validation.py
│       └── model_loader.py
│
├── data/
│   ├── raw/
│   ├── reference/
│   │   ├── description_mapping.csv
│   │   └── transaction_taxonomy.csv
│   └── processed/
│
├── docs/
│   ├── data_cleaning_and_etl.md
│   ├── exploratory_data_analysis.md
│   ├── customer_analytics_and_segmentation.md
│   └── ...
│
├── models/
│   └── selected_logistic_regression.joblib
│
├── notebooks/
│   ├── 01_business_understanding.ipynb
│   ├── 02_data_quality_assessment.ipynb
│   ├── 03_database_engineering_and_sql_analytics.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_customer_analytics_and_segmentation.ipynb
│   ├── 06_feature_engineering_and_target_construction.ipynb
│   ├── 07_model_development.ipynb
│   ├── 08_model_evaluation_and_explainability.ipynb
│   └── 09_business_impact_and_retention_prioritization.ipynb
│
├── sql/
│
├── src/
│   ├── data/
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── validate.py
│   │   └── load.py
│   │
│   └── model/
│       ├── train_model.py
│       └── build_retention_priorities.py
│
├── tests/
│
├── reports/
│
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

*The tree describes the principal project components. Local raw and processed data files are not necessarily tracked in Git.*

## Getting Started

### 1. Clone the repository

```powershell
git clone https://github.com/hizkiafebrian98/customer-intelligence-revenue-optimization.git

cd customer-intelligence-revenue-optimization
```

### 2. Create and activate a Python environment

The project was developed and tested using Python 3.12.

Using Conda:

```powershell
conda create -n retail-analytics python=3.12 -y

conda activate retail-analytics
```

Alternatively, create a virtual environment:

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

### 4. Prepare the dataset

Download the Online Retail II workbook from UCI and place it at:

```text
data/raw/online_retail_II.xlsx
```

Ensure the required reference files are also available:

```text
data/reference/description_mapping.csv
data/reference/transaction_taxonomy.csv
```

### 5. Prepare analytical artifacts

The processed datasets and model artifacts are required by the analytical notebooks and Streamlit application.

Follow the data preparation and feature engineering workflow described below before launching the application.

## Data and Model Reproduction

The project follows a sequential workflow. Later stages depend on artifacts generated in earlier stages.

### Stage 1 — Data preparation and ETL

The data preparation scripts are located in:

```text
src/data/
```

They cover:

- Data extraction from the original workbook.
- Transaction transformation and classification.
- Data quality and output validation.
- Database loading.

The cleaning workflow uses the approved reference files in `data/reference/`.

The primary cleaned transaction artifacts include:

```text
data/processed/online_retail_clean.parquet
data/processed/duplicate_audit.csv
```

The cleaned dataset contains 1,033,036 records, with 34,335 exact duplicate records retained separately for audit purposes.

See `docs/data_cleaning_and_etl.md` for the data treatment decisions and validation details.

### Stage 2 — Feature engineering and target construction

Run the notebook:

```text
notebooks/06_feature_engineering_and_target_construction.ipynb
```

This notebook generates:

```text
data/processed/customer_purchase_propensity_dataset.parquet
```

The resulting modeling dataset contains 47,933 customer-snapshot observations.

The target identifies whether a customer makes another qualifying purchase within the subsequent 90-day target window.

### Stage 3 — Model training

After generating the modeling dataset, execute:

```powershell
python src/model/train_model.py
```

The training script:

- Uses the training partition only.
- Applies feature standardization.
- Fits the selected Logistic Regression model.
- Saves the fitted pipeline using Joblib.

Output:

```text
models/selected_logistic_regression.joblib
```

### Stage 4 — Retention-priority generation

After model training, execute:

```powershell
python src/model/build_retention_priorities.py
```

This script:

- Loads the fitted model.
- Generates repeat-purchase probabilities for test-partition observations.
- Reconstructs historical monetary values from their log-transformed representation.
- Retains the latest test-period snapshot for each customer.
- Assigns customers to four priority groups using median-based thresholds.

Output:

```text
data/processed/retention_priorities.parquet
```

The resulting dataset contains 2,968 unique customers.

### Reproduction dependencies

The model and retention-priority scripts require the following files:

| Artifact | Generated by |
|---|---|
| `customer_purchase_propensity_dataset.parquet` | Phase 7 feature-engineering notebook |
| `selected_logistic_regression.joblib` | `src/model/train_model.py` |
| `retention_priorities.parquet` | `src/model/build_retention_priorities.py` |

The complete workflow also requires the original workbook and the two reference files.

## Streamlit Application

The project includes an interactive Streamlit application designed to communicate analytical results and support customer-level exploration.

### Run the application

From the project root:

```powershell
python -m streamlit run app/Home.py
```

The application requires the processed analytical datasets and fitted model artifact to be available in their expected local directories.

### Application pages

#### 1. Executive Overview

Provides a high-level summary of customer behavior, revenue patterns, segmentation, and repeat-purchase modeling.

#### 2. Customer Segmentation

Enables exploration of RFM customer segments and complementary K-Means clusters.

Users can filter customer groups and inspect their associated metrics and customer records.

#### 3. Repeat-Purchase Prediction

Provides an interactive interface for exploring predicted repeat-purchase probabilities.

Users can adjust the classification threshold and examine its effect on classification metrics and the confusion matrix.

#### 4. Retention Prioritization

Presents the four customer priority groups, their historical monetary values, predicted probabilities, and recommended retention actions.

Users can filter priority groups and explore individual customer records.

## Key Analytical Findings

### Data quality and preparation

The original dataset contained 1,067,371 transaction line items.

After the data quality and cleaning workflow:

- 1,033,036 records remained in the primary cleaned dataset.
- 34,335 exact duplicate records were separated into an audit dataset.
- Missing customer identifiers were preserved rather than imputed.
- Missing descriptions were partially recovered using an evidence-based StockCode mapping.
- Transaction categories and analytical eligibility were established through explicit classification rules.

### Exploratory data analysis

The cleaned dataset covers December 1, 2009 to December 9, 2011.

Key findings include:

- Customer ID was missing in approximately 22.76% of original transaction records.
- November was the strongest month for observed revenue in the dataset.
- December 2011 represents only a partial month.
- The United Kingdom accounted for approximately 85.42% of total merchandise revenue.
- The five largest revenue-contributing countries represented approximately 95.02% of total merchandise revenue.
- The top 100 products accounted for approximately 28.96% of merchandise revenue.

Net merchandise revenue was approximately £18.92 million.

### Customer segmentation

Customer analytics identified 5,852 customers.

RFM analysis produced six customer segments:

| Segment | Customers | Revenue Share |
|---|---:|---:|
| At-risk valuable | 782 | 9.95% |
| Champions | 1,254 | 67.71% |
| Hibernating | 1,352 | 2.04% |
| Loyal customers | 603 | 10.21% |
| Other customers | 1,693 | 6.99% |
| Recent high-value | 168 | 3.10% |

RFM segmentation was used as the primary business-facing segmentation approach.

K-Means clustering was implemented as a complementary unsupervised analysis. The selected four-cluster solution achieved a silhouette score of 0.3614.

### Predictive modeling

The predictive task estimates the probability of a qualifying repeat purchase within a 90-day target window.

The selected model was Logistic Regression with standardized features.

The five selected predictors were:

- `recency_days`
- `log1p_frequency`
- `log1p_monetary`
- `log1p_unique_products`
- `log1p_cancellation_value`

## Model Performance

The selected Logistic Regression model achieved the following results.

### Validation performance

| Metric | Score |
|---|---:|
| ROC-AUC | 0.7472 |
| PR-AUC | 0.7190 |
| Accuracy | 0.6661 |
| Precision | 0.5826 |
| Recall | 0.7203 |
| F1-score | 0.6442 |

### Test performance

| Metric | Score |
|---|---:|
| ROC-AUC | 0.7413 |
| PR-AUC | 0.8139 |
| Accuracy | 0.6765 |
| Precision | 0.7555 |
| Recall | 0.6565 |
| F1-score | 0.7026 |
| Specificity | 0.7044 |
| Brier score | 0.2031 |

The model was selected using validation performance. The test partition was reserved for final evaluation.

## Retention Prioritization

Customers were grouped using two dimensions:

1. Historical monetary value.
2. Predicted repeat-purchase probability.

Both dimensions use the median of the customer-level test population as their respective thresholds.

| Priority | Customer Profile | Customers | Historical Monetary Value |
|---|---|---:|---:|
| P1 | High value, low predicted probability | 228 | £159,677.46 |
| P2 | High value, high predicted probability | 1,256 | £3,043,099.13 |
| P3 | Low value, low predicted probability | 1,256 | £275,587.57 |
| P4 | Low value, high predicted probability | 228 | £75,012.29 |

### Priority interpretation

- **P1:** Higher historical customer value combined with lower predicted repeat-purchase probability. Potentially suitable for targeted retention attention.
- **P2:** Higher historical customer value and higher predicted repeat-purchase probability. Potentially suitable for loyalty and relationship-strengthening initiatives.
- **P3:** Lower historical customer value and lower predicted repeat-purchase probability. Potentially suitable for lower-cost or selective engagement.
- **P4:** Lower historical customer value and higher predicted repeat-purchase probability. Potentially suitable for scalable engagement strategies.

These groups are prioritization categories, not estimates of incremental campaign impact.

## Limitations and Methodological Considerations

Several limitations should be considered when interpreting the findings.

### Dataset limitations

- The dataset represents historical transactions from a single online retail business.
- Customer identifiers are missing for a substantial proportion of transaction records.
- The dataset does not contain complete customer demographics, marketing exposure, or campaign response information.
- The observation period ends on December 9, 2011.

### Revenue interpretation

Revenue figures represent historical transaction-based merchandise revenue under the project's classification rules.

They should not be interpreted as profit, customer lifetime value, or incremental revenue.

### Customer inactivity

A customer with a long period without a purchase is not necessarily permanently churned.

The project uses observed inactivity and repeat-purchase behavior rather than claiming permanent customer attrition.

### Predictive modeling

- Model predictions represent estimated repeat-purchase probabilities within a defined target window.
- Temporal partitions were used to evaluate model performance.
- Customer overlap across temporal partitions is intentional; the evaluation does not establish generalization to entirely unseen customers.
- Model coefficients indicate statistical associations, not causal effects.
- Probability calibration showed that the model tends to underestimate observed repeat-purchase rates in parts of the probability range.

### Retention prioritization

- Priority thresholds are relative to the evaluated customer population.
- Historical monetary value is not equivalent to customer lifetime value.
- No causal campaign experiment was conducted.
- Retention scenarios do not establish actual revenue saved, campaign ROI, or incremental business impact.

## Project Progress

The project is organized into thirteen phases.

| Phase | Description | Status |
|---|---|---|
| 1 | Business Understanding & Problem Formulation | Completed |
| 2 | Dataset Acquisition & Feasibility Assessment | Completed |
| 3 | Data Quality Assessment, Cleaning & ETL Preparation | Completed |
| 4 | Database Engineering & SQL Analytics | Completed |
| 5 | Exploratory Data Analysis | Completed |
| 6 | Customer Analytics & Segmentation | Completed |
| 7 | Feature Engineering & Target Construction | Completed |
| 8 | Predictive Model Development | Completed |
| 9 | Model Evaluation & Explainability | Completed |
| 10 | Business Impact & Retention Prioritization | Completed |
| 11 | Streamlit Application | Completed |
| 12 | Testing, Refactoring & Documentation | In Progress |
| 13 | Final Portfolio Presentation | Planned |

## References

Chen, D. (2012). *Online Retail II*. UCI Machine Learning Repository.

https://doi.org/10.24432/C5CG6D

Dataset license: Creative Commons Attribution 4.0 International (CC BY 4.0).

---

**Author:** Hizkia Febrian

**Repository:** [customer-intelligence-revenue-optimization](https://github.com/hizkiafebrian98/customer-intelligence-revenue-optimization)
