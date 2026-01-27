from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class AuthConfig(BaseModel):
    type: str = Field(default="none")  # none, bearer, basic, api_key
    token: str | None = None
    username: str | None = None
    password: str | None = None
    key: str | None = None
    value: str | None = None
    in_: str | None = Field(default=None, alias="in")  # header, query


class RequestBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    method: str = Field(default="GET")
    url: str = Field(..., min_length=1, max_length=800)
    headers: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    body_type: str = Field(default="none")  # none, json, form, raw
    body: Any | None = None
    auth: AuthConfig = Field(default_factory=AuthConfig)
    tests: list[dict] = Field(default_factory=list)
    collection_id: int | None = None


class RequestCreate(RequestBase):
    pass


class RequestUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    method: str | None = None
    url: str | None = Field(default=None, min_length=1, max_length=800)
    headers: dict[str, str] | None = None
    params: dict[str, str] | None = None
    body_type: str | None = None
    body: Any | None = None
    auth: AuthConfig | None = None
    tests: list[dict] | None = None
    collection_id: int | None = None


class RequestOut(RequestBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
