from __future__ import annotations

import hashlib
import secrets
import string
from typing import Tuple


DEFAULT_ITERATIONS = 200_000


def hash_password(password: str, salt: str | None = None) -> Tuple[str, str]:
    """Return a PBKDF2 password hash and salt as hex strings."""
    if not isinstance(password, str) or not password:
        raise ValueError("Password is required")

    salt_hex = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        DEFAULT_ITERATIONS,
    )
    return dk.hex(), salt_hex


def verify_password(password: str, password_hash: str | None, salt: str | None) -> bool:
    if not password_hash or not salt:
        return False
    computed_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(computed_hash, password_hash)


def generate_password(length: int = 10) -> str:
    if length < 8:
        raise ValueError("Generated password length must be at least 8")
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
