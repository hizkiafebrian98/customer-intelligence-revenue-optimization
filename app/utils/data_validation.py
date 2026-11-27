from pathlib import Path

import pandas as pd
import streamlit as st


def validate_file_exists(path: Path, label: str):
    """Check whether a required application file exists."""

    if not path.exists():
        st.error(
            f"Required file not found: {label}\n\n"
            f"Expected location: {path}"
        )
        st.stop()


def validate_columns(
    df: pd.DataFrame,
    required_columns: list,
    label: str,
):
    """Check whether a dataset contains its required columns."""

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Invalid dataset: {label}\n\n"
            f"Missing columns: {', '.join(missing_columns)}"
        )
        st.stop()


def validate_non_empty(df: pd.DataFrame, label: str):
    """Check whether a dataset contains records."""

    if df.empty:
        st.error(
            f"The dataset is empty: {label}"
        )
        st.stop()
