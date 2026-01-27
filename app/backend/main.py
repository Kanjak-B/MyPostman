from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI

from app.backend.api import collections, envs, execute, history, requests
from app.backend.database import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(title="Kanjakitude - MyPostman Backend", version="0.1.0")

    app.include_router(envs.router)
    app.include_router(collections.router)
    app.include_router(requests.router)
    app.include_router(execute.router)
    app.include_router(history.router)

    return app


app = create_app()


@app.on_event("startup")
def on_startup() -> None:
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
