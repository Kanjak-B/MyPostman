from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class EnvironmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    base_url: str = Field(default="", max_length=500)
    variables: dict[str, str] = Field(default_factory=dict)


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    base_url: str | None = Field(default=None, max_length=500)
    variables: dict[str, str] | None = None
    is_active: bool | None = None


class EnvironmentOut(EnvironmentBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
