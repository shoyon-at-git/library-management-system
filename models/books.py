from db import get_connection

def add_book(title, author, qty):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO books(title,author,quantity) VALUES(%s,%s,%s)",
        (title, author, qty)
    )
    con.commit()
    con.close()


def update_book(book_id, title, author, qty):
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE books SET title=%s, author=%s, quantity=%s WHERE id=%s",
        (title, author, qty, book_id)
    )
    con.commit()
    con.close()


def delete_book(book_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
    con.commit()
    con.close()


def search_books(keyword):
    con = get_connection()
    cur = con.cursor()
    key = "%" + keyword + "%"
    cur.execute(
        "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s",
        (key, key)
    )
    rows = cur.fetchall()
    con.close()
    return rows


def get_books():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    con.close()
    return rows
