from __future__ import annotations

import json
from typing import Any

from app.frontend.services.api_client import ApiClient


class RequestViewModel:
    def __init__(self, client: ApiClient):
        self.client = client

    def list_envs(self) -> list[dict[str, Any]]:
        return self.client.list_envs()

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.execute(payload)

    @staticmethod
    def parse_json(text: str) -> dict:
        if not text.strip():
            return {}
        return json.loads(text)
