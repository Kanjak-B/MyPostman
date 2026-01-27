from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.collection import Collection
from app.backend.schemas.collection import CollectionCreate, CollectionOut, CollectionUpdate

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("", response_model=list[CollectionOut])
def list_collections(db: Session = Depends(get_db)):
    return db.query(Collection).order_by(Collection.id).all()


@router.post("", response_model=CollectionOut)
def create_collection(payload: CollectionCreate, db: Session = Depends(get_db)):
    collection = Collection(name=payload.name, description=payload.description)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


@router.get("/{collection_id}", response_model=CollectionOut)
def get_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.put("/{collection_id}", response_model=CollectionOut)
def update_collection(collection_id: int, payload: CollectionUpdate, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(collection, key, value)
    db.commit()
    db.refresh(collection)
    return collection


@router.delete("/{collection_id}")
def delete_collection(collection_id: int, db: Session = Depends(get_db)):
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db.delete(collection)
    db.commit()
    return {"ok": True}
