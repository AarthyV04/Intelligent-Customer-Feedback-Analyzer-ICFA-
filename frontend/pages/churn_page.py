import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


def show():
    st.title("📉 Churn Prediction")
    st.markdown(
        "Upload a CSV with columns: "
        "`tenure`, `MonthlyCharges`, `TotalCharges`, "
        "`Contract`, `PaymentMethod`, `InternetService`"
    )
    st.info("💡 Use the Telco Customer Churn dataset from Kaggle to test this")
    st.divider()

    uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

    if uploaded_file:
        df_preview = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        st.markdown("**Preview:**")
        st.dataframe(df_preview.head(), use_container_width=True)
        st.divider()

        if st.button("📉 Predict Churn", use_container_width=True):
            try:
                with st.spinner("Predicting..."):
                    response = requests.post(
                        f"{API_URL}/churn/predict",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")},
                        timeout=60
                    )
                if response.status_code == 200:
                    show_churn_results(response.json())
                else:
                    st.error(f"API Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend not running. Showing mock results for UI demo.")
                show_churn_results(mock_churn())


def show_churn_results(data):
    if "error" in data:
        st.error(data["error"])
        return

    st.success("✅ Prediction complete!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", data["total_customers"])
    col2.metric("Will Churn",      data["predicted_churn"])
    col3.metric("Churn Rate",      f"{data['churn_rate']}%")
    st.divider()

    st.subheader("Customer-wise Predictions")
    df = pd.DataFrame(data["predictions"])

    def color_churn(row):
        if row["churn_prediction"] == "Yes":
            return ["background-color: #ff2c00"] * len(row)
        return ["background-color: #00de03"] * len(row)

    st.dataframe(df.style.apply(color_churn, axis=1), use_container_width=True)


def mock_churn():
    return {
        "total_customers": 5,
        "predicted_churn": 2,
        "churn_rate": 40.0,
        "predictions": [
            {"customer_index": 1, "churn_prediction": "Yes", "churn_probability": 0.82, "risk_level": "High"},
            {"customer_index": 2, "churn_prediction": "No",  "churn_probability": 0.12, "risk_level": "Low"},
            {"customer_index": 3, "churn_prediction": "Yes", "churn_probability": 0.76, "risk_level": "High"},
            {"customer_index": 4, "churn_prediction": "No",  "churn_probability": 0.09, "risk_level": "Low"},
            {"customer_index": 5, "churn_prediction": "No",  "churn_probability": 0.33, "risk_level": "Medium"},
        ]
    }

