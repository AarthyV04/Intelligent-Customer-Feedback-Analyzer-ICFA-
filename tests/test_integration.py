from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_full_workflow():

    login_response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    csv_content = """feedback
Great service
Bad delivery
Customer support was helpful
"""

    response = client.post(
        "/feedback/analyze",
        files={"file": ("test.csv", csv_content, "text/csv")},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert "total" in data
