from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.backend.schemas.request import AuthConfig


class ExecuteRequest(BaseModel):
    method: str = Field(default="GET")
    url: str = Field(..., min_length=1, max_length=800)
    headers: dict[str, str] = Field(default_factory=dict)
    params: dict[str, str] = Field(default_factory=dict)
    body_type: str = Field(default="none")
    body: Any | None = None
    auth: AuthConfig = Field(default_factory=AuthConfig)
    env_id: int | None = None
    tests: list[dict] = Field(default_factory=list)


class ExecuteResponse(BaseModel):
    status_code: int
    headers: dict[str, str]
    body: Any | str | None
    duration_ms: int
    size_bytes: int
    tests: list[dict]
