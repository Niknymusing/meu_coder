"""Tests for item endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_create_item(client: TestClient):
    """Test creating a new item."""
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 29.99,
        "is_available": True
    }

    response = client.post("/api/items/", json=item_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert data["is_available"] == item_data["is_available"]
    assert "id" in data
    assert "created_at" in data


def test_create_item_negative_price(client: TestClient):
    """Test creating item with negative price fails."""
    item_data = {
        "name": "Test Item",
        "price": -10.0
    }

    response = client.post("/api/items/", json=item_data)

    assert response.status_code == 422


def test_create_item_zero_price(client: TestClient):
    """Test creating item with zero price fails."""
    item_data = {
        "name": "Test Item",
        "price": 0.0
    }

    response = client.post("/api/items/", json=item_data)

    assert response.status_code == 422


def test_get_items(client: TestClient):
    """Test getting list of items."""
    # Create test items
    for i in range(3):
        client.post("/api/items/", json={
            "name": f"Item {i}",
            "price": 10.0 + i
        })

    response = client.get("/api/items/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 10


def test_get_items_available_only(client: TestClient):
    """Test filtering available items only."""
    # Create items with different availability
    client.post("/api/items/", json={
        "name": "Available Item",
        "price": 10.0,
        "is_available": True
    })
    client.post("/api/items/", json={
        "name": "Unavailable Item",
        "price": 20.0,
        "is_available": False
    })

    response = client.get("/api/items/?available_only=true")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Available Item"


def test_get_items_pagination(client: TestClient):
    """Test item list pagination."""
    # Create 5 items
    for i in range(5):
        client.post("/api/items/", json={
            "name": f"Item {i}",
            "price": 10.0 + i
        })

    # Get page 1 with 2 items
    response = client.get("/api/items/?page=1&page_size=2")
    data = response.json()

    assert response.status_code == 200
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1


def test_get_item_by_id(client: TestClient):
    """Test getting a specific item by ID."""
    # Create an item
    create_response = client.post("/api/items/", json={
        "name": "Test Item",
        "price": 29.99
    })
    item_id = create_response.json()["id"]

    # Get the item
    response = client.get(f"/api/items/{item_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"


def test_get_item_not_found(client: TestClient):
    """Test getting non-existent item returns 404."""
    response = client.get("/api/items/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_item(client: TestClient):
    """Test updating an item."""
    # Create an item
    create_response = client.post("/api/items/", json={
        "name": "Test Item",
        "price": 29.99
    })
    item_id = create_response.json()["id"]

    # Update the item
    update_data = {
        "name": "Updated Item",
        "price": 39.99
    }
    response = client.put(f"/api/items/{item_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 39.99
    assert data["updated_at"] is not None


def test_update_item_partial(client: TestClient):
    """Test partial update of an item."""
    # Create an item
    create_response = client.post("/api/items/", json={
        "name": "Test Item",
        "price": 29.99,
        "description": "Original description"
    })
    item_id = create_response.json()["id"]

    # Update only the price
    update_data = {"price": 19.99}
    response = client.put(f"/api/items/{item_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 19.99
    assert data["name"] == "Test Item"
    assert data["description"] == "Original description"


def test_update_item_not_found(client: TestClient):
    """Test updating non-existent item returns 404."""
    response = client.put("/api/items/999", json={"price": 10.0})

    assert response.status_code == 404


def test_delete_item(client: TestClient):
    """Test deleting an item."""
    # Create an item
    create_response = client.post("/api/items/", json={
        "name": "Test Item",
        "price": 29.99
    })
    item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(f"/api/items/{item_id}")

    assert response.status_code == 204

    # Verify item is deleted
    get_response = client.get(f"/api/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client: TestClient):
    """Test deleting non-existent item returns 404."""
    response = client.delete("/api/items/999")

    assert response.status_code == 404
