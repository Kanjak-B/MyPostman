from __future__ import annotations

from sqlalchemy.orm import Session

from app.backend.models.history import History


def save_history(db: Session, request_snapshot: dict, response_snapshot: dict, duration_ms: int) -> History:
    history = History(
        request_snapshot=request_snapshot,
        response_snapshot=response_snapshot,
        duration_ms=duration_ms,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
