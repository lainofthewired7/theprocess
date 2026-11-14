"""Request/response shapes for /items (the test resource).

Copy this pattern for users, entries and goals:
  XCreate  = what the client sends on POST
  XUpdate  = what the client sends on PATCH (all fields optional)
  X        = what the API returns (saved fields + id + timestamps)
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    text: str = Field(min_length=1, max_length=500)
    is_done: bool = False


class ItemUpdate(BaseModel):
    text: Optional[str] = Field(default=None, min_length=1, max_length=500)
    is_done: Optional[bool] = None


class Item(ItemCreate):
    id: str
    created_at: datetime
