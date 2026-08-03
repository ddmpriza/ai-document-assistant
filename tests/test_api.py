from fastapi.testclient import TestClient

from app.main import app

"""
    Verify that the health endpoint returns HTTP 200.
"""

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }