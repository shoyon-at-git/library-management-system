from __future__ import annotations

from db import column_exists, get_connection
from utils.security import hash_password, verify_password


LEGACY_PASSWORD_COLUMN = "password" if True else None


def _row_supports_legacy_password() -> bool:
    return column_exists("admin", "password")


def validate_login(username: str, password: str) -> bool:
    con = get_connection()
    cur = con.cursor()
    try:
        if _row_supports_legacy_password():
            cur.execute(
                "SELECT password_hash, password_salt, password FROM admin WHERE username=%s",
                (username,),
            )
        else:
            cur.execute(
                "SELECT password_hash, password_salt FROM admin WHERE username=%s",
                (username,),
            )
        row = cur.fetchone()
        if not row:
            return False

        password_hash = row[0]
        password_salt = row[1]
        legacy_password = row[2] if len(row) > 2 else None

        if verify_password(password, password_hash, password_salt):
            return True

        if legacy_password and password == legacy_password:
            new_hash, new_salt = hash_password(password)
            cur.execute(
                "UPDATE admin SET password_hash=%s, password_salt=%s WHERE username=%s",
                (new_hash, new_salt, username),
            )
            con.commit()
            return True

        return False
    finally:
        cur.close()
        con.close()


def register_admin(username: str, password: str):
    """Register a new admin user. Returns (True, None) or (False, error_message)."""
    username = username.strip()
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT username FROM admin WHERE username=%s", (username,))
        if cur.fetchone():
            return False, "Username already exists"

        password_hash, salt = hash_password(password)
        if _row_supports_legacy_password():
            cur.execute(
                "INSERT INTO admin(username, password, password_hash, password_salt) VALUES(%s,%s,%s,%s)",
                (username, None, password_hash, salt),
            )
        else:
            cur.execute(
                "INSERT INTO admin(username, password_hash, password_salt) VALUES(%s,%s,%s)",
                (username, password_hash, salt),
            )
        con.commit()
        return True, None
    finally:
        cur.close()
        con.close()
