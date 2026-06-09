import pytest
from fastapi.testclient import TestClient

from app.core import add
from app.main import app, users_db


@pytest.fixture(autouse=True)
def clear_users_db():
    users_db.clear()
    yield
    users_db.clear()


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


def test_create_update_delete_user_routes():
    client = TestClient(app)

    create_response = client.post(
        "/api/users/1",
        json={"name": "Anna", "age": 31, "email": "anna@example.com"},
    )
    assert create_response.status_code == 200
    assert create_response.json() == {
        "nachricht": "Benutzer erfolgreich angelegt",
        "benutzer": {"name": "Anna", "age": 31, "email": "anna@example.com"},
    }

    update_response = client.put(
        "/api/users/1",
        json={"name": "Anna Meyer", "age": 32, "email": "anna.meyer@example.com"},
    )
    assert update_response.status_code == 200
    assert update_response.json() == {
        "nachricht": "Benutzer erfolgreich bearbeitet",
        "benutzer": {
            "name": "Anna Meyer",
            "age": 32,
            "email": "anna.meyer@example.com",
        },
    }

    delete_response = client.delete("/api/users/1")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"nachricht": "Benutzer erfolgreich gelöscht"}

    metrics_response = client.get("/metrics")
    assert metrics_response.status_code == 200
    metrics_text = metrics_response.text
    assert 'path="/api/users/1"' in metrics_text
    assert 'method="POST"' in metrics_text
    assert 'method="PUT"' in metrics_text
    assert 'method="DELETE"' in metrics_text
