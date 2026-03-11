from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_churn_predict():

    csv_content = """tenure,MonthlyCharges,TotalCharges,Contract,PaymentMethod,InternetService
12,70,840,Month-to-month,Electronic check,Fiber optic
24,60,1440,One year,Credit card,DSL
"""

    response = client.post(
        "/churn/predict",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200
    assert "total_customers" in response.json()