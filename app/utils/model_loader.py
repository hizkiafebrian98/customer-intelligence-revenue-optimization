import joblib
import streamlit as st

from app.config import MODEL_PATH
from app.utils.data_validation import validate_file_exists


@st.cache_resource
def load_selected_model():
    """Load and cache the selected Logistic Regression pipeline."""

    validate_file_exists(
        MODEL_PATH,
        "Selected Logistic Regression model",
    )

    try:
        model = joblib.load(MODEL_PATH)

    except Exception as error:
        st.error(
            "The saved model could not be loaded. "
            "Check the model artifact and scikit-learn compatibility."
        )
        st.exception(error)
        st.stop()

    return model
