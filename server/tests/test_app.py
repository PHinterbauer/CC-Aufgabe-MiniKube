from app.core import add
from app.main import app
from fastapi.testclient import TestClient


def test_add():
    assert add(2, 3) == 5


def test_health():
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": {"add": "ok", "metrics": "ok"},
        "errors": {},
    }


def test_metrics():
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")
