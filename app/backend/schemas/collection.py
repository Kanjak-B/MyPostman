from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class CollectionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: str = Field(default="", max_length=500)


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=500)


class CollectionOut(CollectionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
