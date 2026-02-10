
from db import get_connection
from datetime import date

def issue_book(book_id, student_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO issued(book_id,student_id,issue_date) VALUES(%s,%s,%s)",
                (book_id, student_id, date.today()))
    con.commit()
    con.close()

def return_book(issue_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE issued SET return_date=%s WHERE id=%s",
                (date.today(), issue_id))
    con.commit()
    con.close()

def get_issued():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM issued")
    rows = cur.fetchall()
    con.close()
    return rows
