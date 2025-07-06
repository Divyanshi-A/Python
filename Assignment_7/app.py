import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("final_best_model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(
    page_title="Customer Value Prediction",
    layout="centered"
)

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #fff8f0;
    }
    .main {
        background-color: #fff8f0;
    }
    .stButton>button {
        background-color: #f4a261;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #e76f51;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #fefae0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar explanation
st.sidebar.header("About RFM Score")
st.sidebar.markdown(
    """
**RFM Score** summarizes customer behavior:

- **Recency**: How recently a purchase was made.
- **Frequency**: How often purchases occur.
- **Monetary**: Average spending.

Each dimension is scored from 1 to 5:

- **Recency Score**
  - ≤30 days = 5
  - 31–60 = 4
  - 61–180 = 3
  - 181–365 = 2
  - >365 = 1
- **Frequency Score**
  - ≥50 = 5
  - 25–49 = 4
  - 10–24 = 3
  - 5–9 = 2
  - <5 = 1
- **Monetary Score**
  - ≥500 = 5
  - 250–499 = 4
  - 100–249 = 3
  - 50–99 = 2
  - <50 = 1

**Final RFM Score = Average of the 3 scores**, rounded to nearest whole number.
"""
)

st.title("Customer High-Value Prediction")

st.write(
    "Enter customer metrics below. The model will predict whether the customer is likely high-value."
)

# Input fields
recency_days = st.number_input(
    "Recency (days since last purchase)",
    min_value=0,
    max_value=3650,
    value=90
)

frequency_transactions = st.number_input(
    "Frequency (total transactions)",
    min_value=0,
    max_value=500,
    value=10
)

monetary_avg = st.number_input(
    "Monetary Average per Transaction",
    min_value=0.0,
    value=100.0
)

customer_lifetime_days = st.number_input(
    "Customer Lifetime (days)",
    min_value=0,
    max_value=5000,
    value=365
)

# Compute RFM Score
def compute_rfm_score(recency, frequency, monetary):
    # Recency score
    if recency <= 30:
        r_score = 5
    elif recency <= 60:
        r_score = 4
    elif recency <= 180:
        r_score = 3
    elif recency <= 365:
        r_score = 2
    else:
        r_score = 1

    # Frequency score
    if frequency >= 50:
        f_score = 5
    elif frequency >= 25:
        f_score = 4
    elif frequency >= 10:
        f_score = 3
    elif frequency >= 5:
        f_score = 2
    else:
        f_score = 1

    # Monetary score
    if monetary >= 500:
        m_score = 5
    elif monetary >= 250:
        m_score = 4
    elif monetary >= 100:
        m_score = 3
    elif monetary >= 50:
        m_score = 2
    else:
        m_score = 1

    return round((r_score + f_score + m_score) / 3)

rfm_score = compute_rfm_score(recency_days, frequency_transactions, monetary_avg)

st.write(f"Calculated RFM Score: **{rfm_score}**")

# Prepare input for prediction
inputs = [
    recency_days,
    frequency_transactions,
    monetary_avg,
    customer_lifetime_days,
    rfm_score
]

# Ensure correct feature order
feature_names = scaler.feature_names_in_
input_df = pd.DataFrame([inputs], columns=feature_names)

if st.button("Predict"):
    input_scaled = scaler.transform(input_df)
    pred_class = model.predict(input_scaled)[0]
    pred_proba = model.predict_proba(input_scaled)[0][1]

    if pred_class == 1:
        st.success(
            f"Prediction: High-Value Customer\nProbability: {pred_proba:.2%}"
        )
    else:
        st.info(
            f"Prediction: Standard-Value Customer\nProbability: {pred_proba:.2%}"
        )

    if hasattr(model, "feature_importances_"):
        st.subheader("Feature Importance")
        importance = pd.Series(
            model.feature_importances_,
            index=feature_names
        ).sort_values(ascending=False)
        st.bar_chart(importance)
