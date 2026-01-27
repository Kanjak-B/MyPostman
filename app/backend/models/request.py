from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.database import Base


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    collection_id: Mapped[int | None] = mapped_column(ForeignKey("collections.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    method: Mapped[str] = mapped_column(String(10), default="GET")
    url: Mapped[str] = mapped_column(String(800))
    headers: Mapped[dict] = mapped_column(JSON, default=dict)
    params: Mapped[dict] = mapped_column(JSON, default=dict)
    body_type: Mapped[str] = mapped_column(String(20), default="none")
    body: Mapped[dict | str | None] = mapped_column(JSON, default=None)
    auth: Mapped[dict] = mapped_column(JSON, default=dict)
    tests: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
