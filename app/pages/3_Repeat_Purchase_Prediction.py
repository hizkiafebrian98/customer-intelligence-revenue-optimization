
from app.utils.model_loader import load_selected_model

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

from utils.data_loader import load_purchase_propensity_dataset

from app.components.metrics import display_metric_row
from app.components.charts import apply_chart_theme


FEATURES = [
    "recency_days",
    "log1p_frequency",
    "log1p_monetary",
    "log1p_unique_products",
    "log1p_cancellation_value",
]

TARGET = "repeat_purchase_90d"


# Load data and model
df = load_purchase_propensity_dataset()
model = load_selected_model()

test_df = df.loc[df["partition"] == "test"].copy()

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

test_df["predicted_probability"] = model.predict_proba(X_test)[:, 1]


# Page heading
st.title(":material/psychology: Repeat-Purchase Prediction")

st.markdown(
    """
    Explore the selected Logistic Regression model's ability to
    estimate the probability of a customer making another qualifying
    purchase within the following 90 days.
    """
)

st.caption(
    "Historical test-period evaluation | August–September 2011"
)


# Classification threshold
threshold = st.slider(
    "Classification Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.50,
    step=0.05,
)

test_df["predicted_class"] = (
    test_df["predicted_probability"] >= threshold
).astype(int)


# Classification metrics
y_pred = test_df["predicted_class"]

precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)

roc_auc = 0.7413
pr_auc = 0.8139
brier_score = 0.2031

display_metric_row([
    {
        "label": "ROC-AUC",
        "value": f"{roc_auc:.4f}",
    },
    {
        "label": "PR-AUC",
        "value": f"{pr_auc:.4f}",
    },
    {
        "label": "Precision",
        "value": f"{precision:.4f}",
    },
    {
        "label": "Recall",
        "value": f"{recall:.4f}",
    },
])

display_metric_row([
    {
        "label": "F1 Score",
        "value": f"{f1:.4f}",
    },
    {
        "label": "Brier Score",
        "value": f"{brier_score:.4f}",
    },
    {
        "label": "Test Observations",
        "value": f"{len(test_df):,}",
    },
    {
        "label": "Actual Repeat-Purchase Rate",
        "value": f"{y_test.mean():.2%}",
    },
])


st.divider()


# Probability distribution
st.subheader("Predicted Probability Distribution")

fig_probability = px.histogram(
    test_df,
    x="predicted_probability",
    nbins=30,
    title="Distribution of Predicted Repeat-Purchase Probabilities",
    labels={
        "predicted_probability": "Predicted Probability",
        "count": "Number of Observations",
    },
)

fig_probability.add_vline(
    x=threshold,
    line_dash="dash",
    annotation_text=f"Threshold: {threshold:.2f}",
)

fig_probability = apply_chart_theme(fig_probability)

st.plotly_chart(
    fig_probability,
    use_container_width=True,
)


# Confusion matrix
st.subheader("Classification Performance")

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1],
)

cm_df = pd.DataFrame(
    cm,
    index=["Actual No Repeat", "Actual Repeat"],
    columns=["Predicted No Repeat", "Predicted Repeat"],
)

fig_cm = px.imshow(
    cm_df,
    text_auto=True,
    aspect="auto",
    title="Confusion Matrix",
    labels={
        "x": "Predicted Class",
        "y": "Actual Class",
        "color": "Observations",
    },
    color_continuous_scale=[
        "#F3F6F9",
        "#A9BED2",
        "#52769C",
        "#203B5C",
    ],
)

fig_cm = apply_chart_theme(fig_cm)

st.plotly_chart(
    fig_cm,
    use_container_width=True,
)


# Prediction outcomes
st.subheader("Prediction Outcomes")

tp, fp, fn, tn = cm[1, 1], cm[0, 1], cm[1, 0], cm[0, 0]

outcome_col1, outcome_col2, outcome_col3, outcome_col4 = st.columns(4)

outcome_col1.metric("True Positives", f"{tp:,}")
outcome_col2.metric("False Positives", f"{fp:,}")
outcome_col3.metric("False Negatives", f"{fn:,}")
outcome_col4.metric("True Negatives", f"{tn:,}")


# Observation explorer
st.subheader("Historical Prediction Explorer")

display_df = test_df[
    [
        "Customer ID",
        "snapshot_date",
        "predicted_probability",
        "predicted_class",
        TARGET,
    ]
].copy()

display_df["Customer ID"] = (
    display_df["Customer ID"].astype("Int64")
)

st.dataframe(
    display_df.sort_values(
        "predicted_probability",
        ascending=False,
    ),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Customer ID": "Customer ID",
        "snapshot_date": st.column_config.DateColumn(
            "Snapshot Date"
        ),
        "predicted_probability": st.column_config.NumberColumn(
            "Predicted Repeat-Purchase Probability",
            format="percent",
        ),
        "predicted_class": "Predicted Class",
        TARGET: "Actual Outcome",
    },
)


st.caption(
    """
    A predicted class of 1 indicates that the predicted probability
    meets or exceeds the selected threshold. The actual outcome
    indicates whether a qualifying purchase occurred within the
    subsequent 90-day target window.

    The displayed ROC-AUC, PR-AUC, and Brier score are the fixed
    Phase 9 test results. Precision, recall, and F1 respond to the
    selected threshold. This page evaluates historical observations;
    it does not generate current customer forecasts.
    """
)
