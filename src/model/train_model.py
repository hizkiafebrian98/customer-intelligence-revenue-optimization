from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# Resolve project directories
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_purchase_propensity_dataset.parquet"
)

MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "selected_logistic_regression.joblib"

# Phase 9 feature configuration
FEATURES = [
    "recency_days",
    "log1p_frequency",
    "log1p_monetary",
    "log1p_unique_products",
    "log1p_cancellation_value",
]

TARGET = "repeat_purchase_90d"


def main():
    # Load modeling dataset
    df = pd.read_parquet(DATA_PATH)

    # Use training partition only
    train_df = df.loc[df["partition"] == "train"].copy()

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    # Reproduce the selected Phase 9 pipeline
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "logistic_regression",
                LogisticRegression(
                    C=0.01,
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    # Fit using training data only
    model.fit(X_train, y_train)

    # Save fitted model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Model training completed.")
    print(f"Training observations: {len(X_train):,}")
    print(f"Features: {FEATURES}")
    print(f"Target: {TARGET}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
