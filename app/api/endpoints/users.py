"""User endpoints."""

from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.api.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserList,
)

router = APIRouter()

# In-memory storage for demo purposes
users_db: dict[int, dict] = {}
user_id_counter = 1


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user with the following information:

    - **email**: User's email address
    - **username**: Unique username (3-50 characters)
    - **full_name**: Optional full name
    - **password**: Password (8-100 characters)
    """
    global user_id_counter

    # Check if username already exists
    for existing_user in users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

    from datetime import datetime
    user_data = {
        "id": user_id_counter,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": None,
    }
    users_db[user_id_counter] = user_data
    user_id_counter += 1

    return UserResponse(**user_data)


@router.get(
    "/",
    response_model=UserList,
    summary="Get all users",
)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> UserList:
    """
    Retrieve a paginated list of all users.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    """
    all_users = list(users_db.values())
    total = len(all_users)

    # Calculate pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = all_users[start:end]

    return UserList(
        users=[UserResponse(**user) for user in paginated_users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
async def get_user(user_id: int) -> UserResponse:
    """
    Get a specific user by ID.

    - **user_id**: The ID of the user to retrieve
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return UserResponse(**users_db[user_id])


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
)
async def update_user(user_id: int, user_update: UserUpdate) -> UserResponse:
    """
    Update a user's information.

    - **user_id**: The ID of the user to update
    - **email**: New email address (optional)
    - **full_name**: New full name (optional)
    - **password**: New password (optional)
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user_data = users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)

    from datetime import datetime
    user_data.update(update_data)
    user_data["updated_at"] = datetime.now()

    return UserResponse(**user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
)
async def delete_user(user_id: int):
    """
    Delete a user by ID.

    - **user_id**: The ID of the user to delete
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    del users_db[user_id]
    return None
