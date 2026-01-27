from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.database import Base


class Environment(Base):
    __tablename__ = "environments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    base_url: Mapped[str] = mapped_column(String(500), default="")
    variables: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
