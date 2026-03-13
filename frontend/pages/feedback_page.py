import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

def show():
    st.title("💬 Sentiment Analysis")
    st.markdown(
        "Upload a CSV with a column named: `review`, `feedback`, `comment`, or `text`"
    )
    st.divider()

    uploaded_file = st.file_uploader("📂 Upload CSV file", type=["csv"])

    if uploaded_file:
        df_preview = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        st.markdown("**Preview (first 5 rows):**")
        st.dataframe(df_preview.head(), use_container_width=True)
        st.markdown(f"Total rows: `{len(df_preview)}`")
        st.divider()

        if st.button("🔍 Analyze Sentiment", use_container_width=True):
            try:
                with st.spinner("Analyzing... (first run may take 1-2 mins to load the model)"):
                    response = requests.post(
                        f"{API_URL}/feedback/analyze",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")},
                        timeout=120
                    )
                if response.status_code == 200:
                    st.session_state.analysis_results = response.json()
                else:
                    st.error(f"API Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.warning("⚠️ Backend not running. Showing mock results for UI demo.")
                st.session_state.analysis_results = mock_result()

    if 'analysis_results' in st.session_state:
        show_results(st.session_state.analysis_results)


def show_results(data):
    st.success(f"✅ Analyzed {data['total']} reviews!")

    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Positive", data["positive"])
    col2.metric("❌ Negative", data["negative"])
    col3.metric("😐 Neutral",  data["neutral"])
    st.divider()

    col_chart, col_kw = st.columns(2)

    with col_chart:
        st.subheader("Sentiment Split")
        labels, sizes, colors = [], [], []
        for label, count, color in [
            ("Positive", data["positive"], "#31F738"),
            ("Negative", data["negative"], "#D82114"),
            ("Neutral",  data["neutral"],  "#8C7777"),
        ]:
            if count > 0:
                labels.append(label)
                sizes.append(count)
                colors.append(color)
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%")
        st.pyplot(fig)

    with col_kw:
        st.subheader("Top Keywords")
        kw_df = pd.DataFrame(data["keywords"])
        if not kw_df.empty:
            st.bar_chart(kw_df.set_index("word")["count"])

    st.divider()
    st.subheader("All Review Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_filter = st.selectbox(
            "Filter by sentiment",
            ["All", "Positive", "Negative", "Neutral"],
            key="sentiment_filter"
        )
    
    with col2:
        sort_order = st.selectbox(
            "Sort by sentiment score",
            ["Descending (High to Low)", "Ascending (Low to High)"],
            key="sort_order"
        )
    
    results_df = pd.DataFrame(data["results"])
    
    if sentiment_filter != "All":
        results_df = results_df[results_df["label"] == sentiment_filter.upper()]
    
    ascending = sort_order == "Ascending (Low to High)"
    results_df = results_df.sort_values("score", ascending=ascending)
    
    st.dataframe(results_df, use_container_width=True)


def mock_result():
    return {
        "total": 5, "positive": 3, "negative": 1, "neutral": 1,
        "results": [
            {"review": "Great product!",  "label": "POSITIVE", "score": 0.99},
            {"review": "Worst ever.",     "label": "NEGATIVE", "score": 0.97},
            {"review": "It was okay.",    "label": "POSITIVE", "score": 0.61},
            {"review": "Love it!",        "label": "POSITIVE", "score": 0.98},
            {"review": "Not bad.",        "label": "NEUTRAL",  "score": 0.55},
        ],
        "keywords": [
            {"word": "great",   "count": 5},
            {"word": "product", "count": 4},
            {"word": "love",    "count": 3},
        ]
    }

