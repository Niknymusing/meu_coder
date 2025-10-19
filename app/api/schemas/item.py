"""Item schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    """Base item schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    is_available: bool = True


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None


class ItemResponse(ItemBase):
    """Schema for item response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ItemList(BaseModel):
    """Schema for list of items."""
    items: list[ItemResponse]
    total: int
    page: int
    page_size: int
