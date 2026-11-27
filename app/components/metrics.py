
import html
import streamlit as st


def display_metric_row(metrics):
    columns = st.columns(len(metrics))

    for column, metric in zip(columns, metrics):
        with column:
            label = html.escape(str(metric["label"]))
            value = html.escape(str(metric["value"]))

            delta = metric.get("delta")
            delta_html = ""

            if delta is not None:
                delta_text = str(delta)
                escaped_delta = html.escape(delta_text)

                if delta_text.strip().startswith("-"):
                    delta_color = "#C45B5B"
                elif delta_text.strip().startswith("+"):
                    delta_color = "#16866A"
                else:
                    delta_color = "#64748B"

                delta_html = f"""
                    <div style="
                        margin-top: 12px;
                        font-size: 12px;
                        font-weight: 600;
                        color: {delta_color};
                    ">
                        {escaped_delta}
                    </div>
                """

            st.html(
                f"""
                <div style="
                    background-color: #FFFFFF;
                    border: 1px solid #E2E8F0;
                    border-top: 3px solid #52769C;
                    border-radius: 10px;
                    padding: 20px 18px;
                    min-height: 120px;
                    box-shadow: 0 2px 8px rgba(32, 59, 92, 0.045);
                    box-sizing: border-box;
                ">
                    <div style="
                        color: #64748B;
                        font-size: 11px;
                        font-weight: 600;
                        letter-spacing: 0.7px;
                        text-transform: uppercase;
                        margin-bottom: 16px;
                        line-height: 1.4;
                    ">
                        {label}
                    </div>

                    <div style="
                        color: #203B5C;
                        font-size: 30px;
                        font-weight: 700;
                        line-height: 1.2;
                        letter-spacing: -0.8px;
                        overflow-wrap: anywhere;
                    ">
                        {value}
                    </div>

                    {delta_html}
                </div>
                """
            )
