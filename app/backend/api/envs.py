from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.environment import Environment
from app.backend.schemas.environment import EnvironmentCreate, EnvironmentOut, EnvironmentUpdate

router = APIRouter(prefix="/envs", tags=["envs"])


@router.get("", response_model=list[EnvironmentOut])
def list_envs(db: Session = Depends(get_db)):
    return db.query(Environment).order_by(Environment.id).all()


@router.post("", response_model=EnvironmentOut)
def create_env(payload: EnvironmentCreate, db: Session = Depends(get_db)):
    env = Environment(name=payload.name, base_url=payload.base_url, variables=payload.variables)
    db.add(env)
    db.commit()
    db.refresh(env)
    return env


@router.put("/{env_id}", response_model=EnvironmentOut)
def update_env(env_id: int, payload: EnvironmentUpdate, db: Session = Depends(get_db)):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(env, key, value)
    db.commit()
    db.refresh(env)
    return env


@router.delete("/{env_id}")
def delete_env(env_id: int, db: Session = Depends(get_db)):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    db.delete(env)
    db.commit()
    return {"ok": True}


@router.post("/{env_id}/activate", response_model=EnvironmentOut)
def activate_env(env_id: int, db: Session = Depends(get_db)):
    env = db.query(Environment).filter(Environment.id == env_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    db.query(Environment).update({Environment.is_active: False})
    env.is_active = True
    db.commit()
    db.refresh(env)
    return env
