from __future__ import annotations

from typing import Any

import httpx


class ApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def list_envs(self) -> list[dict[str, Any]]:
        response = httpx.get(f"{self.base_url}/envs")
        response.raise_for_status()
        return response.json()

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = httpx.post(f"{self.base_url}/execute", json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()
