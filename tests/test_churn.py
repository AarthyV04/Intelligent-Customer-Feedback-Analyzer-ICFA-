from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_churn_success():

    csv_content = """tenure,MonthlyCharges,TotalCharges,Contract,PaymentMethod,InternetService
12,70,840,Month-to-month,Electronic check,Fiber optic
24,60,1440,One year,Credit card,DSL
"""

    response = client.post(
        "/churn/predict",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_customers" in data
    assert "churn_rate" in data


def test_churn_wrong_file():

    response = client.post(
        "/churn/predict",
        files={"file": ("test.txt", "invalid", "text/plain")}
    )

    assert response.status_code == 400
    assert "Only CSV files allowed" in response.json()["detail"]


def test_churn_missing_columns():

    csv_content = """id,value
1,10
2,20
"""

    response = client.post(
        "/churn/predict",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    data = response.json()

    assert "error" in data