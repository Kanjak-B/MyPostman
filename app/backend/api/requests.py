from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.request import Request
from app.backend.schemas.request import RequestCreate, RequestOut, RequestUpdate

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestOut)
def create_request(payload: RequestCreate, db: Session = Depends(get_db)):
    request = Request(
        name=payload.name,
        method=payload.method,
        url=payload.url,
        headers=payload.headers,
        params=payload.params,
        body_type=payload.body_type,
        body=payload.body,
        auth=payload.auth.model_dump(by_alias=True),
        tests=payload.tests,
        collection_id=payload.collection_id,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.get("/{request_id}", response_model=RequestOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.put("/{request_id}", response_model=RequestOut)
def update_request(request_id: int, payload: RequestUpdate, db: Session = Depends(get_db)):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "auth" in update_data and update_data["auth"] is not None:
        update_data["auth"] = update_data["auth"].model_dump(by_alias=True)
    for key, value in update_data.items():
        setattr(request, key, value)
    db.commit()
    db.refresh(request)
    return request


@router.delete("/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(request)
    db.commit()
    return {"ok": True}
