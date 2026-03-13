from __future__ import annotations

from db import get_connection


def _validate_book_payload(title: str, author: str, qty: int) -> tuple[str, str, int]:
    title = title.strip()
    author = author.strip()
    if not title:
        raise ValueError("Title is required")
    if not author:
        raise ValueError("Author is required")
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    return title, author, qty


def add_book(title, author, qty):
    title, author, qty = _validate_book_payload(title, author, qty)
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO books(title,author,quantity) VALUES(%s,%s,%s)",
            (title, author, qty),
        )
        con.commit()
    finally:
        cur.close()
        con.close()


def update_book(book_id, title, author, qty):
    title, author, qty = _validate_book_payload(title, author, qty)
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT id FROM books WHERE id=%s", (book_id,))
        if not cur.fetchone():
            raise ValueError("Book not found")

        cur.execute(
            "UPDATE books SET title=%s, author=%s, quantity=%s WHERE id=%s",
            (title, author, qty, book_id),
        )
        con.commit()
    finally:
        cur.close()
        con.close()


def delete_book(book_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM issued WHERE book_id=%s AND return_date IS NULL", (book_id,))
        active_loans = cur.fetchone()[0]
        if active_loans:
            raise ValueError("Cannot delete a book that is currently issued")

        cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
        if cur.rowcount == 0:
            raise ValueError("Book not found")
        con.commit()
    finally:
        cur.close()
        con.close()


def get_book_by_id(book_id):
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT id, title, author, quantity FROM books WHERE id=%s", (book_id,))
        return cur.fetchone()
    finally:
        cur.close()
        con.close()


def search_books(keyword):
    con = get_connection()
    cur = con.cursor()
    try:
        key = f"%{keyword.strip()}%"
        cur.execute(
            "SELECT id, title, author, quantity FROM books "
            "WHERE CAST(id AS CHAR) LIKE %s OR title LIKE %s OR author LIKE %s "
            "ORDER BY id DESC",
            (key, key, key),
        )
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def get_books():
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SELECT id, title, author, quantity FROM books ORDER BY id DESC")
        return cur.fetchall()
    finally:
        cur.close()
        con.close()
