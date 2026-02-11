
from db import get_connection


def validate_login(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    con.close()
    return user is not None


def register_admin(username, password):
    """Register a new admin user. Returns (True, None) on success,
    or (False, error_message) on failure.
    """
    con = get_connection()
    cur = con.cursor()
    # Check if username exists
    cur.execute("SELECT username FROM admin WHERE username=%s", (username,))
    if cur.fetchone():
        con.close()
        return False, "Username already exists"

    cur.execute(
        "INSERT INTO admin(username, password) VALUES(%s,%s)",
        (username, password)
    )
    con.commit()
    con.close()
    return True, None
