from fastapi.testclient import TestClient

from app.main import app
"""
    Verify that the health check endpoint returns the expected response.
    This test checks that the /health endpoint returns a 200 status code and the expected JSON response.
"""
# Create a TestClient instance for the FastAPI application
client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
