"""Item endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.api.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemList,
)

router = APIRouter()

# In-memory storage for demo purposes
items_db: dict[int, dict] = {}
item_id_counter = 1


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
async def create_item(item: ItemCreate) -> ItemResponse:
    """
    Create a new item with the following information:

    - **name**: Item name (1-100 characters)
    - **description**: Optional item description (max 500 characters)
    - **price**: Item price (must be greater than 0)
    - **is_available**: Availability status (default: true)
    """
    global item_id_counter

    from datetime import datetime
    item_data = {
        "id": item_id_counter,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available,
        "created_at": datetime.now(),
        "updated_at": None,
    }
    items_db[item_id_counter] = item_data
    item_id_counter += 1

    return ItemResponse(**item_data)


@router.get(
    "/",
    response_model=ItemList,
    summary="Get all items",
)
async def get_items(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    available_only: bool = Query(False, description="Filter only available items"),
) -> ItemList:
    """
    Retrieve a paginated list of all items.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    - **available_only**: Filter to show only available items (default: false)
    """
    all_items = list(items_db.values())

    if available_only:
        all_items = [item for item in all_items if item["is_available"]]

    total = len(all_items)

    # Calculate pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = all_items[start:end]

    return ItemList(
        items=[ItemResponse(**item) for item in paginated_items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
)
async def get_item(item_id: int) -> ItemResponse:
    """
    Get a specific item by ID.

    - **item_id**: The ID of the item to retrieve
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    return ItemResponse(**items_db[item_id])


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update item",
)
async def update_item(item_id: int, item_update: ItemUpdate) -> ItemResponse:
    """
    Update an item's information.

    - **item_id**: The ID of the item to update
    - **name**: New item name (optional)
    - **description**: New description (optional)
    - **price**: New price (optional)
    - **is_available**: New availability status (optional)
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    item_data = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)

    from datetime import datetime
    item_data.update(update_data)
    item_data["updated_at"] = datetime.now()

    return ItemResponse(**item_data)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item",
)
async def delete_item(item_id: int):
    """
    Delete an item by ID.

    - **item_id**: The ID of the item to delete
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    del items_db[item_id]
    return None
