# Customer Intelligence & Revenue Optimization

An applied data science project focused on understanding retail customer purchasing behavior, identifying customers at risk of becoming inactive, and supporting data-driven retention prioritization.

## Project Overview

Retail businesses generate large volumes of transaction data, but transaction records alone do not provide a complete understanding of customer behavior.

This project develops a customer intelligence solution using historical retail transactions to investigate:

- Which customers generate the most revenue?
- Which customers are becoming inactive?
- What purchasing behaviors are associated with customer inactivity?
- Can customer inactivity be predicted using historical purchasing behavior?
- Which customer characteristics contribute most to predictive outcomes?
- How much historical revenue is associated with customers identified as at risk?
- Which customer segments should receive retention attention first?

The project combines data engineering, exploratory data analysis, customer analytics, statistical methods, and machine learning into an end-to-end analytical workflow.

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
| Machine learning | Scikit-learn, XGBoost |
| Model explainability | SHAP |
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
│   └── 03_database_integration.ipynb
├── sql/
├── src/
│   └── data/
│       ├── extract.py
│       ├── transform.py
│       └── validate.py
├── app/
├── tests/
├── reports/
├── docs/
│   ├── dataset_feasibility_assessment.md
│   └── data_cleaning_and_etl.md
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Development Progress

### Phase 1 — Business Understanding & Problem Formulation

Defined the business context, management questions, analytical objectives, and project scope.

### Phase 2 — Dataset Acquisition & Feasibility Assessment

Selected and assessed the UCI Online Retail II dataset, including its structure, coverage, data quality characteristics, and analytical limitations.

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

### Upcoming Phases

| Phase | Focus | Status |
|---|---|---|
| 4 | Database Engineering & SQL Analytics | Planned |
| 5 | Exploratory Data Analysis | Planned |
| 6 | Customer Analytics & Segmentation | Planned |
| 7 | Feature Engineering & Target Construction | Planned |
| 8 | Predictive Model Development | Planned |
| 9 | Model Evaluation & Explainability | Planned |
| 10 | Business Impact & Retention Prioritization | Planned |
| 11 | Streamlit Application | Planned |
| 12 | Testing, Refactoring & Documentation | Planned |
| 13 | Final Portfolio Presentation | Planned |

## Important Analytical Considerations

This project investigates behavioral purchase inactivity, not subscription cancellation or permanent customer churn.

The dataset does not contain explicit churn labels, customer demographics, product costs, profit margins, or retention campaign costs.

Consequently:

- Inactivity must be defined using an explicit observation window.
- Predictive labels must account for the dataset's temporal coverage.
- Historical revenue must not be interpreted as profit.
- Predictive associations must not be interpreted as causal relationships.
- Retention return on investment cannot be established without additional cost and margin assumptions.

These limitations will be addressed throughout the analytical workflow.

## Repository and Data Policy

Source code, notebooks, documentation, and reference files are maintained in Git.

Raw and processed datasets are excluded from version control because of their size and data management considerations. The original dataset can be obtained from the official UCI repository.

## Author

Developed as an independent data science portfolio project.