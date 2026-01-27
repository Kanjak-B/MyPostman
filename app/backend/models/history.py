from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.database import Base


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    request_snapshot: Mapped[dict] = mapped_column(JSON)
    response_snapshot: Mapped[dict] = mapped_column(JSON)
    duration_ms: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
