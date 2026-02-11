from db import get_connection

def add_student(name, dept):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO students(name,dept) VALUES(%s,%s)",
        (name, dept)
    )
    con.commit()
    con.close()


def register_student(name, dept):
    """Register a student with duplicate check.
    Returns (True, None) on success or (False, error_message) on failure.
    """
    con = get_connection()
    cur = con.cursor()
    # simple duplicate check: same name and dept
    cur.execute("SELECT id FROM students WHERE name=%s AND dept=%s", (name, dept))
    if cur.fetchone():
        con.close()
        return False, "Student with same name and department already exists"

    cur.execute(
        "INSERT INTO students(name,dept) VALUES(%s,%s)",
        (name, dept)
    )
    student_id = cur.lastrowid

    # if username/password provided via kwargs (we keep function signature same, but callers may set attributes after)
    con.commit()
    con.close()
    return True, student_id


def create_student_user(student_id, username, password):
    """Create a login for a student. Returns (True, None) or (False, errmsg)."""
    con = get_connection()
    cur = con.cursor()
    # check username uniqueness
    cur.execute("SELECT id FROM student_users WHERE username=%s", (username,))
    if cur.fetchone():
        con.close()
        return False, "Username already exists"

    cur.execute(
        "INSERT INTO student_users(student_id, username, password) VALUES(%s,%s,%s)",
        (student_id, username, password)
    )
    con.commit()
    con.close()
    return True, None


def validate_student_login(username, password):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT student_id FROM student_users WHERE username=%s AND password=%s",
        (username, password)
    )
    row = cur.fetchone()
    con.close()
    if row:
        return True, row[0]
    return False, None


def get_student_by_id(student_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id,name,dept FROM students WHERE id=%s", (student_id,))
    row = cur.fetchone()
    con.close()
    return row


def get_student_by_username(username):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "SELECT s.id, s.name, s.dept FROM students s JOIN student_users u ON s.id=u.student_id WHERE u.username=%s",
        (username,)
    )
    row = cur.fetchone()
    con.close()
    return row


def update_student(stu_id, name, dept):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE students SET name=%s, dept=%s WHERE id=%s",
        (name, dept, stu_id)
    )
    con.commit()
    con.close()


def delete_student(stu_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (stu_id,))
    con.commit()
    con.close()


def search_students(keyword):
    con = get_connection()
    cur = con.cursor()
    key = "%" + keyword + "%"
    cur.execute(
        "SELECT * FROM students WHERE name LIKE %s OR dept LIKE %s",
        (key, key)
    )
    rows = cur.fetchall()
    con.close()
    return rows


def get_students():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()
    return rows
