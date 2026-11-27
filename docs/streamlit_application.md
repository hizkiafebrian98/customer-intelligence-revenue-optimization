# Streamlit Application Documentation

## 1. Overview

The Customer Intelligence & Revenue Optimization application is an interactive dashboard developed using Streamlit.

The application presents analytical findings from the UCI Online Retail II dataset, covering customer purchasing behavior, revenue contribution, customer segmentation, repeat-purchase prediction, and retention prioritization.

Its primary objective is to translate analytical outputs into accessible business insights and decision-support information.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Application framework | Streamlit |
| Data manipulation | Pandas |
| Numerical computation | NumPy |
| Data visualization | Plotly |
| Machine learning | Scikit-learn |
| Model serialization | Joblib |
| Data storage | Parquet and CSV |
| Programming language | Python |

## 3. Application Architecture

The application follows a modular structure that separates navigation, page-level functionality, reusable components, and data-access utilities.

```text
app/
├── Home.py
│
├── pages/
│   ├── 1_Executive_Overview.py
│   ├── 2_Customer_Segmentation.py
│   ├── 3_Repeat_Purchase_Prediction.py
│   └── 4_Retention_Prioritization.py
│
├── components/
│   ├── __init__.py
│   ├── metrics.py
│   └── charts.py
│
└── utils/
    ├── __init__.py
    ├── data_loader.py
    ├── data_validation.py
    └── model_loader.py
```

### 3.1 Navigation

`Home.py` acts as the central application entry point and navigation controller.

Streamlit's `st.navigation()` and `st.Page()` functions register the four application pages.

Material Symbols icons are used consistently in the navigation sidebar and individual page headings.

### 3.2 Reusable Components

**Metrics (`components/metrics.py`)**

Provides a reusable function for displaying KPI cards with consistent styling.

**Charts (`components/charts.py`)**

Provides shared Plotly styling, including typography, chart colors, backgrounds, axes, and category-specific color mappings.

### 3.3 Data Access and Validation

The data-access utilities are responsible for loading the analytical datasets and validating their availability and structure.

- `data_loader.py`: Loads processed analytical datasets using Streamlit caching.
- `data_validation.py`: Checks file existence, required columns, and non-empty datasets.
- `model_loader.py`: Loads the selected serialized Logistic Regression pipeline using resource caching.

## 4. Application Pages

### 4.1 Executive Overview

Provides a high-level summary of customer analytics and revenue performance.

Key elements:

- Identified customer count.
- Qualifying purchase revenue.
- Median purchase recency.
- Customers with recorded cancellation values.
- Customer distribution across RFM segments.
- Purchase revenue by RFM segment.
- RFM segment performance table.
- Key business observations.

### 4.2 Customer Segmentation

Presents customer-level purchasing behavior and segmentation results.

Key elements:

- RFM segment analysis.
- Customer-level filtering and exploration.
- Recency and frequency distributions.
- Monetary-value analysis.
- K-Means clustering results.
- Customer segmentation visualizations.

RFM segmentation is used as the primary business-oriented classification, while K-Means provides complementary clustering analysis.

### 4.3 Repeat-Purchase Prediction

Presents the selected Logistic Regression model and its repeat-purchase predictions.

Key elements:

- Model performance metrics.
- Classification threshold adjustment.
- Precision, recall, and F1-score monitoring.
- Confusion matrix.
- Customer-level prediction exploration.
- Predicted probabilities and observed outcomes.

The prediction target represents whether an eligible customer makes another qualifying purchase within the defined 90-day future window.

### 4.4 Retention Prioritization

Translates customer-level predictions and historical monetary values into actionable prioritization groups.

The application presents four priority segments:

- P1: High historical monetary value and lower predicted repeat-purchase probability.
- P2: High historical monetary value and higher predicted repeat-purchase probability.
- P3: Low historical monetary value and lower predicted repeat-purchase probability.
- P4: Low historical monetary value and higher predicted repeat-purchase probability.

Key elements:

- Priority-segment distribution.
- Historical monetary-value concentration.
- Customer filtering and exploration.
- Retention prioritization scenarios.
- Customer-level predicted probabilities.

## 5. Data and Model Integration

The application uses processed analytical artifacts generated during the preceding project phases.

Primary datasets include:

| Artifact | Purpose |
|---|---|
| `customer_analytics.parquet` | Customer-level analytical attributes |
| `customer_purchase_propensity_dataset.parquet` | Feature and target dataset |
| `retention_priorities.parquet` | Customer-level retention prioritization |
| `rfm_segment_profile.csv` | RFM segment summaries |
| `kmeans_cluster_profile.csv` | K-Means cluster summaries |
| `rfm_cancellation_concentration.csv` | Cancellation concentration by RFM segment |
| `top_cancellation_customers_by_rfm.csv` | Selected customers with cancellation activity |

The selected Logistic Regression pipeline is stored at:

`models/selected_logistic_regression.joblib`

The model was developed and evaluated in the preceding modeling phases. The application loads the selected model artifact rather than independently retraining it during normal application execution.

## 6. Visual Design

The application uses a Modern Enterprise BI visual direction.

Design characteristics include:

- Inter typography.
- Muted navy and blue color palette.
- Cool light-gray application background.
- White KPI cards with subtle borders and blue accents.
- Consistent Plotly chart styling.
- Consistent category colors across analytical pages.
- Material Symbols navigation icons.

Shared styling is maintained through `.streamlit/config.toml` and the reusable chart and metric components.

## 7. Running the Application

### Prerequisites

- Python environment with project dependencies installed.
- Processed analytical datasets available under `data/processed/`.
- Selected model artifact available under `models/`.

### Environment activation

On Windows PowerShell:

```powershell
& "C:\ProgramData\anaconda3\shell\condabin\conda-hook.ps1"
conda activate tf-env
```

### Launching Streamlit

From the project root:

```powershell
python -s -m streamlit run app/Home.py
```

The application opens in the default web browser.

## 8. Methodological Considerations and Limitations

The application presents historical analytical results and model-based predictions. These should be interpreted within the limitations of the underlying dataset and methodology.

- Qualifying purchase revenue represents historical purchase value, not profit.
- Historical monetary value is not equivalent to customer lifetime value.
- RFM segments are rule-based analytical classifications.
- K-Means clusters are complementary statistical groupings.
- Repeat-purchase predictions are probabilistic estimates, not certainties.
- The prediction target concerns repeat purchasing within a defined 90-day window, not permanent customer churn.
- Cancellation values are not automatically equivalent to confirmed refunds or lost revenue.
- Retention prioritization scenarios do not establish causal intervention effects, incremental revenue, or return on investment.
- Model evaluation uses temporal partitions with customer overlap; results should not be interpreted as evidence of generalization to entirely unseen customers.

## 9. Project Status

Phase 11 — Streamlit Application: Completed.

The application integrates the analytical outputs from the preceding phases into a modular, interactive dashboard.

Further automated testing, refactoring, reproducibility improvements, and comprehensive project documentation are addressed in Phase 12.