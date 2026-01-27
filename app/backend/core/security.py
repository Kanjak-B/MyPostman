from __future__ import annotations

from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet

KEY_PATH = Path(__file__).resolve().parent.parent / "data" / ".key"


def _load_or_create_key() -> bytes:
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if KEY_PATH.exists():
        return KEY_PATH.read_bytes()
    key = Fernet.generate_key()
    KEY_PATH.write_bytes(key)
    return key


def get_fernet() -> Fernet:
    return Fernet(_load_or_create_key())


def encrypt_value(value: str) -> str:
    if not value:
        return value
    return get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    if not value:
        return value
    try:
        return get_fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except Exception:
        return value


def mask_secret(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    return "****"
