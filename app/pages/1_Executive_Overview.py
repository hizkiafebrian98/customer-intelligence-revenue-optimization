
import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_customer_analytics,
    load_rfm_segment_profile,
)

from components.metrics import display_metric_row
from components.charts import apply_chart_theme


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

customers = load_customer_analytics()
rfm_profile = load_rfm_segment_profile()


# --------------------------------------------------
# Page heading
# --------------------------------------------------

st.title(":material/dashboard: Customer Intelligence & Revenue Optimization")

st.markdown(
    """
    Analyze customer purchasing behavior, revenue concentration,
    and retention opportunities using historical retail transaction data.
    """
)

st.caption(
    "Historical analysis | Observation period ending 10 December 2011"
)


# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_customers = customers["Customer ID"].nunique()
total_revenue = customers["monetary"].sum()
median_recency = customers["recency"].median()

customers_with_cancellations = (
    customers["cancellation_value"] > 0
).sum()

top_segment = rfm_profile.loc[
    rfm_profile["rfm_segment"] == "Champions"
].iloc[0]


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

display_metric_row([
    {
        "label": "Identified Customers",
        "value": f"{total_customers:,.0f}",
    },
    {
        "label": "Qualifying Purchase Revenue",
        "value": f"£{total_revenue:,.2f}",
    },
    {
        "label": "Median Recency",
        "value": f"{median_recency:.0f} days",
    },
    {
        "label": "Customers with Cancellations",
        "value": f"{customers_with_cancellations:,.0f}",
    },
])


st.divider()


# --------------------------------------------------
# Customer Segment Overview
# --------------------------------------------------

st.subheader("Customer Segment Overview")

left_col, right_col = st.columns(2)

with left_col:
    fig_customers = px.bar(
        rfm_profile.sort_values(
            "customers",
            ascending=True,
        ),
        x="customers",
        y="rfm_segment",
        orientation="h",
        title="Customers by RFM Segment",
        labels={
            "rfm_segment": "Customer Segment",
            "customers": "Number of Customers",
        },
        text="customers",
    )

    fig_customers.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
    )

    fig_customers.update_layout(
        yaxis_title=None,
        xaxis_title="Number of Customers",
    )

    fig_customers = apply_chart_theme(fig_customers)

    st.plotly_chart(
        fig_customers,
        use_container_width=True,
    )


with right_col:
    fig_revenue = px.bar(
        rfm_profile.sort_values(
            "total_purchase_value",
            ascending=True,
        ),
        x="total_purchase_value",
        y="rfm_segment",
        orientation="h",
        title="Purchase Revenue by RFM Segment",
        labels={
            "rfm_segment": "Customer Segment",
            "total_purchase_value": "Purchase Revenue (£)",
        },
        text="total_purchase_value",
    )

    fig_revenue.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside",
    )

    fig_revenue.update_layout(
        yaxis_title=None,
        xaxis_title="Purchase Revenue (£)",
    )

    fig_revenue = apply_chart_theme(fig_revenue)

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
    )


# --------------------------------------------------
# RFM Segment Performance
# --------------------------------------------------

st.subheader("RFM Segment Performance")

display_columns = [
    "rfm_segment",
    "customers",
    "total_purchase_value",
    "total_cancellation_value",
    "median_recency",
    "median_frequency",
]

display_df = rfm_profile[display_columns].sort_values(
    "total_purchase_value",
    ascending=False,
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "rfm_segment": st.column_config.TextColumn(
            "Customer Segment"
        ),
        "customers": st.column_config.NumberColumn(
            "Customers",
            format="%d",
        ),
        "total_purchase_value": st.column_config.NumberColumn(
            "Qualifying Purchase Revenue",
            format="£%.2f",
        ),
        "total_cancellation_value": st.column_config.NumberColumn(
            "Cancellation Value",
            format="£%.2f",
        ),
        "median_recency": st.column_config.NumberColumn(
            "Median Recency (days)",
            format="%.1f",
        ),
        "median_frequency": st.column_config.NumberColumn(
            "Median Purchase Frequency",
            format="%.1f",
        ),
    },
)


# --------------------------------------------------
# Business Interpretation
# --------------------------------------------------

st.subheader("Key Business Observations")

champions_share = (
    top_segment["total_purchase_value"] / total_revenue
) * 100

at_risk = rfm_profile.loc[
    rfm_profile["rfm_segment"] == "At-risk valuable"
].iloc[0]

hibernating = rfm_profile.loc[
    rfm_profile["rfm_segment"] == "Hibernating"
].iloc[0]

st.markdown(
    f"""
    **1. Revenue concentration**

    Champions represent {champions_share:.2f}% of qualifying
    purchase revenue, despite accounting for only
    {top_segment["customers"] / total_customers * 100:.2f}%
    of identified customers. Maintaining these relationships
    is an important revenue-protection priority.

    **2. Valuable customers with declining engagement**

    The At-risk valuable segment contains
    {int(at_risk["customers"]):,} customers and contributes
    £{at_risk["total_purchase_value"]:,.2f} in qualifying
    purchase revenue. Its median recency is
    {at_risk["median_recency"]:.1f} days, making it a relevant
    segment for targeted retention analysis.

    **3. Large inactive customer population**

    The Hibernating segment contains
    {int(hibernating["customers"]):,} customers, with median
    recency of {hibernating["median_recency"]:.0f} days.
    Its historical revenue contribution is comparatively small,
    suggesting that broad, high-cost retention efforts may not
    be the most efficient approach.

    **4. Cancellation monitoring**

    {customers_with_cancellations:,} customers have recorded
    cancellation value greater than zero. These records warrant
    monitoring, but cancellation values should not automatically
    be interpreted as confirmed refunds or lost revenue.
    """
)


# --------------------------------------------------
# Methodological Note
# --------------------------------------------------

st.caption(
    """
    Revenue represents qualifying historical purchase value, not profit
    or customer lifetime value. RFM segments are rule-based analytical
    classifications. Cancellation values are reported separately and
    are not treated as confirmed refunds against specific purchases.
    """
)
