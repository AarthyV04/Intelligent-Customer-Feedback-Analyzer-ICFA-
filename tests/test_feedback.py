from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_feedback_success():

    csv_content = """feedback
Great service
Bad delivery
Customer support was helpful
"""

    response = client.post(
        "/feedback/analyze",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "results" in data
    assert isinstance(data["results"], list)



def test_feedback_wrong_file():

    response = client.post(
        "/feedback/analyze",
        files={"file": ("test.txt", "invalid data", "text/plain")}
    )

    assert response.status_code == 400
    assert "Only CSV files allowed" in response.json()["detail"]



def test_feedback_no_text_column():

    csv_content = """id,value
1,100
2,200
"""

    response = client.post(
        "/feedback/analyze",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 400
    assert "No text column found" in response.json()["detail"]