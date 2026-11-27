
import pandas as pd
import streamlit as st

from app.config import (
    CUSTOMER_ANALYTICS_PATH,
    PURCHASE_PROPENSITY_PATH,
    RETENTION_PRIORITIES_PATH,
    RFM_SEGMENT_PROFILE_PATH,
    KMEANS_CLUSTER_PROFILE_PATH,
    RFM_CANCELLATION_PATH,
    TOP_CANCELLATION_CUSTOMERS_PATH,
)

from app.utils.data_validation import (
    validate_file_exists,
    validate_columns,
    validate_non_empty,
)


def _load_dataset(
    path,
    label,
    required_columns,
    file_format="parquet",
):
    """Load and validate a required application dataset."""

    validate_file_exists(path, label)

    try:
        if file_format == "parquet":
            df = pd.read_parquet(path)

        elif file_format == "csv":
            df = pd.read_csv(path)

        else:
            raise ValueError(
                f"Unsupported dataset format: {file_format}"
            )

    except (OSError, ValueError, ImportError) as error:
        st.error(
            f"Unable to load dataset: {label}\n\n"
            f"File location: {path}\n\n"
            f"Details: {error}"
        )
        st.stop()

    validate_columns(
        df,
        required_columns,
        label,
    )

    validate_non_empty(
        df,
        label,
    )

    return df


@st.cache_data
def load_customer_analytics():
    return _load_dataset(
        path=CUSTOMER_ANALYTICS_PATH,
        label="Customer analytics",
        required_columns=[
            "Customer ID",
            "recency",
            "frequency",
            "monetary",
            "rfm_segment",
            "cancellation_value",
        ],
    )


@st.cache_data
def load_purchase_propensity_dataset():
    return _load_dataset(
        path=PURCHASE_PROPENSITY_PATH,
        label="Purchase propensity",
        required_columns=[
            "Customer ID",
            "snapshot_date",
            "recency_days",
            "log1p_frequency",
            "log1p_monetary",
            "log1p_unique_products",
            "log1p_cancellation_value",
            "repeat_purchase_90d",
            "partition",
        ],
    )


@st.cache_data
def load_retention_priorities():
    return _load_dataset(
        path=RETENTION_PRIORITIES_PATH,
        label="Retention priorities",
        required_columns=[
            "Customer ID",
            "snapshot_date",
            "historical_monetary",
            "predicted_probability",
            "repeat_purchase_90d",
            "priority_segment",
        ],
    )


@st.cache_data
def load_rfm_segment_profile():
    return _load_dataset(
        path=RFM_SEGMENT_PROFILE_PATH,
        label="RFM segment profile",
        required_columns=[
            "rfm_segment",
            "customers",
            "total_purchase_value",
            "total_cancellation_value",
        ],
        file_format="csv",
    )


@st.cache_data
def load_kmeans_cluster_profile():
    return _load_dataset(
        path=KMEANS_CLUSTER_PROFILE_PATH,
        label="K-Means cluster profile",
        required_columns=[
            "kmeans_cluster",
            "customers",
            "total_purchase_value",
        ],
        file_format="csv",
    )


@st.cache_data
def load_rfm_cancellation_concentration():
    return _load_dataset(
        path=RFM_CANCELLATION_PATH,
        label="RFM cancellation concentration",
        required_columns=[
            "rfm_segment",
            "customers",
            "customers_with_cancellations",
        ],
        file_format="csv",
    )


@st.cache_data
def load_top_cancellation_customers():
    return _load_dataset(
        path=TOP_CANCELLATION_CUSTOMERS_PATH,
        label="Top cancellation customers",
        required_columns=[
            "Customer ID",
            "rfm_segment",
            "recency",
            "frequency",
            "monetary",
            "cancellation_value",
        ],
        file_format="csv",
    )
