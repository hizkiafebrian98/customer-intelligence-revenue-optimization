from pathlib import Path

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_purchase_propensity_dataset.parquet"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "selected_logistic_regression.joblib"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retention_priorities.parquet"
)

FEATURES = [
    "recency_days",
    "log1p_frequency",
    "log1p_monetary",
    "log1p_unique_products",
    "log1p_cancellation_value",
]


def main():
    # Load historical test observations and fitted model
    df = pd.read_parquet(DATA_PATH)
    model = joblib.load(MODEL_PATH)

    test_df = df.loc[
        df["partition"] == "test"
    ].copy()

    # Generate repeat-purchase probabilities
    test_df["predicted_probability"] = model.predict_proba(
        test_df[FEATURES]
    )[:, 1]

    # Recover historical monetary value from log1p transformation
    test_df["historical_monetary"] = np.expm1(
        test_df["log1p_monetary"]
    )

    # Retain the latest test-period snapshot for each customer
    priority_df = (
        test_df.sort_values("snapshot_date")
        .drop_duplicates(
            subset="Customer ID",
            keep="last",
        )
        .copy()
    )

    # Define high/low thresholds using population medians
    monetary_threshold = priority_df[
        "historical_monetary"
    ].median()

    probability_threshold = priority_df[
        "predicted_probability"
    ].median()

    high_value = (
        priority_df["historical_monetary"]
        >= monetary_threshold
    )

    high_probability = (
        priority_df["predicted_probability"]
        >= probability_threshold
    )

    # Assign four retention priority groups
    priority_df["priority_segment"] = np.select(
        [
            high_value & ~high_probability,
            high_value & high_probability,
            ~high_value & ~high_probability,
            ~high_value & high_probability,
        ],
        [
            "P1",
            "P2",
            "P3",
            "P4",
        ],
        default="Unassigned",
    )

    # Keep fields required by the application
    output_columns = [
        "Customer ID",
        "snapshot_date",
        "recency_days",
        "log1p_frequency",
        "log1p_monetary",
        "historical_monetary",
        "log1p_unique_products",
        "log1p_cancellation_value",
        "predicted_probability",
        "repeat_purchase_90d",
        "priority_segment",
    ]

    priority_df = priority_df[output_columns].copy()

    # Save artifact
    priority_df.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    print("Retention-priority dataset created.")
    print(f"Shape: {priority_df.shape}")
    print(f"Unique customers: {priority_df['Customer ID'].nunique():,}")
    print(f"Monetary threshold: £{monetary_threshold:,.2f}")
    print(f"Probability threshold: {probability_threshold:.4f}")

    print("\nPriority segment counts:")
    print(
        priority_df["priority_segment"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
