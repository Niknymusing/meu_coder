"""Tests for user endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "securepassword123"
    }

    response = client.post("/api/users/", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_username(client: TestClient):
    """Test creating user with duplicate username fails."""
    user_data = {
        "email": "test1@example.com",
        "username": "testuser",
        "password": "securepassword123"
    }

    # Create first user
    client.post("/api/users/", json=user_data)

    # Try to create second user with same username
    user_data["email"] = "test2@example.com"
    response = client.post("/api/users/", json=user_data)

    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]


def test_create_user_invalid_email(client: TestClient):
    """Test creating user with invalid email fails."""
    user_data = {
        "email": "invalid-email",
        "username": "testuser",
        "password": "securepassword123"
    }

    response = client.post("/api/users/", json=user_data)

    assert response.status_code == 422


def test_create_user_short_password(client: TestClient):
    """Test creating user with short password fails."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "short"
    }

    response = client.post("/api/users/", json=user_data)

    assert response.status_code == 422


def test_get_users(client: TestClient):
    """Test getting list of users."""
    # Create test users
    for i in range(3):
        client.post("/api/users/", json={
            "email": f"test{i}@example.com",
            "username": f"testuser{i}",
            "password": "securepassword123"
        })

    response = client.get("/api/users/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["users"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 10


def test_get_users_pagination(client: TestClient):
    """Test user list pagination."""
    # Create 5 users
    for i in range(5):
        client.post("/api/users/", json={
            "email": f"test{i}@example.com",
            "username": f"testuser{i}",
            "password": "securepassword123"
        })

    # Get page 1 with 2 items
    response = client.get("/api/users/?page=1&page_size=2")
    data = response.json()

    assert response.status_code == 200
    assert data["total"] == 5
    assert len(data["users"]) == 2
    assert data["page"] == 1

    # Get page 2
    response = client.get("/api/users/?page=2&page_size=2")
    data = response.json()

    assert response.status_code == 200
    assert len(data["users"]) == 2
    assert data["page"] == 2


def test_get_user_by_id(client: TestClient):
    """Test getting a specific user by ID."""
    # Create a user
    create_response = client.post("/api/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123"
    })
    user_id = create_response.json()["id"]

    # Get the user
    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"


def test_get_user_not_found(client: TestClient):
    """Test getting non-existent user returns 404."""
    response = client.get("/api/users/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_user(client: TestClient):
    """Test updating a user."""
    # Create a user
    create_response = client.post("/api/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123"
    })
    user_id = create_response.json()["id"]

    # Update the user
    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/api/users/{user_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["updated_at"] is not None


def test_update_user_not_found(client: TestClient):
    """Test updating non-existent user returns 404."""
    response = client.put("/api/users/999", json={"full_name": "Test"})

    assert response.status_code == 404


def test_delete_user(client: TestClient):
    """Test deleting a user."""
    # Create a user
    create_response = client.post("/api/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepassword123"
    })
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == 204

    # Verify user is deleted
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client: TestClient):
    """Test deleting non-existent user returns 404."""
    response = client.delete("/api/users/999")

    assert response.status_code == 404
