
import streamlit as st


st.set_page_config(
    page_title="Customer Intelligence & Revenue Optimization",
    page_icon=":material/analytics:",
    layout="wide",
)

pages = [
    st.Page(
        "pages/1_Executive_Overview.py",
        title="Executive Overview",
        icon=":material/dashboard:",
        default=True,
    ),
    st.Page(
        "pages/2_Customer_Segmentation.py",
        title="Customer Segmentation",
        icon=":material/groups:",
    ),
    st.Page(
        "pages/3_Repeat_Purchase_Prediction.py",
        title="Repeat-Purchase Prediction",
        icon=":material/psychology:",
    ),
    st.Page(
        "pages/4_Retention_Prioritization.py",
        title="Retention Prioritization",
        icon=":material/track_changes:",
    ),
]

pg = st.navigation(pages)
pg.run()
