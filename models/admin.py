
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
