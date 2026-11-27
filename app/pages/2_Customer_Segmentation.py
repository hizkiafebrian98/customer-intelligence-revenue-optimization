
import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_customer_analytics,
    load_rfm_segment_profile,
    load_kmeans_cluster_profile,
)

from app.components.metrics import display_metric_row
from app.components.charts import apply_chart_theme


# Load datasets
customers = load_customer_analytics()
rfm_profile = load_rfm_segment_profile()
kmeans_profile = load_kmeans_cluster_profile()


# Page heading
st.title(":material/groups: Customer Segmentation")

st.markdown(
    """
    Explore customer purchasing behavior through rule-based RFM
    segmentation and complementary K-Means clustering.
    """
)

st.caption(
    "Historical customer analysis | Observation date: 10 December 2011"
)


# RFM segmentation
st.header("RFM Segmentation")

st.markdown(
    """
    RFM segmentation classifies customers using Recency, Frequency,
    and Monetary value. The six segments provide an interpretable
    framework for understanding customer engagement and value.
    """
)


# Segment filter
segment_options = ["All Segments"] + sorted(
    customers["rfm_segment"].dropna().unique().tolist()
)

selected_segment = st.selectbox(
    "Select RFM Segment",
    segment_options,
)

if selected_segment == "All Segments":
    filtered_customers = customers.copy()
else:
    filtered_customers = customers.loc[
        customers["rfm_segment"] == selected_segment
    ].copy()


# Selected population metrics
customer_count = len(filtered_customers)

segment_revenue = filtered_customers["monetary"].sum()

median_recency = filtered_customers["recency"].median()

median_frequency = filtered_customers["frequency"].median()

display_metric_row([
    {
        "label": "Customers",
        "value": f"{customer_count:,}",
    },
    {
        "label": "Qualifying Purchase Revenue",
        "value": f"£{segment_revenue:,.2f}",
    },
    {
        "label": "Median Recency",
        "value": f"{median_recency:.0f} days",
    },
    {
        "label": "Median Purchase Frequency",
        "value": f"{median_frequency:.1f}",
    },
])


st.divider()


# Customer behavior visualization
st.subheader("Customer Behavior")

left_col, right_col = st.columns(2)

with left_col:
    fig_recency = px.histogram(
        filtered_customers,
        x="recency",
        nbins=30,
        title="Customer Recency Distribution",
        labels={
            "recency": "Recency (days)",
            "count": "Number of Customers",
        },
    )

    fig_recency = apply_chart_theme(fig_recency)

    st.plotly_chart(
        fig_recency,
        use_container_width=True,
    )


with right_col:
    fig_frequency = px.histogram(
        filtered_customers,
        x="frequency",
        nbins=30,
        title="Purchase Frequency Distribution",
        labels={
            "frequency": "Number of Invoices",
            "count": "Number of Customers",
        },
    )

    fig_frequency = apply_chart_theme(fig_frequency)

    st.plotly_chart(
        fig_frequency,
        use_container_width=True,
    )


# Customer-level scatter plot
st.subheader("Customer Value and Engagement")

fig_scatter = px.scatter(
    filtered_customers,
    x="recency",
    y="monetary",
    color="rfm_segment",
    hover_data=[
        "Customer ID",
        "frequency",
        "unique_products",
        "cancellation_value",
    ],
    log_y=True,
    title="Recency vs. Qualifying Purchase Value",
    labels={
        "recency": "Recency (days)",
        "monetary": "Qualifying Purchase Value (£, log scale)",
        "rfm_segment": "RFM Segment",
    },
)

fig_scatter = apply_chart_theme(fig_scatter)

st.plotly_chart(
    fig_scatter,
    use_container_width=True,
)


# Customer-level records
st.subheader("Customer Explorer")

st.markdown(
    "Review individual customer metrics within the selected population."
)

display_df = filtered_customers[
    [
        "Customer ID",
        "rfm_segment",
        "recency",
        "frequency",
        "monetary",
        "unique_products",
        "cancellation_value",
        "cancellation_value_ratio",
    ]
].copy()

display_df["Customer ID"] = (
    display_df["Customer ID"].astype("Int64")
)

st.dataframe(
    display_df.sort_values(
        "monetary",
        ascending=False,
    ),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Customer ID": st.column_config.NumberColumn(
            "Customer ID",
            format="%d",
        ),
        "rfm_segment": "RFM Segment",
        "recency": st.column_config.NumberColumn(
            "Recency (days)",
            format="%d",
        ),
        "frequency": st.column_config.NumberColumn(
            "Purchase Frequency",
            format="%d",
        ),
        "monetary": st.column_config.NumberColumn(
            "Qualifying Purchase Value",
            format="£%.2f",
        ),
        "unique_products": st.column_config.NumberColumn(
            "Unique Products",
            format="%d",
        ),
        "cancellation_value": st.column_config.NumberColumn(
            "Cancellation Value",
            format="£%.2f",
        ),
        "cancellation_value_ratio": st.column_config.NumberColumn(
            "Cancellation-to-Purchase-Value Ratio",
            format="%.2f",
        ),
    },
)


st.divider()


# K-Means analysis
st.header("K-Means Clustering")

st.markdown(
    """
    K-Means provides a complementary data-driven grouping of customers.
    The four clusters below are based on the Phase 6 clustering analysis.
    Cluster labels are numerical identifiers, not ordinal rankings.
    """
)


fig_clusters = px.bar(
    kmeans_profile.sort_values(
        "customers",
        ascending=True,
    ),
    x="customers",
    y="kmeans_cluster",
    orientation="h",
    text="customers",
    title="Customer Distribution by K-Means Cluster",
    labels={
        "customers": "Number of Customers",
        "kmeans_cluster": "K-Means Cluster",
    },
)

fig_clusters.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside",
)

fig_clusters = apply_chart_theme(fig_clusters)

st.plotly_chart(
    fig_clusters,
    use_container_width=True,
)


st.subheader("K-Means Cluster Profiles")

st.dataframe(
    kmeans_profile,
    use_container_width=True,
    hide_index=True,
)


st.caption(
    """
    RFM and K-Means are different segmentation methods.
    RFM segments are rule-based and interpretable, while K-Means
    identifies groups based on feature similarity. Monetary values
    represent historical qualifying purchase value, not profit or
    customer lifetime value.
    """
)
