from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.database import get_db
from app.backend.models.environment import Environment
from app.backend.schemas.execute import ExecuteRequest, ExecuteResponse
from app.backend.services.http_client import execute_http_request
from app.backend.services.history import save_history
from app.backend.services.tests import run_tests
from app.backend.services.variables import substitute_variables

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("", response_model=ExecuteResponse)
def execute(payload: ExecuteRequest, db: Session = Depends(get_db)):
    variables: dict[str, str] = {}
    base_url = ""
    if payload.env_id is not None:
        env = db.query(Environment).filter(Environment.id == payload.env_id).first()
        if not env:
            raise HTTPException(status_code=404, detail="Environment not found")
        variables = env.variables or {}
        base_url = env.base_url or ""

    url = substitute_variables(payload.url, variables)
    headers = substitute_variables(payload.headers, variables)
    params = substitute_variables(payload.params, variables)
    body = substitute_variables(payload.body, variables)

    if base_url and url.startswith("/"):
        url = base_url.rstrip("/") + url
    elif base_url and not url.startswith("http"):
        url = base_url.rstrip("/") + "/" + url.lstrip("/")

    request_snapshot, response_snapshot = execute_http_request(
        method=payload.method,
        url=url,
        headers=headers,
        params=params,
        body_type=payload.body_type,
        body=body,
        auth=payload.auth.model_dump(by_alias=True),
    )

    tests_result = run_tests(payload.tests, response_snapshot)
    response_snapshot["tests"] = tests_result

    save_history(
        db,
        request_snapshot=request_snapshot,
        response_snapshot=response_snapshot,
        duration_ms=response_snapshot["duration_ms"],
    )

    return ExecuteResponse(**response_snapshot)
