from __future__ import annotations

from datetime import datetime

from db import column_exists, get_connection
from utils.security import generate_password, hash_password, verify_password


def _validate_birth_date(birth_date: str | None) -> str | None:
    if not birth_date:
        return None
    datetime.strptime(birth_date, "%Y-%m-%d")
    return birth_date


def _generate_student_email(student_id: str, name: str) -> str:
    clean_name = "".join(ch for ch in name if ch.isalnum()).lower() or "student"
    return f"{clean_name}{student_id}@hstu.ac.bd"


def _uses_legacy_password_column() -> bool:
    return column_exists("student_users", "password")


def _students_have_internal_id() -> bool:
    return column_exists("students", "id")


def register_student(student_id, name, dept, session=None, birth_date=None):
    student_id = student_id.strip()
    name = name.strip()
    dept = dept.strip()
    session = session.strip() if session else None
    birth_date = _validate_birth_date(birth_date.strip() if birth_date else None)

    if not student_id:
        return False, "Student ID is required"
    if not name:
        return False, "Student name is required"
    if not dept:
        return False, "Department is required"

    email = _generate_student_email(student_id, name)
    password = generate_password(10)
    password_hash, password_salt = hash_password(password)

    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT student_id FROM students WHERE student_id=%s", (student_id,))
        if cur.fetchone():
            return False, "Student ID already exists"

        cur.execute("SELECT email FROM students WHERE email=%s", (email,))
        if cur.fetchone():
            return False, "Generated email already exists; try a different student name or ID"

        cur.execute(
            "INSERT INTO students(student_id, name, dept, email, session, birth_date) VALUES(%s,%s,%s,%s,%s,%s)",
            (student_id, name, dept, email, session, birth_date),
        )

        if _uses_legacy_password_column():
            cur.execute(
                "INSERT INTO student_users(student_id, username, password, password_hash, password_salt) "
                "VALUES(%s,%s,%s,%s,%s)",
                (student_id, email, password, password_hash, password_salt),
            )
        else:
            cur.execute(
                "INSERT INTO student_users(student_id, username, password_hash, password_salt) VALUES(%s,%s,%s,%s)",
                (student_id, email, password_hash, password_salt),
            )

        con.commit()
        return True, (student_id, email, password)
    finally:
        cur.close()
        con.close()


def create_student_user(student_id, username, password):
    username = username.strip()
    if not username:
        return False, "Username is required"

    password_hash, password_salt = hash_password(password)
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT id FROM student_users WHERE username=%s", (username,))
        if cur.fetchone():
            return False, "Username already exists"

        if _uses_legacy_password_column():
            cur.execute(
                "INSERT INTO student_users(student_id, username, password, password_hash, password_salt) "
                "VALUES(%s,%s,%s,%s,%s)",
                (student_id, username, password, password_hash, password_salt),
            )
        else:
            cur.execute(
                "INSERT INTO student_users(student_id, username, password_hash, password_salt) VALUES(%s,%s,%s,%s)",
                (student_id, username, password_hash, password_salt),
            )
        con.commit()
        return True, None
    finally:
        cur.close()
        con.close()


def validate_student_login(username, password):
    con = get_connection()
    cur = con.cursor()
    try:
        if _uses_legacy_password_column():
            cur.execute(
                "SELECT student_id, password_hash, password_salt, password FROM student_users WHERE username=%s",
                (username,),
            )
        else:
            cur.execute(
                "SELECT student_id, password_hash, password_salt FROM student_users WHERE username=%s",
                (username,),
            )
        row = cur.fetchone()
        if not row:
            return False, None

        student_id, password_hash, password_salt = row[:3]
        legacy_password = row[3] if len(row) > 3 else None

        if verify_password(password, password_hash, password_salt):
            return True, student_id

        if legacy_password and password == legacy_password:
            new_hash, new_salt = hash_password(password)
            cur.execute(
                "UPDATE student_users SET password_hash=%s, password_salt=%s WHERE username=%s",
                (new_hash, new_salt, username),
            )
            con.commit()
            return True, student_id

        return False, None
    finally:
        cur.close()
        con.close()


def get_student_by_id(student_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT student_id, name, dept, email, session, birth_date FROM students WHERE student_id=%s",
            (student_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        con.close()


def get_student_by_username(username):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT s.student_id, s.name, s.dept, s.email, s.session, s.birth_date "
            "FROM students s JOIN student_users u ON s.student_id = u.student_id "
            "WHERE u.username=%s",
            (username,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        con.close()


def update_student(record_id, student_id, name, dept, session=None, birth_date=None):
    student_id = student_id.strip()
    name = name.strip()
    dept = dept.strip()
    session = session.strip() if session else None
    birth_date = _validate_birth_date(birth_date.strip() if birth_date else None)

    if not record_id:
        raise ValueError("Student record ID is required")
    if not student_id:
        raise ValueError("Student ID is required")
    if not name:
        raise ValueError("Name is required")
    if not dept:
        raise ValueError("Department is required")

    new_email = _generate_student_email(student_id, name)

    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT student_id FROM students WHERE id=%s", (record_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Student not found")

        old_student_id = row[0]

        cur.execute("SELECT id FROM students WHERE student_id=%s AND id<>%s", (student_id, record_id))
        if cur.fetchone():
            raise ValueError("Student ID already exists")

        cur.execute("SELECT id FROM students WHERE email=%s AND id<>%s", (new_email, record_id))
        if cur.fetchone():
            raise ValueError("Generated email already exists for another student")

        cur.execute(
            "UPDATE students SET student_id=%s, name=%s, dept=%s, email=%s, session=%s, birth_date=%s WHERE id=%s",
            (student_id, name, dept, new_email, session, birth_date, record_id),
        )
        if cur.rowcount == 0:
            raise ValueError("Student not found")

        cur.execute("SELECT id FROM student_users WHERE username=%s AND student_id<>%s", (new_email, student_id))
        if cur.fetchone():
            raise ValueError("Updated login username would conflict with another account")

        cur.execute(
            "UPDATE student_users SET username=%s WHERE student_id=%s",
            (new_email, student_id),
        )

        con.commit()
    finally:
        cur.close()
        con.close()


def delete_student(record_id):
    if not record_id:
        raise ValueError("Student record ID is required")

    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT student_id FROM students WHERE id=%s", (record_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Student not found")

        student_id = row[0]

        cur.execute("SELECT COUNT(*) FROM issued WHERE student_id=%s AND return_date IS NULL", (student_id,))
        active_loans = cur.fetchone()[0]
        if active_loans:
            raise ValueError("Cannot delete a student with books still issued")

        cur.execute("DELETE FROM students WHERE id=%s", (record_id,))
        if cur.rowcount == 0:
            raise ValueError("Student not found")
        con.commit()
    finally:
        cur.close()
        con.close()


def search_students(keyword):
    con = get_connection()
    cur = con.cursor()
    try:
        key = f"%{keyword.strip()}%"
        if _students_have_internal_id():
            cur.execute(
                "SELECT id, student_id, name, dept, email, session, birth_date FROM students "
                "WHERE CAST(id AS CHAR) LIKE %s OR student_id LIKE %s OR name LIKE %s OR dept LIKE %s "
                "OR email LIKE %s OR session LIKE %s ORDER BY id ASC",
                (key, key, key, key, key, key),
            )
        else:
            cur.execute(
                "SELECT student_id, name, dept, email, session, birth_date FROM students "
                "WHERE student_id LIKE %s OR name LIKE %s OR dept LIKE %s OR email LIKE %s OR session LIKE %s "
                "ORDER BY student_id ASC",
                (key, key, key, key, key),
            )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_students():
    con = get_connection()
    cur = con.cursor()
    try:
        if _students_have_internal_id():
            cur.execute(
                "SELECT id, student_id, name, dept, email, session, birth_date FROM students ORDER BY id ASC"
            )
        else:
            cur.execute(
                "SELECT student_id, name, dept, email, session, birth_date FROM students ORDER BY student_id ASC"
            )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()
