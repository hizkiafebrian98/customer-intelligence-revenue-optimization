from pathlib import Path


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"


# Data paths
CUSTOMER_ANALYTICS_PATH = DATA_DIR / "customer_analytics.parquet"

PURCHASE_PROPENSITY_PATH = (
    DATA_DIR / "customer_purchase_propensity_dataset.parquet"
)

RETENTION_PRIORITIES_PATH = DATA_DIR / "retention_priorities.parquet"

RFM_SEGMENT_PROFILE_PATH = DATA_DIR / "rfm_segment_profile.csv"

KMEANS_CLUSTER_PROFILE_PATH = DATA_DIR / "kmeans_cluster_profile.csv"

RFM_CANCELLATION_PATH = (
    DATA_DIR / "rfm_cancellation_concentration.csv"
)

TOP_CANCELLATION_CUSTOMERS_PATH = (
    DATA_DIR / "top_cancellation_customers_by_rfm.csv"
)


# Model artifact
MODEL_PATH = MODEL_DIR / "selected_logistic_regression.joblib"


# Predictive model configuration
FEATURES = [
    "recency_days",
    "log1p_frequency",
    "log1p_monetary",
    "log1p_unique_products",
    "log1p_cancellation_value",
]

TARGET = "repeat_purchase_90d"


# Business analysis configuration
OBSERVATION_DATE = "2011-12-10"

DEFAULT_CLASSIFICATION_THRESHOLD = 0.50
