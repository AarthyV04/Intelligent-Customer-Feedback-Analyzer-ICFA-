from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_feedback_upload():

    csv_content = "feedback\nGreat service\nBad delivery"

    response = client.post(
        "/feedback/analyze",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.status_code == 200
    assert "results" in response.json()