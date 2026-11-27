
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



@st.cache_data
def load_customer_analytics():
    path = CUSTOMER_ANALYTICS_PATH
    validate_file_exists(path, "Customer analytics")

    df = pd.read_parquet(path)

    validate_columns(
        df,
        [
            "Customer ID",
            "recency",
            "frequency",
            "monetary",
            "rfm_segment",
            "cancellation_value",
        ],
        "Customer analytics",
    )

    validate_non_empty(df, "Customer analytics")
    return df


@st.cache_data
def load_purchase_propensity_dataset():
    path = PURCHASE_PROPENSITY_PATH
    validate_file_exists(path, "Purchase propensity")

    df = pd.read_parquet(path)

    validate_columns(
        df,
        [
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
        "Purchase propensity",
    )

    validate_non_empty(df, "Purchase propensity")
    return df


@st.cache_data
def load_retention_priorities():
    path = RETENTION_PRIORITIES_PATH
    validate_file_exists(path, "Retention priorities")

    df = pd.read_parquet(path)

    validate_columns(
        df,
        [
            "Customer ID",
            "snapshot_date",
            "historical_monetary",
            "predicted_probability",
            "repeat_purchase_90d",
            "priority_segment",
        ],
        "Retention priorities",
    )

    validate_non_empty(df, "Retention priorities")
    return df


@st.cache_data
def load_rfm_segment_profile():
    path = RFM_SEGMENT_PROFILE_PATH
    validate_file_exists(path, "RFM segment profile")

    df = pd.read_csv(path)

    validate_columns(
        df,
        [
            "rfm_segment",
            "customers",
            "total_purchase_value",
            "total_cancellation_value",
        ],
        "RFM segment profile",
    )

    validate_non_empty(df, "RFM segment profile")
    return df


@st.cache_data
def load_kmeans_cluster_profile():
    path = KMEANS_CLUSTER_PROFILE_PATH
    validate_file_exists(path, "K-Means cluster profile")

    df = pd.read_csv(path)

    validate_columns(
        df,
        [
            "kmeans_cluster",
            "customers",
            "total_purchase_value",
        ],
        "K-Means cluster profile",
    )

    validate_non_empty(df, "K-Means cluster profile")
    return df


@st.cache_data
def load_rfm_cancellation_concentration():
    path = RFM_CANCELLATION_PATH
    validate_file_exists(path, "RFM cancellation concentration")

    df = pd.read_csv(path)

    validate_columns(
        df,
        [
            "rfm_segment",
            "customers",
            "customers_with_cancellations",
        ],
        "RFM cancellation concentration",
    )

    validate_non_empty(df, "RFM cancellation concentration")
    return df


@st.cache_data
def load_top_cancellation_customers():
    path = TOP_CANCELLATION_CUSTOMERS_PATH
    validate_file_exists(path, "Top cancellation customers")

    df = pd.read_csv(path)

    validate_columns(
        df,
        [
            "Customer ID",
            "rfm_segment",
            "recency",
            "frequency",
            "monetary",
            "cancellation_value",
        ],
        "Top cancellation customers",
    )

    validate_non_empty(df, "Top cancellation customers")
    return df
