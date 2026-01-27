from __future__ import annotations

import json
import time
from typing import Any

import httpx

from app.backend.core.config import settings
from app.backend.core.security import mask_secret


def _apply_auth(headers: dict[str, str], params: dict[str, str], auth: dict) -> None:
    auth_type = auth.get("type", "none")
    if auth_type == "bearer":
        token = auth.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    elif auth_type == "basic":
        username = auth.get("username", "")
        password = auth.get("password", "")
        headers["Authorization"] = httpx.BasicAuth(username, password).auth_header
    elif auth_type == "api_key":
        key = auth.get("key")
        value = auth.get("value")
        location = auth.get("in", "header")
        if key and value:
            if location == "query":
                params[key] = value
            else:
                headers[key] = value


def _prepare_body(body_type: str, body: Any) -> dict[str, Any]:
    if body_type == "json":
        return {"json": body}
    if body_type == "form":
        return {"data": body or {}}
    if body_type == "raw":
        return {"content": body or ""}
    return {}


def execute_http_request(
    method: str,
    url: str,
    headers: dict[str, str],
    params: dict[str, str],
    body_type: str,
    body: Any,
    auth: dict,
) -> tuple[dict, dict]:
    safe_headers = dict(headers)
    safe_params = dict(params)
    _apply_auth(safe_headers, safe_params, auth)

    start = time.perf_counter()
    with httpx.Client(timeout=settings.request_timeout_seconds) as client:
        response = client.request(
            method=method.upper(),
            url=url,
            headers=safe_headers,
            params=safe_params,
            **_prepare_body(body_type, body),
        )
    duration_ms = int((time.perf_counter() - start) * 1000)

    response_headers = {k: v for k, v in response.headers.items()}
    content_type = response.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body_out: Any = response.json()
        except json.JSONDecodeError:
            body_out = response.text
    else:
        body_out = response.text

    response_snapshot = {
        "status_code": response.status_code,
        "headers": response_headers,
        "body": body_out,
        "duration_ms": duration_ms,
        "size_bytes": len(response.content),
    }

    auth_masked = dict(auth)
    if auth_masked.get("token"):
        auth_masked["token"] = mask_secret(auth_masked["token"])
    if auth_masked.get("password"):
        auth_masked["password"] = mask_secret(auth_masked["password"])
    if auth_masked.get("value"):
        auth_masked["value"] = mask_secret(auth_masked["value"])

    request_snapshot = {
        "method": method,
        "url": url,
        "headers": safe_headers,
        "params": safe_params,
        "body_type": body_type,
        "body": body,
        "auth": auth_masked,
    }

    return request_snapshot, response_snapshot
