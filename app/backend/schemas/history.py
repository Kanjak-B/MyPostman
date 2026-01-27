from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class HistoryOut(BaseModel):
    id: int
    request_snapshot: dict
    response_snapshot: dict
    duration_ms: int
    model_config = ConfigDict(from_attributes=True)
