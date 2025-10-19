"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    """Reset in-memory data before each test."""
    from app.api.endpoints import users, items

    users.users_db.clear()
    users.user_id_counter = 1
    items.items_db.clear()
    items.item_id_counter = 1

    yield

    users.users_db.clear()
    users.user_id_counter = 1
    items.items_db.clear()
    items.item_id_counter = 1
