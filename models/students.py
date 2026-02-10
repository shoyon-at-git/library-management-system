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
