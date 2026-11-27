
import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_retention_priorities

from app.components.metrics import display_metric_row
from app.components.charts import (
    apply_chart_theme,
    PRIORITY_COLORS,
)


# Load customer-priority dataset
customers = load_retention_priorities()


# Priority group definitions
priority_descriptions = {
    "P1": "High historical value, low predicted repeat probability",
    "P2": "High historical value, high predicted repeat probability",
    "P3": "Low historical value, low predicted repeat probability",
    "P4": "Low historical value, high predicted repeat probability",
}

priority_actions = {
    "P1": "Focused retention review",
    "P2": "Maintain the customer relationship",
    "P3": "Scalable, lower-cost engagement",
    "P4": "Routine engagement and growth",
}


# Page heading
st.title(":material/track_changes: Retention Prioritization")

st.markdown(
    """
    Translate historical repeat-purchase predictions and customer
    monetary value into four actionable customer priority groups.
    """
)

st.caption(
    "Historical test-period prioritization | August–September 2011"
)


# Overall population metrics
total_customers = len(customers)

total_historical_value = customers[
    "historical_monetary"
].sum()

median_probability = customers[
    "predicted_probability"
].median()

actual_repeat_rate = customers[
    "repeat_purchase_90d"
].mean()

display_metric_row([
    {
        "label": "Customers Prioritized",
        "value": f"{total_customers:,}",
    },
    {
        "label": "Historical Purchase Value",
        "value": f"£{total_historical_value:,.2f}",
    },
    {
        "label": "Median Predicted Probability",
        "value": f"{median_probability:.2%}",
    },
    {
        "label": "Actual Repeat-Purchase Rate",
        "value": f"{actual_repeat_rate:.2%}",
    },
])


st.divider()


# Priority group selection
st.header("Priority Group Analysis")

selected_priority = st.selectbox(
    "Select Priority Group",
    ["All Groups", "P1", "P2", "P3", "P4"],
)

if selected_priority == "All Groups":
    filtered_customers = customers.copy()
else:
    filtered_customers = customers.loc[
        customers["priority_segment"] == selected_priority
    ].copy()


# Selected group metrics
group_count = len(filtered_customers)

group_value = filtered_customers[
    "historical_monetary"
].sum()

group_probability = filtered_customers[
    "predicted_probability"
].mean()

group_repeat_rate = filtered_customers[
    "repeat_purchase_90d"
].mean()

display_metric_row([
    {
        "label": "Customers",
        "value": f"{group_count:,}",
    },
    {
        "label": "Historical Purchase Value",
        "value": f"£{group_value:,.2f}",
    },
    {
        "label": "Mean Predicted Probability",
        "value": f"{group_probability:.2%}",
    },
    {
        "label": "Actual Repeat-Purchase Rate",
        "value": f"{group_repeat_rate:.2%}",
    },
])


st.divider()


# Priority group comparison
st.subheader("Priority Group Comparison")

priority_summary = (
    customers.groupby("priority_segment")
    .agg(
        customers=("Customer ID", "count"),
        historical_value=("historical_monetary", "sum"),
        mean_predicted_probability=(
            "predicted_probability",
            "mean",
        ),
        actual_repeat_rate=("repeat_purchase_90d", "mean"),
    )
    .reindex(["P1", "P2", "P3", "P4"])
    .reset_index()
)

left_col, right_col = st.columns(2)

with left_col:
    fig_customers = px.bar(
        priority_summary,
        x="priority_segment",
        y="customers",
        text="customers",
        color="priority_segment",
        color_discrete_map=PRIORITY_COLORS,
        category_orders={
            "priority_segment": ["P1", "P2", "P3", "P4"]
        },
        title="Customer Distribution by Priority",
        labels={
            "priority_segment": "Priority Group",
            "customers": "Customers",
        },
    )

    fig_customers.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
    )

    fig_customers = apply_chart_theme(fig_customers)

    st.plotly_chart(
        fig_customers,
        use_container_width=True,
    )


with right_col:
    fig_value = px.bar(
        priority_summary,
        x="priority_segment",
        y="historical_value",
        text="historical_value",
        color="priority_segment",
        color_discrete_map=PRIORITY_COLORS,
        category_orders={
            "priority_segment": ["P1", "P2", "P3", "P4"]
        },
        title="Historical Purchase Value by Priority",
        labels={
            "priority_segment": "Priority Group",
            "historical_value": "Historical Purchase Value (£)",
        },
    )

    fig_value.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside",
    )

    fig_value = apply_chart_theme(fig_value)

    st.plotly_chart(
        fig_value,
        use_container_width=True,
    )


# Priority summary table
st.subheader("Priority Group Performance")

st.dataframe(
    priority_summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "priority_segment": "Priority Group",
        "customers": st.column_config.NumberColumn(
            "Customers",
            format="%d",
        ),
        "historical_value": st.column_config.NumberColumn(
            "Historical Purchase Value",
            format="£%.2f",
        ),
        "mean_predicted_probability": st.column_config.NumberColumn(
            "Mean Predicted Probability",
            format="percent",
        ),
        "actual_repeat_rate": st.column_config.NumberColumn(
            "Actual Repeat-Purchase Rate",
            format="percent",
        ),
    },
)


st.divider()


# Scenario analysis
st.header("Retention Scenario Analysis")

scenario_definitions = {
    "Scenario A — P1 only": ["P1"],
    "Scenario B — P1 + P3": ["P1", "P3"],
    "Scenario C — P1 + P2": ["P1", "P2"],
    "Scenario D — All customers": ["P1", "P2", "P3", "P4"],
}

scenario_rows = []

for scenario_name, groups in scenario_definitions.items():
    scenario_df = customers.loc[
        customers["priority_segment"].isin(groups)
    ]

    scenario_rows.append(
        {
            "scenario": scenario_name,
            "customers": len(scenario_df),
            "customer_share": len(scenario_df) / total_customers,
            "historical_value": scenario_df[
                "historical_monetary"
            ].sum(),
            "mean_predicted_probability": scenario_df[
                "predicted_probability"
            ].mean(),
            "actual_repeat_rate": scenario_df[
                "repeat_purchase_90d"
            ].mean(),
        }
    )

scenario_df = pd.DataFrame(scenario_rows)

st.dataframe(
    scenario_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "scenario": "Scenario",
        "customers": st.column_config.NumberColumn(
            "Customers",
            format="%d",
        ),
        "customer_share": st.column_config.NumberColumn(
            "Customer Share",
            format="percent",
        ),
        "historical_value": st.column_config.NumberColumn(
            "Historical Purchase Value",
            format="£%.2f",
        ),
        "mean_predicted_probability": st.column_config.NumberColumn(
            "Mean Predicted Probability",
            format="percent",
        ),
        "actual_repeat_rate": st.column_config.NumberColumn(
            "Actual Repeat-Purchase Rate",
            format="percent",
        ),
    },
)


st.divider()


# Customer explorer
st.header("Customer Priority Explorer")

st.markdown(
    "Explore individual customers and their historical prioritization metrics."
)

display_df = filtered_customers[
    [
        "Customer ID",
        "snapshot_date",
        "recency_days",
        "historical_monetary",
        "predicted_probability",
        "repeat_purchase_90d",
        "priority_segment",
    ]
].copy()

display_df["Customer ID"] = (
    display_df["Customer ID"].astype("Int64")
)

st.dataframe(
    display_df.sort_values(
        "predicted_probability",
        ascending=True,
    ),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Customer ID": st.column_config.NumberColumn(
            "Customer ID",
            format="%d",
        ),
        "snapshot_date": st.column_config.DateColumn(
            "Snapshot Date"
        ),
        "recency_days": st.column_config.NumberColumn(
            "Recency (days)",
            format="%d",
        ),
        "historical_monetary": st.column_config.NumberColumn(
            "Historical Purchase Value",
            format="£%.2f",
        ),
        "predicted_probability": st.column_config.NumberColumn(
            "Predicted Repeat-Purchase Probability",
            format="percent",
        ),
        "repeat_purchase_90d": "Actual Repeat-Purchase Outcome",
        "priority_segment": "Priority Group",
    },
)


st.caption(
    """
    Priority groups use median historical monetary value and median
    predicted repeat-purchase probability as analytical thresholds.
    Historical purchase value is not profit or customer lifetime value.
    Scenario comparisons are descriptive and do not estimate causal
    retention impact, revenue saved, or intervention ROI.

    Results represent historical test-period observations, not live
    customer predictions.
    """
)
