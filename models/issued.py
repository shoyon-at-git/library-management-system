from __future__ import annotations

from datetime import date, timedelta

from db import get_connection


FINE_PER_DAY = 10  # Fine amount per day per book
ISSUE_PERIOD_DAYS = 30


def issue_book(book_id, student_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT id, quantity FROM books WHERE id=%s FOR UPDATE", (book_id,))
        book = cur.fetchone()
        if not book:
            raise ValueError("Book not found")
        if book[1] <= 0:
            raise ValueError("This book is currently out of stock")

        cur.execute("SELECT student_id FROM students WHERE student_id=%s", (student_id,))
        if not cur.fetchone():
            raise ValueError("Student not found")

        cur.execute(
            "SELECT id FROM issued WHERE book_id=%s AND student_id=%s AND return_date IS NULL",
            (book_id, student_id),
        )
        if cur.fetchone():
            raise ValueError("This student already has this book issued")

        issue_date = date.today()
        due_date = issue_date + timedelta(days=ISSUE_PERIOD_DAYS)

        cur.execute(
            "INSERT INTO issued(book_id,student_id,issue_date,due_date,fine_amount) VALUES(%s,%s,%s,%s,%s)",
            (book_id, student_id, issue_date, due_date, 0),
        )
        cur.execute("UPDATE books SET quantity = quantity - 1 WHERE id=%s", (book_id,))
        con.commit()
        return due_date
    except Exception:
        con.rollback()
        raise
    finally:
        cur.close()
        con.close()


def return_book(issue_id, return_date=None):
    con = get_connection()
    cur = con.cursor()
    try:
        return_date = return_date or date.today()

        cur.execute(
            "SELECT book_id, due_date, return_date FROM issued WHERE id=%s FOR UPDATE",
            (issue_id,),
        )
        result = cur.fetchone()
        if not result:
            raise ValueError("Issue record not found")

        book_id, due_date, existing_return_date = result
        if existing_return_date is not None:
            raise ValueError("This book has already been returned")

        fine = 0
        if due_date and return_date > due_date:
            overdue_days = (return_date - due_date).days
            fine = overdue_days * FINE_PER_DAY

        cur.execute(
            "UPDATE issued SET return_date=%s, fine_amount=%s, fine_paid=%s, fine_paid_at=%s WHERE id=%s",
            (return_date, fine, 0, None, issue_id),
        )
        cur.execute("UPDATE books SET quantity = quantity + 1 WHERE id=%s", (book_id,))
        con.commit()
        return fine
    except Exception:
        con.rollback()
        raise
    finally:
        cur.close()
        con.close()


def get_issued():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT id, book_id, student_id, issue_date, due_date, return_date, fine_amount FROM issued ORDER BY id DESC"
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_overdue_books():
    con = get_connection()
    cur = con.cursor()
    try:
        today = date.today()
        cur.execute(
            """
            SELECT id, book_id, student_id, issue_date, due_date,
                   (DATEDIFF(%s, due_date) * %s) AS fine_amount
            FROM issued
            WHERE return_date IS NULL AND due_date < %s
            ORDER BY due_date ASC
            """,
            (today, FINE_PER_DAY, today),
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_student_fines(student_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "SELECT COALESCE(SUM(fine_amount), 0) FROM issued WHERE student_id=%s AND fine_amount > 0",
            (student_id,),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        con.close()


def pay_fine(issue_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT fine_amount, return_date FROM issued WHERE id=%s", (issue_id,))
        record = cur.fetchone()
        if not record:
            raise ValueError("Issue record not found")
        if record[1] is None:
            raise ValueError("Fine can only be paid after the book is returned")
        if float(record[0] or 0) <= 0:
            raise ValueError("No fine due for this record")

        cur.execute(
            "UPDATE issued SET fine_amount=0, fine_paid=1, fine_paid_at=NOW() WHERE id=%s",
            (issue_id,),
        )
        con.commit()
    finally:
        cur.close()
        con.close()
