from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.history import History
from app.backend.schemas.history import HistoryOut

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryOut])
def list_history(db: Session = Depends(get_db)):
    return db.query(History).order_by(History.id.desc()).all()


@router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    item = db.query(History).filter(History.id == history_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="History not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
