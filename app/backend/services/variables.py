from __future__ import annotations

import re
from typing import Any


VAR_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def substitute_variables(value: Any, variables: dict[str, str]) -> Any:
    if isinstance(value, str):
        return VAR_PATTERN.sub(lambda m: variables.get(m.group(1), m.group(0)), value)
    if isinstance(value, dict):
        return {k: substitute_variables(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute_variables(v, variables) for v in value]
    return value
