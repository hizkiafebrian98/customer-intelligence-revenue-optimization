
import plotly.io as pio


# Corporate brand palette
CHART_COLORS = [
    "#203B5C",
    "#52769C",
    "#7898B8",
    "#A9BED2",
    "#CBD8E5",
    "#64748B",
]


# Qualitative palette for categorical visualizations
RFM_SEGMENT_COLORS = {
    "Champions": "#0072B2",
    "At-risk valuable": "#D55E00",
    "Loyal customers": "#009E73",
    "Recent high-value": "#CC79A7",
    "Hibernating": "#E69F00",
    "Other customers": "#56B4E9",
}


# Retention priority colors
PRIORITY_COLORS = {
    "P1": "#D55E00",
    "P2": "#0072B2",
    "P3": "#E69F00",
    "P4": "#009E73",
}


def apply_chart_theme(fig):
    """Apply the shared Enterprise Blue theme to a Plotly figure."""

    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="Inter, sans-serif",
            color="#203B5C",
            size=13,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=CHART_COLORS,
        title_font=dict(
            family="Inter, sans-serif",
            size=18,
            color="#203B5C",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#52769C"),
        ),
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20,
        ),
    )

    # Apply consistent colors to existing traces.
    bar_index = 0

    for trace in fig.data:

        if trace.type == "bar":

            if trace.name in PRIORITY_COLORS:
                trace.marker.color = PRIORITY_COLORS[trace.name]

            else:
                trace.marker.color = CHART_COLORS[
                    bar_index % len(CHART_COLORS)
                ]
                bar_index += 1

        elif trace.type == "histogram":
            trace.marker.color = CHART_COLORS[0]

        elif trace.type in ["scatter", "scattergl"]:

            if trace.name in RFM_SEGMENT_COLORS:
                trace.marker.color = RFM_SEGMENT_COLORS[trace.name]

            else:
                trace.marker.color = CHART_COLORS[0]

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E5EBF1",
        zerolinecolor="#D5DEE8",
        linecolor="#D5DEE8",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#203B5C"),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5EBF1",
        zerolinecolor="#D5DEE8",
        linecolor="#D5DEE8",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#203B5C"),
    )

    return fig


pio.templates.default = "plotly_white"
