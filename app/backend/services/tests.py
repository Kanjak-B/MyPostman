from __future__ import annotations

from typing import Any


def run_tests(tests: list[dict], response_snapshot: dict) -> list[dict]:
    results: list[dict] = []
    status = response_snapshot.get("status_code")
    body = response_snapshot.get("body")

    for test in tests:
        test_type = test.get("type")
        expected = test.get("expected")
        passed = False
        message = ""

        if test_type == "status_code":
            passed = status == expected
            message = f"expected {expected}, got {status}"
        elif test_type == "json_key":
            key = test.get("key")
            if isinstance(body, dict) and key:
                passed = key in body
                message = f"key '{key}' present" if passed else f"missing key '{key}'"
        elif test_type == "equals":
            actual = test.get("actual")
            passed = actual == expected
            message = f"expected {expected}, got {actual}"
        else:
            message = "unknown test"

        results.append({"type": test_type, "passed": passed, "message": message})

    return results
