import streamlit as st


def show():
    st.sidebar.title(f"👤 {st.session_state.username}")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "💬 Sentiment Analysis", "📉 Churn Prediction"]
    )

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.rerun()

    if page == "🏠 Home":
        show_home()
    elif page == "💬 Sentiment Analysis":
        from frontend.pages import feedback_page
        feedback_page.show()
    elif page == "📉 Churn Prediction":
        from frontend.pages import churn_page
        churn_page.show()


def show_home():
    st.title("📊 ICFA Dashboard")
    st.markdown("### Intelligent Customer Feedback Analyzer")
    st.divider()
    st.markdown("#### What can this tool do?")
    col1, col2 = st.columns(2)
    with col1:
        st.success(
            "**💬 Sentiment Analysis**\n\n"
            "- Upload customer reviews (CSV)\n"
            "- Get Positive / Negative / Neutral split\n"
            "- See top keywords from reviews\n"
            "- Powered by HuggingFace DistilBERT"
        )
    with col2:
        st.info(
            "**📉 Churn Prediction**\n\n"
            "- Upload customer data (CSV)\n"
            "- Predict who will leave\n"
            "- See churn probability per customer\n"
            "- Powered by Random Forest ML model"
        )
    st.divider()
    st.markdown("#### How to use:")
    st.markdown("1. Click a page from the left sidebar")
    st.markdown("2. Upload your CSV file")
    st.markdown("3. Click the Analyze / Predict button")
    st.markdown("4. View results and charts")

