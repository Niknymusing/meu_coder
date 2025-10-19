"""Tests for health check endpoint."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert data["version"] == "0.1.0"


def test_health_check_returns_json(client: TestClient):
    """Test that health check returns proper JSON content type."""
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
