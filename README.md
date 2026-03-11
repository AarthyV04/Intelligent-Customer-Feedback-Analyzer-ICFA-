# ICFA — Intelligent Customer Feedback Analyzer

A Python-based tool that analyzes customer feedback using sentiment analysis and predicts customer churn.

---

## Team Roles

| Person | Role | Branch |
|--------|------|--------|
| Person 1 | Frontend (Streamlit) | `p1-frontend` |
| Person 2 | Backend (FastAPI) | `p2-backend` |
| Person 3 | Sentiment Analysis (HuggingFace) | `p3-sentiment` |
| Person 4 | Churn Prediction (Random Forest) | `p4-churn` |

---

## Project Structure

```
ICFA/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── auth.py              # Login & JWT token logic
│   ├── routes/
│   │   ├── feedback.py      # Sentiment analysis endpoint
│   │   └── churn.py         # Churn prediction endpoint
│   └── utils/
│       ├── sentiment.py     # HuggingFace model logic
│       └── churn_model.py   # Churn ML model logic
├── frontend/
│   ├── app.py               # Streamlit entry point
│   └── pages/
│       ├── login.py         # Login page
│       ├── dashboard.py     # Sidebar + navigation
│       ├── feedback_page.py # Sentiment analysis UI
│       └── churn_page.py    # Churn prediction UI
├── ml/
│   ├── train_churn.py           # Train & save churn model
│   ├── explore_data.py          # EDA script (Day 1/2)
│   ├── test_sentiment.py        # Standalone model test
│   ├── test_sentiment_module.py # Module test
│   ├── test_full_sentiment_api.py # End-to-end API test
│   ├── churn_model.pkl          # Saved model (after training)
│   └── sample_data/
│       ├── sample_reviews.csv   # Test reviews CSV
│       └── churn_data.csv       # Kaggle dataset (add manually)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ICFA.git
cd ICFA
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Churn Dataset
- Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Download `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- Save it as `ml/sample_data/churn_data.csv`

### 4. Train the churn model (run once)
```bash
python ml/train_churn.py
```

---

## Running the App

Open **two terminals**:

**Terminal 1 — Backend (FastAPI):**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend (Streamlit):**
```bash
streamlit run frontend/app.py
```

Open browser: http://localhost:8501

---

## Login Credentials

| Username | Password |
|----------|----------|
| admin    | admin123 |
| user1    | pass123  |

---

## API Docs

FastAPI auto-generates interactive API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:       http://127.0.0.1:8000/redoc

---

## Features

- **Sentiment Analysis**: Upload a CSV with customer reviews → get Positive/Negative/Neutral breakdown + top keywords
- **Churn Prediction**: Upload customer data CSV → predict which customers are likely to leave, with probability scores and risk levels

---

## Daily Git Workflow

```bash
git pull origin main          # get latest
git checkout -b your-branch   # your branch
git add .                     # stage changes
git commit -m "what you did"  # commit
git push origin your-branch   # push
# Then create Pull Request on GitHub
```
